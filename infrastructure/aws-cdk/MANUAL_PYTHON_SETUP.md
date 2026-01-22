# Manual Python 3.12 Setup (If Script Fails)

If the automated script fails, follow these manual steps:

## Step 1: Download Python 3.12 Embeddable Package

### Option A: Browser Download

1. **Open browser** and go to:
   ```
   https://www.python.org/ftp/python/3.12.0/python-3.12.0-embed-amd64.zip
   ```

2. **Save the file** to:
   ```
   C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk\python-3.12.0-embed-amd64.zip
   ```

### Option B: PowerShell Download (Manual)

```powershell
cd C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk

# Download
$url = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-embed-amd64.zip"
$output = "python-3.12.0-embed-amd64.zip"

# Use .NET WebClient for better reliability
$webClient = New-Object System.Net.WebClient
$webClient.DownloadFile($url, $output)
$webClient.Dispose()

# Verify download
if (Test-Path $output) {
    $size = (Get-Item $output).Length
    Write-Host "Downloaded: $output ($size bytes)"
} else {
    Write-Host "Download failed!"
}
```

## Step 2: Extract Python

```powershell
cd C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk

# Create directory
New-Item -ItemType Directory -Path "python-3.12-local" -Force

# Extract
Expand-Archive -Path "python-3.12.0-embed-amd64.zip" -DestinationPath "python-3.12-local" -Force

# Verify
if (Test-Path "python-3.12-local\python.exe") {
    Write-Host "Extraction successful!"
} else {
    Write-Host "Extraction failed - python.exe not found"
}
```

## Step 3: Install pip

```powershell
cd C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk

# Download get-pip.py
$pipUrl = "https://bootstrap.pypa.io/get-pip.py"
$pipFile = "python-3.12-local\get-pip.py"

Invoke-WebRequest -Uri $pipUrl -OutFile $pipFile -UseBasicParsing

# Install pip
.\python-3.12-local\python.exe get-pip.py
```

## Step 4: Create Virtual Environment

```powershell
cd C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk

# Create venv
.\python-3.12-local\python.exe -m venv .venv-cdk

# Activate
.venv-cdk\Scripts\Activate.ps1

# Verify
python --version
# Should show: Python 3.12.0
```

## Step 5: Install CDK Dependencies

```powershell
# Make sure venv is activated
.venv-cdk\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Install CDK
pip install -r requirements.txt

# Or install manually:
pip install aws-cdk-lib constructs
```

## Step 6: Verify

```powershell
# Check Python
python --version
# Expected: Python 3.12.0

# Check pip
pip --version

# Test CDK (if installed globally)
cdk --version
```

## Troubleshooting

### Issue: Download Fails

**Solution 1: Use Browser**
- Download manually from: https://www.python.org/downloads/release/python-3120/
- Scroll to "Files" section
- Download "Windows embeddable package (64-bit)"

**Solution 2: Try Alternative Mirror**
```powershell
# Alternative URL (if main site is down)
$url = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-embed-amd64.zip"
```

### Issue: Extraction Fails

**Check:**
1. File exists: `Test-Path python-3.12.0-embed-amd64.zip`
2. File size: Should be ~8-10 MB
3. File is not corrupted: Try re-downloading

**Solution:**
```powershell
# Check file
Get-Item python-3.12.0-embed-amd64.zip | Select-Object Name, Length

# If file is too small (< 1MB), re-download
# If file looks good, try manual extraction with 7-Zip or WinRAR
```

### Issue: pip Installation Fails

**Solution:**
```powershell
# Try alternative get-pip.py URL
$url = "https://raw.githubusercontent.com/pypa/get-pip/main/public/get-pip.py"
Invoke-WebRequest -Uri $url -OutFile "python-3.12-local\get-pip.py"

# Or download manually and place in python-3.12-local folder
```

### Issue: Virtual Environment Creation Fails

**Check Python executable:**
```powershell
.\python-3.12-local\python.exe --version
# Should show: Python 3.12.0
```

**If Python works but venv fails:**
```powershell
# Try with full path
$pythonExe = Resolve-Path "python-3.12-local\python.exe"
& $pythonExe -m venv .venv-cdk
```

## Quick Reference

**All commands in sequence:**
```powershell
cd C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk

# 1. Download (if not done)
$url = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-embed-amd64.zip"
Invoke-WebRequest -Uri $url -OutFile "python-3.12.0-embed-amd64.zip"

# 2. Extract
Expand-Archive -Path "python-3.12.0-embed-amd64.zip" -DestinationPath "python-3.12-local" -Force

# 3. Install pip
Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile "python-3.12-local\get-pip.py"
.\python-3.12-local\python.exe python-3.12-local\get-pip.py

# 4. Create venv
.\python-3.12-local\python.exe -m venv .venv-cdk

# 5. Activate and install
.venv-cdk\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

---

**If all else fails:** Use the browser to download Python 3.12 embeddable package and extract manually.
