# Python 3.11/3.12 Setup for AWS CDK

## Issue
AWS CDK requires Python 3.11 or 3.12, but you currently have Python 3.13.3 installed.

## Solution Options

### Option 1: Install Python 3.12 (Recommended)

#### Windows (Using Python.org Installer)

1. **Download Python 3.12**
   - Go to: https://www.python.org/downloads/release/python-3120/
   - Download "Windows installer (64-bit)" for Python 3.12.0

2. **Install Python 3.12**
   - Run the installer
   - ✅ Check "Add Python 3.12 to PATH"
   - Choose "Install Now" or "Customize installation"
   - Complete the installation

3. **Verify Installation**
   ```powershell
   py -3.12 --version
   # Should show: Python 3.12.0
   ```

4. **Use Python 3.12 for CDK**
   ```powershell
   cd C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk
   py -3.12 -m venv .venv-cdk
   .venv-cdk\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

#### Windows (Using pyenv-win)

1. **Install pyenv-win**
   ```powershell
   # Install via PowerShell
   Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
   ```

2. **Install Python 3.12**
   ```powershell
   pyenv install 3.12.0
   pyenv local 3.12.0
   ```

3. **Verify**
   ```powershell
   python --version
   # Should show: Python 3.12.0
   ```

### Option 2: Use Python 3.11

Same process as above, but download Python 3.11 from:
- https://www.python.org/downloads/release/python-3119/

### Option 3: Use Virtual Environment with Specific Python Version

If you have multiple Python versions installed:

```powershell
# Create virtual environment with Python 3.12
cd C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk
C:\Python312\python.exe -m venv .venv-cdk
.venv-cdk\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Verify CDK Works

After installing Python 3.11/3.12:

```powershell
cd C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk

# Activate virtual environment
.venv-cdk\Scripts\Activate.ps1

# Verify Python version
python --version
# Should show: Python 3.11.x or 3.12.x

# Install CDK dependencies
pip install -r requirements.txt

# Test CDK commands
cdk --version
cdk ls
cdk synth
cdk diff
```

## Quick Setup Script

Create a file `setup-cdk-env.ps1`:

```powershell
# setup-cdk-env.ps1
cd C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk

# Check if Python 3.12 is available
$python312 = Get-Command py -ErrorAction SilentlyContinue
if ($python312) {
    Write-Host "Using py launcher..."
    py -3.12 -m venv .venv-cdk
} else {
    Write-Host "Using python3.12..."
    python3.12 -m venv .venv-cdk
}

# Activate and install
.venv-cdk\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt

Write-Host "CDK environment ready!"
Write-Host "Run: .venv-cdk\Scripts\Activate.ps1"
```

Run it:
```powershell
.\setup-cdk-env.ps1
```

## Troubleshooting

### Issue: "Python 3.12 not found"

**Solution:**
- Make sure Python 3.12 is installed
- Check PATH: `$env:PATH -split ';' | Select-String python`
- Use full path: `C:\Python312\python.exe -m venv .venv-cdk`

### Issue: "cdk: command not found"

**Solution:**
- Make sure virtual environment is activated
- Install CDK: `pip install aws-cdk-lib constructs`
- Or use npx: `npx cdk --version`

### Issue: "Module not found" errors

**Solution:**
- Make sure you're in the CDK directory
- Activate virtual environment
- Reinstall: `pip install -r requirements.txt`

## Alternative: Use Docker

If Python version management is difficult:

```powershell
# Use Docker with Python 3.12
docker run -it --rm -v ${PWD}:/workspace -w /workspace python:3.12 bash
pip install -r requirements.txt
cdk synth
```

## Check Current Python Versions

```powershell
# List all Python versions
py --list

# Or check specific version
py -3.12 --version
py -3.11 --version
```

---

**Next Steps:**
1. Install Python 3.12
2. Create CDK virtual environment
3. Install CDK dependencies
4. Run `cdk ls` to verify
