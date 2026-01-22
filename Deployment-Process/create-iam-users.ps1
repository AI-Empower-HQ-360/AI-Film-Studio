# create-iam-users.ps1
# Automated script to create IAM users for GitHub Actions deployments
# Run this script to create all required IAM users and generate access keys

param(
    [Parameter(Mandatory=$false)]
    [string]$Region = "us-east-1",
    
    [Parameter(Mandatory=$false)]
    [switch]$CreateAll = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$DevOnly = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$ProductionOnly = $false
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AWS IAM User Creation Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

function Write-Info { Write-Host "[INFO] $args" -ForegroundColor Green }
function Write-Warn { Write-Host "[WARN] $args" -ForegroundColor Yellow }
function Write-Error { Write-Host "[ERROR] $args" -ForegroundColor Red }

# Check AWS CLI
if (-not (Get-Command aws -ErrorAction SilentlyContinue)) {
    Write-Error "AWS CLI not found. Please install AWS CLI first."
    exit 1
}

# Verify AWS credentials
Write-Info "Verifying AWS credentials..."
try {
    $identity = aws sts get-caller-identity --output json | ConvertFrom-Json
    Write-Info "Connected to AWS Account: $($identity.Account)"
    Write-Info "User/Role: $($identity.Arn)"
} catch {
    Write-Error "Failed to verify AWS credentials. Run 'aws configure' first."
    exit 1
}

# IAM Policy for CDK deployments (PowerUserAccess equivalent, but more restrictive)
$cdkDeployPolicy = @"
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "cloudformation:*",
                "ec2:*",
                "ecs:*",
                "rds:*",
                "s3:*",
                "cloudfront:*",
                "sqs:*",
                "sns:*",
                "elasticache:*",
                "secretsmanager:*",
                "logs:*",
                "events:*",
                "iam:PassRole",
                "iam:GetRole",
                "iam:GetRolePolicy",
                "iam:ListRolePolicies",
                "iam:ListAttachedRolePolicies",
                "sts:GetCallerIdentity"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Deny",
            "Action": [
                "iam:CreateUser",
                "iam:DeleteUser",
                "iam:CreateRole",
                "iam:DeleteRole",
                "iam:DeleteAccountPasswordPolicy"
            ],
            "Resource": "*"
        }
    ]
}
"@

# Users to create
$users = @()

if ($CreateAll -or $DevOnly) {
    $users += @{
        Name = "dev-deployer"
        Description = "GitHub Actions deployment user for dev environment"
        Policy = $cdkDeployPolicy
    }
}

if ($CreateAll -or $ProductionOnly) {
    $users += @{
        Name = "prod-deployer"
        Description = "GitHub Actions deployment user for production environment"
        Policy = $cdkDeployPolicy
    }
}

if ($CreateAll) {
    $users += @{
        Name = "staging-deployer"
        Description = "GitHub Actions deployment user for staging environment"
        Policy = $cdkDeployPolicy
    }
    
    $users += @{
        Name = "sandbox-deployer"
        Description = "GitHub Actions deployment user for sandbox environment"
        Policy = $cdkDeployPolicy
    }
}

if ($users.Count -eq 0) {
    Write-Warn "No users selected. Use -CreateAll, -DevOnly, or -ProductionOnly"
    exit 0
}

Write-Host ""
Write-Host "Users to create:" -ForegroundColor Yellow
foreach ($user in $users) {
    Write-Host "  - $($user.Name)" -ForegroundColor White
}
Write-Host ""

$confirm = Read-Host "Continue? (y/N)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Info "Cancelled."
    exit 0
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Creating IAM Users" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$results = @()

foreach ($user in $users) {
    Write-Host "Processing: $($user.Name)" -ForegroundColor Yellow
    
    # Check if user already exists
    try {
        $existing = aws iam get-user --user-name $user.Name --output json 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Warn "User $($user.Name) already exists. Skipping creation."
            $results += @{
                UserName = $user.Name
                Status = "Exists"
                AccessKeyId = "N/A"
                SecretAccessKey = "N/A"
            }
            continue
        }
    } catch {
        # User doesn't exist, continue with creation
    }
    
    # Create user
    try {
        Write-Info "Creating user: $($user.Name)"
        $createUser = aws iam create-user `
            --user-name $user.Name `
            --tags "Key=Purpose,Value=GitHubActions" "Key=Environment,Value=$($user.Name.Split('-')[0])" `
            --output json | ConvertFrom-Json
        
        Write-Info "User created: $($createUser.User.Arn)"
    } catch {
        Write-Error "Failed to create user: $_"
        continue
    }
    
    # Create inline policy
    try {
        Write-Info "Creating inline policy for $($user.Name)"
        $policyName = "$($user.Name)-cdk-deploy-policy"
        $policyFile = [System.IO.Path]::GetTempFileName()
        $user.Policy | Out-File -FilePath $policyFile -Encoding UTF8
        
        aws iam put-user-policy `
            --user-name $user.Name `
            --policy-name $policyName `
            --policy-document "file://$policyFile" | Out-Null
        
        Remove-Item $policyFile
        Write-Info "Policy attached: $policyName"
    } catch {
        Write-Error "Failed to create policy: $_"
        continue
    }
    
    # Create access key
    try {
        Write-Info "Creating access key for $($user.Name)"
        $accessKey = aws iam create-access-key `
            --user-name $user.Name `
            --output json | ConvertFrom-Json
        
        $accessKeyId = $accessKey.AccessKey.AccessKeyId
        $secretAccessKey = $accessKey.AccessKey.SecretAccessKey
        
        Write-Info "Access key created: $accessKeyId"
        
        $results += @{
            UserName = $user.Name
            Status = "Created"
            AccessKeyId = $accessKeyId
            SecretAccessKey = $secretAccessKey
        }
    } catch {
        Write-Error "Failed to create access key: $_"
        $results += @{
            UserName = $user.Name
            Status = "Error"
            AccessKeyId = "N/A"
            SecretAccessKey = "N/A"
        }
    }
    
    Write-Host ""
}

# Display results
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Results Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

foreach ($result in $results) {
    Write-Host "User: $($result.UserName)" -ForegroundColor Yellow
    Write-Host "  Status: $($result.Status)" -ForegroundColor $(if ($result.Status -eq "Created") { "Green" } else { "Yellow" })
    
    if ($result.Status -eq "Created") {
        Write-Host "  Access Key ID: $($result.AccessKeyId)" -ForegroundColor Cyan
        Write-Host "  Secret Access Key: $($result.SecretAccessKey)" -ForegroundColor Red
        Write-Host ""
        Write-Host "  ⚠️  IMPORTANT: Copy these values to GitHub Secrets!" -ForegroundColor Yellow
        Write-Host "     GitHub Secret Name: AWS_ACCESS_KEY_ID" -ForegroundColor Gray
        Write-Host "     GitHub Secret Name: AWS_SECRET_ACCESS_KEY" -ForegroundColor Gray
    }
    Write-Host ""
}

# Save to file
$outputFile = "iam-users-output-$(Get-Date -Format 'yyyyMMdd-HHmmss').txt"
$results | ConvertTo-Json -Depth 10 | Out-File -FilePath $outputFile
Write-Info "Results saved to: $outputFile"
Write-Warn "⚠️  This file contains sensitive information. Delete it after copying secrets to GitHub!"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Next Steps" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Copy Access Key ID and Secret Access Key to GitHub:" -ForegroundColor Yellow
Write-Host "   Settings → Environments → [environment-name] → Add secret" -ForegroundColor White
Write-Host ""
Write-Host "2. Add AWS_ACCOUNT_ID secret:" -ForegroundColor Yellow
Write-Host "   Value: $($identity.Account)" -ForegroundColor White
Write-Host ""
Write-Host "3. Test deployment:" -ForegroundColor Yellow
Write-Host "   Push to develop branch (for dev) or main branch (for production)" -ForegroundColor White
Write-Host ""
Write-Host "4. Delete the output file after copying secrets:" -ForegroundColor Yellow
Write-Host "   Remove-Item $outputFile" -ForegroundColor White
Write-Host ""
