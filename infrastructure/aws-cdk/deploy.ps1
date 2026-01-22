# deploy.ps1
# Automated deployment script for AI Film Studio AWS CDK infrastructure

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("dev", "staging", "production")]
    [string]$Environment = "dev",
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "us-east-1",
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipBootstrap = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$Destroy = $false
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AI Film Studio - AWS CDK Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Colors
function Write-Info { Write-Host "[INFO] $args" -ForegroundColor Green }
function Write-Warn { Write-Host "[WARN] $args" -ForegroundColor Yellow }
function Write-Error { Write-Host "[ERROR] $args" -ForegroundColor Red }

# Step 1: Check prerequisites
Write-Info "Checking prerequisites..."

$tools = @{
    "aws" = "AWS CLI"
    "cdk" = "AWS CDK"
    "python" = "Python"
    "docker" = "Docker"
}

$missing = @()
foreach ($tool in $tools.Keys) {
    if (Get-Command $tool -ErrorAction SilentlyContinue) {
        $version = & $tool --version 2>&1 | Select-Object -First 1
        Write-Info "$($tools[$tool]) installed: $version"
    } else {
        Write-Warn "$($tools[$tool]) not found"
        $missing += $tool
    }
}

if ($missing.Count -gt 0) {
    Write-Error "Missing required tools: $($missing -join ', ')"
    Write-Host "Install instructions:" -ForegroundColor Yellow
    Write-Host "  aws: choco install awscli" -ForegroundColor Gray
    Write-Host "  cdk: npm install -g aws-cdk" -ForegroundColor Gray
    Write-Host "  python: See PYTHON_VERSION_REQUIREMENT.md" -ForegroundColor Gray
    Write-Host "  docker: https://www.docker.com/products/docker-desktop" -ForegroundColor Gray
    exit 1
}

# Step 2: Check Python version
Write-Info "Checking Python version..."
$pythonVersion = python --version 2>&1
if ($pythonVersion -match "Python 3\.(11|12)") {
    Write-Info "Python version OK: $pythonVersion"
} else {
    Write-Warn "Python version: $pythonVersion"
    Write-Warn "CDK requires Python 3.11 or 3.12"
    Write-Host "Use: py -3.12 -m venv .venv-cdk" -ForegroundColor Yellow
}

# Step 3: Check AWS authentication
Write-Info "Checking AWS authentication..."
try {
    $accountId = aws sts get-caller-identity --query Account --output text 2>&1
    if ($LASTEXITCODE -eq 0 -and $accountId) {
        Write-Info "AWS Account: $accountId"
    } else {
        throw "AWS not configured"
    }
} catch {
    Write-Error "AWS CLI not configured"
    Write-Host "Run: aws configure" -ForegroundColor Yellow
    exit 1
}

# Step 4: Check virtual environment
Write-Info "Checking virtual environment..."
if (Test-Path ".venv-cdk") {
    Write-Info "Virtual environment found"
} else {
    Write-Warn "Virtual environment not found"
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    py -3.12 -m venv .venv-cdk
    Write-Info "Virtual environment created"
}

# Activate virtual environment
if (Test-Path ".venv-cdk\Scripts\Activate.ps1") {
    & .venv-cdk\Scripts\Activate.ps1
    Write-Info "Virtual environment activated"
} else {
    Write-Error "Failed to activate virtual environment"
    exit 1
}

# Step 5: Install dependencies
Write-Info "Installing dependencies..."
try {
    pip install --upgrade pip --quiet
    pip install -r requirements.txt --quiet
    Write-Info "Dependencies installed"
} catch {
    Write-Error "Failed to install dependencies"
    exit 1
}

# Step 6: Bootstrap CDK (if needed)
if (-not $SkipBootstrap) {
    Write-Info "Checking CDK bootstrap status..."
    $region = $Region
    try {
        # Try to check if already bootstrapped
        aws cloudformation describe-stacks --stack-name CDKToolkit --region $region 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Info "CDK already bootstrapped"
        } else {
            throw "Not bootstrapped"
        }
    } catch {
        Write-Info "Bootstrapping CDK..."
        cdk bootstrap aws://$accountId/$region
        if ($LASTEXITCODE -eq 0) {
            Write-Info "CDK bootstrapped successfully"
        } else {
            Write-Error "CDK bootstrap failed"
            exit 1
        }
    }
}

# Step 7: Deploy or Destroy
if ($Destroy) {
    Write-Warn "This will destroy all infrastructure resources!"
    $confirm = Read-Host "Type 'destroy' to confirm"
    if ($confirm -eq "destroy") {
        Write-Info "Destroying infrastructure..."
        cdk destroy --context environment=$Environment --context region=$Region
        if ($LASTEXITCODE -eq 0) {
            Write-Info "Infrastructure destroyed"
        } else {
            Write-Error "Destroy failed"
            exit 1
        }
    } else {
        Write-Warn "Destroy cancelled"
        exit 0
    }
} else {
    Write-Info "Deploying infrastructure (environment: $Environment)..."
    
    # Synthesize first
    Write-Info "Synthesizing CloudFormation template..."
    cdk synth --context environment=$Environment --context region=$Region 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Synthesis failed"
        exit 1
    }
    
    # Deploy
    Write-Info "Deploying stack..."
    cdk deploy --context environment=$Environment --context region=$Region --require-approval never
    
    if ($LASTEXITCODE -eq 0) {
        Write-Info "Deployment successful!"
        
        # Show outputs
        Write-Host ""
        Write-Host "Stack Outputs:" -ForegroundColor Cyan
        aws cloudformation describe-stacks --stack-name AIFilmStudio --query 'Stacks[0].Outputs' --output table
        
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "  1. Build and push Docker images" -ForegroundColor White
        Write-Host "  2. Configure database" -ForegroundColor White
        Write-Host "  3. Set up secrets in Secrets Manager" -ForegroundColor White
        Write-Host "  4. Test API endpoints" -ForegroundColor White
        Write-Host ""
    } else {
        Write-Error "Deployment failed"
        exit 1
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
