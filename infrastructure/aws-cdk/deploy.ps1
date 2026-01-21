# PowerShell deployment script for AWS CDK infrastructure

param(
    [string]$Environment = "dev",
    [string]$Region = "us-east-1"
)

Write-Host "🚀 Deploying AI Film Studio Infrastructure" -ForegroundColor Green
Write-Host "Environment: $Environment"
Write-Host "Region: $Region"

# Activate virtual environment
if (Test-Path ".venv") {
    & .venv\Scripts\Activate.ps1
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    & .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
}

# Install AWS CDK if not present
$cdkInstalled = Get-Command cdk -ErrorAction SilentlyContinue
if (-not $cdkInstalled) {
    Write-Host "Installing AWS CDK..." -ForegroundColor Yellow
    npm install -g aws-cdk
}

# Bootstrap CDK (if needed)
Write-Host "Checking CDK bootstrap..." -ForegroundColor Yellow
$accountId = aws sts get-caller-identity --query Account --output text
cdk bootstrap "aws://$accountId/$Region" 2>$null

# Synthesize
Write-Host "Synthesizing CDK stack..." -ForegroundColor Yellow
cdk synth --context "environment=$Environment" --context "region=$Region"

# Deploy
Write-Host "Deploying stack..." -ForegroundColor Yellow
cdk deploy --context "environment=$Environment" --context "region=$Region" --require-approval never

Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host "Check outputs above for service URLs and endpoints."
