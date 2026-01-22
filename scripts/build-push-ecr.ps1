# PowerShell script to build and push Docker images to ECR
# Usage: .\scripts\build-push-ecr.ps1 -Environment dev -ImageType backend

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("dev", "staging", "production")]
    [string]$Environment = "dev",
    
    [Parameter(Mandatory=$false)]
    [ValidateSet("backend", "worker", "all")]
    [string]$ImageType = "all",
    
    [Parameter(Mandatory=$false)]
    [string]$Tag = "latest",
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "us-east-1"
)

Write-Host "=== Building and Pushing Docker Images to ECR ===" -ForegroundColor Green
Write-Host "Environment: $Environment" -ForegroundColor Cyan
Write-Host "Image Type: $ImageType" -ForegroundColor Cyan
Write-Host "Tag: $Tag" -ForegroundColor Cyan
Write-Host "Region: $Region" -ForegroundColor Cyan
Write-Host ""

# Get AWS account ID
Write-Host "Getting AWS account ID..." -ForegroundColor Yellow
$accountId = (aws sts get-caller-identity --query Account --output text)
if (-not $accountId) {
    Write-Host "Error: Failed to get AWS account ID. Make sure AWS CLI is configured." -ForegroundColor Red
    exit 1
}
Write-Host "Account ID: $accountId" -ForegroundColor Green
Write-Host ""

# ECR base URI
$ecrBase = "$accountId.dkr.ecr.$Region.amazonaws.com"

# Login to ECR
Write-Host "Logging in to ECR..." -ForegroundColor Yellow
aws ecr get-login-password --region $Region | docker login --username AWS --password-stdin $ecrBase
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to login to ECR" -ForegroundColor Red
    exit 1
}
Write-Host "Successfully logged in to ECR" -ForegroundColor Green
Write-Host ""

# Function to create ECR repository if it doesn't exist
function Create-ECRRepository {
    param(
        [string]$RepoName
    )
    
    Write-Host "Checking if repository '$RepoName' exists..." -ForegroundColor Yellow
    $repoExists = aws ecr describe-repositories --repository-names $RepoName --region $Region 2>&1
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Repository doesn't exist. Creating..." -ForegroundColor Yellow
        aws ecr create-repository `
            --repository-name $RepoName `
            --region $Region `
            --image-scanning-configuration scanOnPush=true `
            --image-tag-mutability MUTABLE
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Repository '$RepoName' created successfully" -ForegroundColor Green
        } else {
            Write-Host "Error: Failed to create repository" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "Repository '$RepoName' already exists" -ForegroundColor Green
    }
}

# Function to build and push image
function Build-And-Push {
    param(
        [string]$ImageName,
        [string]$Dockerfile,
        [string]$Context = "."
    )
    
    $repoName = "ai-film-studio-$ImageName-$Environment"
    $ecrUri = "$ecrBase/$repoName"
    
    Write-Host "=== Processing $ImageName ===" -ForegroundColor Cyan
    Write-Host "Repository: $repoName" -ForegroundColor Yellow
    Write-Host "ECR URI: $ecrUri" -ForegroundColor Yellow
    Write-Host ""
    
    # Create repository if needed
    Create-ECRRepository -RepoName $repoName
    Write-Host ""
    
    # Build image
    Write-Host "Building Docker image..." -ForegroundColor Yellow
    docker build -t "$ImageName:$Tag" -f $Dockerfile $Context
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to build image" -ForegroundColor Red
        exit 1
    }
    Write-Host "Image built successfully" -ForegroundColor Green
    Write-Host ""
    
    # Tag image
    Write-Host "Tagging image..." -ForegroundColor Yellow
    docker tag "$ImageName:$Tag" "$ecrUri:$Tag"
    docker tag "$ImageName:$Tag" "$ecrUri:latest"
    Write-Host "Image tagged successfully" -ForegroundColor Green
    Write-Host ""
    
    # Push image
    Write-Host "Pushing image to ECR..." -ForegroundColor Yellow
    docker push "$ecrUri:$Tag"
    docker push "$ecrUri:latest"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to push image" -ForegroundColor Red
        exit 1
    }
    Write-Host "Image pushed successfully" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "=== $ImageName Complete ===" -ForegroundColor Green
    Write-Host "ECR URI: $ecrUri" -ForegroundColor Cyan
    Write-Host "Tags: $Tag, latest" -ForegroundColor Cyan
    Write-Host ""
}

# Build and push images
if ($ImageType -eq "all" -or $ImageType -eq "backend") {
    Build-And-Push -ImageName "backend" -Dockerfile "Dockerfile" -Context "."
}

if ($ImageType -eq "all" -or $ImageType -eq "worker") {
    Build-And-Push -ImageName "worker" -Dockerfile "Dockerfile.worker" -Context "."
}

Write-Host "=== All Images Built and Pushed Successfully ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Update ECS service to use new image" -ForegroundColor White
Write-Host "2. Verify deployment in AWS Console" -ForegroundColor White
Write-Host ""
