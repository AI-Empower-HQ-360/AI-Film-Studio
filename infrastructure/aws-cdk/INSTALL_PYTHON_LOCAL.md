# Install Python 3.12 Locally (No System Installation)

## Option 1: Portable Python (Recommended)

Download and extract Python 3.12 to a local directory without installing system-wide.

### Steps

1. **Download Python 3.12 Embeddable Package**
   - Go to: https://www.python.org/downloads/release/python-3120/
   - Scroll down to "Files" section
   - Download: **"Windows embeddable package (64-bit)"**
   - File: `python-3.12.0-embed-amd64.zip`

2. **Extract to Local Directory**
   ```powershell
   # Create directory in your project
   cd C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk
   mkdir python-3.12-local
   
   # Extract the zip file to this directory
   # Or use PowerShell:
   Expand-Archive -Path "path\to\python-3.12.0-embed-amd64.zip" -DestinationPath "python-3.12-local"
   ```

3. **Enable pip (Required)**
   ```powershell
   cd python-3.12-local
   
   # Download get-pip.py
   Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile "get-pip.py"
   
   # Install pip
   .\python.exe get-pip.py
   ```

4. **Create Virtual Environment**
   ```powershell
   cd C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk
   
   # Use local Python
   .\python-3.12-local\python.exe -m venv .venv-cdk
   
   # Activate
   .venv-cdk\Scripts\Activate.ps1
   
   # Verify version
   python --version
   # Should show: Python 3.12.0
   ```

5. **Install CDK Dependencies**
   ```powershell
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Option 2: Use pyenv-win (Local Installation)

Install pyenv-win to manage Python versions locally.

### Steps

1. **Install pyenv-win**
   ```powershell
   # Run in PowerShell as Administrator
   Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"
   &"./install-pyenv-win.ps1"
   ```

2. **Install Python 3.12**
   ```powershell
   pyenv install 3.12.0
   ```

3. **Set Local Version**
   ```powershell
   cd C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk
   pyenv local 3.12.0
   ```

4. **Create Virtual Environment**
   ```powershell
   python -m venv .venv-cdk
   .venv-cdk\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

## Option 3: Download Full Installer (Extract Only)

Download the full installer but extract files manually.

### Steps

1. **Download Python 3.12 Installer**
   - https://www.python.org/downloads/release/python-3120/
   - Download: "Windows installer (64-bit)"

2. **Extract Without Installing**
   ```powershell
   # Use 7-Zip or WinRAR to extract the installer
   # Or use PowerShell (if you have 7-Zip):
   # 7z x python-3.12.0-amd64.exe -o"python-3.12-local"
   ```

   **Note:** This is more complex. Option 1 (embeddable package) is easier.

## Option 4: Use Docker (Fully Local, No Installation)

Use Docker to run Python 3.12 without installing anything.

### Steps

1. **Create Dockerfile**
   ```dockerfile
   # Dockerfile.cdk
   FROM python:3.12-slim
   
   WORKDIR /workspace
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   # Install CDK CLI
   RUN npm install -g aws-cdk
   
   CMD ["/bin/bash"]
   ```

2. **Build and Use**
   ```powershell
   cd C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk
   
   # Build image
   docker build -f Dockerfile.cdk -t cdk-python312 .
   
   # Run container
   docker run -it --rm `
     -v ${PWD}:/workspace `
     -w /workspace `
     cdk-python312 bash
   
   # Inside container, run CDK commands
   cdk ls
   cdk synth
   ```

## Quick Setup Script (Option 1 - Portable)

Save as `setup-local-python.ps1`:

```powershell
# setup-local-python.ps1
# Downloads and sets up Python 3.12 locally

$ErrorActionPreference = "Stop"

Write-Host "Setting up Python 3.12 locally for CDK..." -ForegroundColor Green

# Create directory
$pythonDir = "python-3.12-local"
if (Test-Path $pythonDir) {
    Write-Host "Directory $pythonDir already exists. Removing..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $pythonDir
}
New-Item -ItemType Directory -Path $pythonDir | Out-Null

# Download Python 3.12 embeddable package
$pythonUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-embed-amd64.zip"
$zipFile = "python-3.12.0-embed-amd64.zip"

Write-Host "Downloading Python 3.12 embeddable package..." -ForegroundColor Cyan
Invoke-WebRequest -Uri $pythonUrl -OutFile $zipFile

# Extract
Write-Host "Extracting..." -ForegroundColor Cyan
Expand-Archive -Path $zipFile -DestinationPath $pythonDir -Force

# Clean up zip
Remove-Item $zipFile

# Download get-pip.py
Write-Host "Setting up pip..." -ForegroundColor Cyan
$getPipUrl = "https://bootstrap.pypa.io/get-pip.py"
$getPipFile = Join-Path $pythonDir "get-pip.py"
Invoke-WebRequest -Uri $getPipUrl -OutFile $getPipFile

# Install pip
$pythonExe = Join-Path $pythonDir "python.exe"
& $pythonExe $getPipFile

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Cyan
& $pythonExe -m venv .venv-cdk

# Activate and install dependencies
Write-Host "Installing CDK dependencies..." -ForegroundColor Cyan
& .venv-cdk\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host ""
Write-Host "✅ Python 3.12 setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To activate the environment:" -ForegroundColor Yellow
Write-Host "  .venv-cdk\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "To verify:" -ForegroundColor Yellow
Write-Host "  python --version" -ForegroundColor White
Write-Host "  cdk --version" -ForegroundColor White
```

Run it:
```powershell
cd C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk
.\setup-local-python.ps1
```

## Verification

After setup:

```powershell
cd C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk

# Activate environment
.venv-cdk\Scripts\Activate.ps1

# Check Python version
python --version
# Expected: Python 3.12.0

# Check CDK
cdk --version

# Test CDK commands
cdk ls
cdk synth
```

## Directory Structure

After setup:
```
infrastructure/aws-cdk/
├── python-3.12-local/          # Local Python 3.12 (portable)
│   ├── python.exe
│   ├── python312.dll
│   └── ...
├── .venv-cdk/                  # Virtual environment
│   ├── Scripts/
│   │   ├── Activate.ps1
│   │   └── python.exe
│   └── ...
├── requirements.txt
├── app.py
└── ...
```

## Advantages of Local Installation

✅ No system-wide installation  
✅ No PATH modifications  
✅ Project-specific Python version  
✅ Easy to remove (just delete folder)  
✅ Works without admin rights  
✅ Can have multiple versions  

## Troubleshooting

### Issue: "python.exe not found"

**Solution:** Make sure you're using the full path:
```powershell
.\python-3.12-local\python.exe -m venv .venv-cdk
```

### Issue: "pip not found"

**Solution:** Install pip first:
```powershell
cd python-3.12-local
Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile "get-pip.py"
.\python.exe get-pip.py
```

### Issue: Execution Policy Error

**Solution:** Allow script execution:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

**Recommended:** Use Option 1 (Portable Python) or the setup script above.
