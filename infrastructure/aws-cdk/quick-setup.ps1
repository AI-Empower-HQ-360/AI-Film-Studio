# quick-setup.ps1
# Simplified Python 3.12 setup with better error handling

$ErrorActionPreference = "Continue"
$ProgressPreference = 'SilentlyContinue'

Write-Host "Python 3.12 Local Setup - Quick Version" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Set working directory
$workDir = "C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk"
Set-Location $workDir
Write-Host "Working directory: $workDir" -ForegroundColor Gray
Write-Host ""

# Step 1: Download
Write-Host "[1/5] Downloading Python 3.12..." -ForegroundColor Yellow
$zipFile = "python-3.12.0-embed-amd64.zip"
$pythonUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-embed-amd64.zip"

if (Test-Path $zipFile) {
    Write-Host "    File already exists, skipping download" -ForegroundColor Green
} else {
    try {
        Write-Host "    Downloading from: $pythonUrl" -ForegroundColor Gray
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($pythonUrl, $zipFile)
        $webClient.Dispose()
        
        if (Test-Path $zipFile) {
            $size = [math]::Round((Get-Item $zipFile).Length / 1MB, 2)
            Write-Host "    Download complete ($size MB)" -ForegroundColor Green
        } else {
            throw "File not found after download"
        }
    } catch {
        Write-Host "    Download failed: $_" -ForegroundColor Red
        Write-Host "    Please download manually from:" -ForegroundColor Yellow
        Write-Host "    https://www.python.org/ftp/python/3.12.0/python-3.12.0-embed-amd64.zip" -ForegroundColor Gray
        exit 1
    }
}

# Step 2: Extract
Write-Host "[2/5] Extracting Python..." -ForegroundColor Yellow
$pythonDir = "python-3.12-local"

if (-not (Test-Path $zipFile)) {
    Write-Host "    ERROR: Zip file not found: $zipFile" -ForegroundColor Red
    Write-Host "    Current directory: $(Get-Location)" -ForegroundColor Gray
    Write-Host "    Files in directory:" -ForegroundColor Gray
    Get-ChildItem | Select-Object Name | Format-Table -AutoSize
    exit 1
}

try {
    if (Test-Path $pythonDir) {
        Remove-Item -Recurse -Force $pythonDir
    }
    Expand-Archive -Path $zipFile -DestinationPath $pythonDir -Force
    Write-Host "    Extraction complete" -ForegroundColor Green
} catch {
    Write-Host "    Extraction failed: $_" -ForegroundColor Red
    exit 1
}

# Step 3: Install pip
Write-Host "[3/5] Installing pip..." -ForegroundColor Yellow
$pythonExe = Join-Path $pythonDir "python.exe"
$getPipFile = Join-Path $pythonDir "get-pip.py"

if (-not (Test-Path $pythonExe)) {
    Write-Host "    ERROR: Python executable not found: $pythonExe" -ForegroundColor Red
    exit 1
}

try {
    Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile $getPipFile -UseBasicParsing
    & $pythonExe $getPipFile 2>&1 | Out-Null
    Write-Host "    pip installed" -ForegroundColor Green
} catch {
    Write-Host "    pip installation failed: $_" -ForegroundColor Red
    Write-Host "    Continuing anyway..." -ForegroundColor Yellow
}

# Step 4: Create venv
Write-Host "[4/5] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv-cdk") {
    Remove-Item -Recurse -Force .venv-cdk
}

try {
    & $pythonExe -m venv .venv-cdk
    Write-Host "    Virtual environment created" -ForegroundColor Green
} catch {
    Write-Host "    Failed to create venv: $_" -ForegroundColor Red
    exit 1
}

# Step 5: Install dependencies
Write-Host "[5/5] Installing CDK dependencies..." -ForegroundColor Yellow
$activateScript = ".venv-cdk\Scripts\Activate.ps1"

if (-not (Test-Path $activateScript)) {
    Write-Host "    ERROR: Activation script not found" -ForegroundColor Red
    exit 1
}

try {
    & $activateScript
    python -m pip install --upgrade pip --quiet
    if (Test-Path "requirements.txt") {
        pip install -r requirements.txt
    } else {
        pip install aws-cdk-lib constructs
    }
    Write-Host "    Dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "    Installation failed: $_" -ForegroundColor Red
    Write-Host "    You can install manually after activation" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "To activate:" -ForegroundColor Yellow
Write-Host "  .venv-cdk\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "To verify:" -ForegroundColor Yellow
Write-Host "  python --version" -ForegroundColor White
Write-Host ""
