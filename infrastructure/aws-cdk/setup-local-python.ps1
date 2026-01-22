# setup-local-python.ps1
# Downloads and sets up Python 3.12 locally for CDK (no system installation)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Python 3.12 Local Setup for CDK" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Create directory
$pythonDir = "python-3.12-local"
if (Test-Path $pythonDir) {
    Write-Host "⚠️  Directory $pythonDir already exists." -ForegroundColor Yellow
    $response = Read-Host "Remove and reinstall? (y/n)"
    if ($response -eq "y" -or $response -eq "Y") {
        Write-Host "Removing existing directory..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force $pythonDir
    } else {
        Write-Host "Using existing installation." -ForegroundColor Green
        $skipDownload = $true
    }
}

if (-not $skipDownload) {
    New-Item -ItemType Directory -Path $pythonDir | Out-Null

    # Download Python 3.12 embeddable package
    $pythonUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-embed-amd64.zip"
    $zipFile = "python-3.12.0-embed-amd64.zip"

    Write-Host "📥 Downloading Python 3.12 embeddable package..." -ForegroundColor Cyan
    Write-Host "   URL: $pythonUrl" -ForegroundColor Gray
    try {
        Invoke-WebRequest -Uri $pythonUrl -OutFile $zipFile -UseBasicParsing
        Write-Host "✅ Download complete" -ForegroundColor Green
    } catch {
        Write-Host "❌ Download failed: $_" -ForegroundColor Red
        exit 1
    }

    # Extract
    Write-Host "📦 Extracting Python..." -ForegroundColor Cyan
    try {
        Expand-Archive -Path $zipFile -DestinationPath $pythonDir -Force
        Write-Host "✅ Extraction complete" -ForegroundColor Green
    } catch {
        Write-Host "❌ Extraction failed: $_" -ForegroundColor Red
        exit 1
    }

    # Clean up zip
    Remove-Item $zipFile -ErrorAction SilentlyContinue

    # Download get-pip.py
    Write-Host "📥 Setting up pip..." -ForegroundColor Cyan
    $getPipUrl = "https://bootstrap.pypa.io/get-pip.py"
    $getPipFile = Join-Path $pythonDir "get-pip.py"
    try {
        Invoke-WebRequest -Uri $getPipUrl -OutFile $getPipFile -UseBasicParsing
        Write-Host "✅ pip setup script downloaded" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to download pip setup: $_" -ForegroundColor Red
        exit 1
    }

    # Install pip
    Write-Host "🔧 Installing pip..." -ForegroundColor Cyan
    $pythonExe = Join-Path $pythonDir "python.exe"
    try {
        & $pythonExe $getPipFile
        Write-Host "✅ pip installed" -ForegroundColor Green
    } catch {
        Write-Host "❌ pip installation failed: $_" -ForegroundColor Red
        exit 1
    }
}

# Create virtual environment
Write-Host "🔧 Creating virtual environment..." -ForegroundColor Cyan
$pythonExe = Join-Path $pythonDir "python.exe"
if (-not (Test-Path $pythonExe)) {
    Write-Host "❌ Python executable not found at: $pythonExe" -ForegroundColor Red
    exit 1
}

if (Test-Path ".venv-cdk") {
    Write-Host "⚠️  Virtual environment already exists." -ForegroundColor Yellow
    $response = Read-Host "Remove and recreate? (y/n)"
    if ($response -eq "y" -or $response -eq "Y") {
        Remove-Item -Recurse -Force .venv-cdk
    } else {
        Write-Host "Using existing virtual environment." -ForegroundColor Green
        $skipVenv = $true
    }
}

if (-not $skipVenv) {
    try {
        & $pythonExe -m venv .venv-cdk
        Write-Host "✅ Virtual environment created" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to create virtual environment: $_" -ForegroundColor Red
        exit 1
    }
}

# Activate and install dependencies
Write-Host "📦 Installing CDK dependencies..." -ForegroundColor Cyan
$activateScript = ".venv-cdk\Scripts\Activate.ps1"
if (-not (Test-Path $activateScript)) {
    Write-Host "❌ Activation script not found: $activateScript" -ForegroundColor Red
    exit 1
}

try {
    & $activateScript
    python -m pip install --upgrade pip --quiet
    Write-Host "✅ pip upgraded" -ForegroundColor Green
    
    if (Test-Path "requirements.txt") {
        pip install -r requirements.txt
        Write-Host "✅ CDK dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "⚠️  requirements.txt not found, installing basic CDK packages..." -ForegroundColor Yellow
        pip install aws-cdk-lib constructs
        Write-Host "✅ Basic CDK packages installed" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Failed to install dependencies: $_" -ForegroundColor Red
    exit 1
}

# Verify installation
Write-Host ""
Write-Host "🔍 Verifying installation..." -ForegroundColor Cyan
$pythonVersion = python --version 2>&1
Write-Host "   Python: $pythonVersion" -ForegroundColor White

try {
    $cdkVersion = cdk --version 2>&1
    Write-Host "   CDK: $cdkVersion" -ForegroundColor White
} catch {
    Write-Host "   CDK: Not installed (install with: npm install -g aws-cdk)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ✅ Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "To activate the environment:" -ForegroundColor Yellow
Write-Host "  .venv-cdk\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "To test CDK:" -ForegroundColor Yellow
Write-Host "  cdk ls      # List stacks" -ForegroundColor White
Write-Host "  cdk synth   # Synthesize CloudFormation" -ForegroundColor White
Write-Host "  cdk diff    # Show differences" -ForegroundColor White
Write-Host ""
