# Python Version Requirement for AWS CDK

## Issue

AWS CDK requires Python 3.11 or 3.12, but you currently have Python 3.13.3 installed.

## Why Python 3.11/3.12 is Required

### 1. AWS CDK Library Compatibility

AWS CDK libraries (`aws-cdk-lib`, `constructs`) are built and tested against specific Python versions. As of January 2026:

- **Python 3.11**: ✅ Fully supported
- **Python 3.12**: ✅ Fully supported  
- **Python 3.13**: ❌ Not yet supported (released October 2024, CDK support pending)

### 2. Dependency Compatibility

Many CDK dependencies may not have Python 3.13 wheels available yet:
- `aws-cdk-lib` may not have 3.13-compatible builds
- Native extensions may not be compiled for 3.13
- Some transitive dependencies may fail on 3.13

### 3. Testing and Validation

AWS CDK is tested against Python 3.11 and 3.12 in CI/CD pipelines. Python 3.13 support will be added in future CDK releases.

## Current Status

**Your System:**
```
py -0p output:
 -V:3.13 *  C:\Users\ctrpr\AppData\Local\Programs\Python\Python313\python.exe
```

**Required:**
- Python 3.11.x OR
- Python 3.12.x

## Solutions

### Option 1: Install Python 3.12 (Recommended)

1. **Download Python 3.12**
   - Go to: https://www.python.org/downloads/release/python-3120/
   - Download "Windows installer (64-bit)"

2. **Install Python 3.12**
   - Run installer
   - ✅ Check "Add Python 3.12 to PATH"
   - Complete installation

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

### Option 2: Install Python 3.11

Same process as above, but download from:
- https://www.python.org/downloads/release/python-3119/

### Option 3: Use pyenv-win (Multiple Versions)

1. **Install pyenv-win**
   ```powershell
   Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"
   &"./install-pyenv-win.ps1"
   ```

2. **Install and Use Python 3.12**
   ```powershell
   pyenv install 3.12.0
   pyenv local 3.12.0
   python --version  # Should show 3.12.0
   ```

### Option 4: Use Docker (Temporary Workaround)

If you can't install Python 3.12 locally:

```powershell
# Use Docker with Python 3.12
docker run -it --rm `
  -v ${PWD}:/workspace `
  -w /workspace `
  python:3.12 bash

# Inside container
pip install -r requirements.txt
cdk synth
```

## Verification Steps

After installing Python 3.12:

```powershell
# 1. Check Python version
py -3.12 --version
# Expected: Python 3.12.0

# 2. Create CDK virtual environment
cd C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk
py -3.12 -m venv .venv-cdk

# 3. Activate environment
.venv-cdk\Scripts\Activate.ps1

# 4. Verify Python version in venv
python --version
# Expected: Python 3.12.x

# 5. Install CDK dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 6. Test CDK
cdk --version
cdk ls
cdk synth
```

## Why Not Python 3.13?

### Technical Reasons

1. **ABI Compatibility**: Python 3.13 introduced ABI changes that may break compiled extensions
2. **Library Support**: Many scientific/native libraries haven't released 3.13 wheels yet
3. **CDK Release Cycle**: AWS CDK follows a release schedule and 3.13 support will come in future versions

### Timeline

- **Python 3.13**: Released October 2024
- **CDK Support**: Typically 6-12 months after Python release
- **Expected**: Mid to late 2025 for full CDK 3.13 support

## Workaround: Force Python 3.13 (Not Recommended)

⚠️ **Warning**: This may cause compatibility issues

If you absolutely must use Python 3.13:

```powershell
cd C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk
python -m venv .venv-cdk
.venv-cdk\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt --no-deps
pip install aws-cdk-lib constructs
```

**Risks:**
- May fail during installation
- Runtime errors possible
- Not officially supported
- May break in future CDK updates

## Recommended Action

**Install Python 3.12** - It's the safest and most compatible option for AWS CDK development.

## Quick Setup Script

Save as `setup-cdk-python.ps1`:

```powershell
# setup-cdk-python.ps1
Write-Host "Setting up CDK environment with Python 3.12..."

# Check if Python 3.12 is available
$python312 = Get-Command py -ErrorAction SilentlyContinue
if (-not $python312) {
    Write-Host "ERROR: Python launcher (py) not found!"
    Write-Host "Please install Python 3.12 from https://www.python.org/downloads/"
    exit 1
}

# Check Python 3.12
$version = py -3.12 --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python 3.12 not installed!"
    Write-Host "Download from: https://www.python.org/downloads/release/python-3120/"
    exit 1
}

Write-Host "Found: $version"

# Create virtual environment
cd C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk
Write-Host "Creating virtual environment..."
py -3.12 -m venv .venv-cdk

# Activate
Write-Host "Activating virtual environment..."
.venv-cdk\Scripts\Activate.ps1

# Verify version
$venvVersion = python --version
Write-Host "Virtual environment Python: $venvVersion"

# Install dependencies
Write-Host "Installing CDK dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

Write-Host ""
Write-Host "✅ CDK environment ready!"
Write-Host "To activate: .venv-cdk\Scripts\Activate.ps1"
Write-Host "To test: cdk ls"
```

Run it:
```powershell
.\setup-cdk-python.ps1
```

## References

- [Python 3.12 Downloads](https://www.python.org/downloads/release/python-3120/)
- [Python 3.11 Downloads](https://www.python.org/downloads/release/python-3119/)
- [AWS CDK Python Documentation](https://docs.aws.amazon.com/cdk/v2/guide/work-with-cdk-python.html)
- [AWS CDK GitHub Issues](https://github.com/aws/aws-cdk/issues)

---

**Summary:** Python 3.13 is too new for AWS CDK. Install Python 3.12 for full compatibility.
