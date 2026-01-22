# setup-local-python.ps1
# Downloads and sets up Python 3.12 locally for CDK (no system installation)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Python 3.12 Local Setup for CDK" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Current directory: $((Get-Location).Path)" -ForegroundColor Gray
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

    Write-Host "[*] Downloading Python 3.12 embeddable package..." -ForegroundColor Cyan
    Write-Host "    URL: $pythonUrl" -ForegroundColor Gray
    Write-Host "    This may take a few minutes..." -ForegroundColor Gray
    
    try {
        $ProgressPreference = 'SilentlyContinue'
        Invoke-WebRequest -Uri $pythonUrl -OutFile $zipFile -UseBasicParsing -ErrorAction Stop
        
        # Verify file was downloaded
        if (-not (Test-Path $zipFile)) {
            throw "Downloaded file not found: $zipFile"
        }
        
        $fileSize = (Get-Item $zipFile).Length
        if ($fileSize -lt 1000000) {
            throw "Downloaded file is too small ($fileSize bytes). Download may have failed."
        }
        
        Write-Host "[OK] Download complete ($([math]::Round($fileSize/1MB, 2)) MB)" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Download failed: $_" -ForegroundColor Red
        if (Test-Path $zipFile) {
            Remove-Item $zipFile -ErrorAction SilentlyContinue
        }
        exit 1
    }

    # Extract
    Write-Host "[*] Extracting Python..." -ForegroundColor Cyan
    
    # Verify zip file exists before extraction
    if (-not (Test-Path $zipFile)) {
        Write-Host "[ERROR] Zip file not found: $zipFile" -ForegroundColor Red
        exit 1
    }
    
    try {
        # Create destination directory if it doesn't exist
        if (-not (Test-Path $pythonDir)) {
            New-Item -ItemType Directory -Path $pythonDir -Force | Out-Null
        }
        
        Expand-Archive -Path $zipFile -DestinationPath $pythonDir -Force -ErrorAction Stop
        
        # Verify extraction
        $pythonExe = Join-Path $pythonDir "python.exe"
        if (-not (Test-Path $pythonExe)) {
            throw "Python executable not found after extraction: $pythonExe"
        }
        
        Write-Host "[OK] Extraction complete" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Extraction failed: $_" -ForegroundColor Red
        Write-Host "       Zip file location: $((Get-Location).Path)\$zipFile" -ForegroundColor Gray
        if (Test-Path $zipFile) {
            Write-Host "       Zip file exists: Yes ($((Get-Item $zipFile).Length) bytes)" -ForegroundColor Gray
        } else {
            Write-Host "       Zip file exists: No" -ForegroundColor Gray
        }
        exit 1
    }

    # Clean up zip
    Remove-Item $zipFile -ErrorAction SilentlyContinue

    # Download get-pip.py
    Write-Host "[*] Setting up pip..." -ForegroundColor Cyan
    $getPipUrl = "https://bootstrap.pypa.io/get-pip.py"
    $getPipFile = Join-Path $pythonDir "get-pip.py"
    try {
        $ProgressPreference = 'SilentlyContinue'
        Invoke-WebRequest -Uri $getPipUrl -OutFile $getPipFile -UseBasicParsing -ErrorAction Stop
        Write-Host "[OK] pip setup script downloaded" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Failed to download pip setup: $_" -ForegroundColor Red
        Write-Host "        Trying alternative URL..." -ForegroundColor Yellow
        
        # Try alternative URL
        $getPipUrlAlt = "https://raw.githubusercontent.com/pypa/get-pip/main/public/get-pip.py"
        try {
            Invoke-WebRequest -Uri $getPipUrlAlt -OutFile $getPipFile -UseBasicParsing -ErrorAction Stop
            Write-Host "[OK] pip setup script downloaded (alternative URL)" -ForegroundColor Green
        } catch {
            Write-Host "[ERROR] Both URLs failed. Please download manually:" -ForegroundColor Red
            Write-Host "        https://bootstrap.pypa.io/get-pip.py" -ForegroundColor Gray
            exit 1
        }
    }

    # Install pip
    Write-Host "[*] Installing pip..." -ForegroundColor Cyan
    $pythonExe = Join-Path $pythonDir "python.exe"
    if (-not (Test-Path $pythonExe)) {
        Write-Host "[ERROR] Python executable not found: $pythonExe" -ForegroundColor Red
        exit 1
    }
    
    try {
        & $pythonExe $getPipFile 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] pip installed" -ForegroundColor Green
        } else {
            throw "pip installation returned exit code: $LASTEXITCODE"
        }
    } catch {
        Write-Host "[ERROR] pip installation failed: $_" -ForegroundColor Red
        Write-Host "        You may need to install pip manually" -ForegroundColor Yellow
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
Write-Host "[*] Verifying installation..." -ForegroundColor Cyan

# Check if virtual environment is activated
$venvPython = ".venv-cdk\Scripts\python.exe"
if (Test-Path $venvPython) {
    $pythonVersion = & $venvPython --version 2>&1
    Write-Host "[OK] Python: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "[WARN] Virtual environment Python not found" -ForegroundColor Yellow
    Write-Host "       Activate environment first: .venv-cdk\Scripts\Activate.ps1" -ForegroundColor Gray
}

# Check pip
if (Test-Path $venvPython) {
    $pipVersion = & $venvPython -m pip --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] pip: $($pipVersion -split ' ' | Select-Object -First 2 -Join ' ')" -ForegroundColor Green
    }
}

# Check CDK
try {
    $cdkVersion = cdk --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] CDK: $cdkVersion" -ForegroundColor Green
    }
} catch {
    Write-Host "[INFO] CDK: Not installed globally" -ForegroundColor Yellow
    Write-Host "        Install with: npm install -g aws-cdk" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  [OK] Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Activate the environment:" -ForegroundColor White
Write-Host "     .venv-cdk\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. Verify Python version:" -ForegroundColor White
Write-Host "     python --version" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. Test CDK commands:" -ForegroundColor White
Write-Host "     cdk ls      # List stacks" -ForegroundColor Gray
Write-Host "     cdk synth   # Synthesize CloudFormation" -ForegroundColor Gray
Write-Host "     cdk diff    # Show differences" -ForegroundColor Gray
Write-Host ""
