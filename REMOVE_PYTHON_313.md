# How to Remove Python 3.13

## ⚠️ Important Warning

**Before removing Python 3.13, consider:**
- You can keep both Python 3.13 and 3.12 installed
- Python 3.13 won't interfere with CDK if you use Python 3.12 in a virtual environment
- Removing Python 3.13 might break other projects that depend on it
- The local Python 3.12 setup doesn't require removing Python 3.13

## Option 1: Keep Both (Recommended)

**Best Practice:** Keep Python 3.13 for other projects, use Python 3.12 locally for CDK.

The local setup script (`setup-local-python.ps1`) doesn't require removing Python 3.13. It installs Python 3.12 in a separate folder.

## Option 2: Uninstall Python 3.13 via Windows Settings

### Steps

1. **Open Windows Settings**
   - Press `Win + I`
   - Go to **Apps** → **Installed apps**

2. **Find Python 3.13**
   - Search for "Python"
   - Look for "Python 3.13.x" entries

3. **Uninstall**
   - Click on Python 3.13
   - Click **Uninstall**
   - Follow the prompts

### Alternative: Control Panel

1. **Open Control Panel**
   - Press `Win + R`, type `appwiz.cpl`, press Enter

2. **Find Python 3.13**
   - Look for "Python 3.13.x" entries

3. **Uninstall**
   - Right-click → **Uninstall**
   - Follow the prompts

## Option 3: Use Python Installer to Uninstall

1. **Download Python 3.13 Installer Again**
   - Go to: https://www.python.org/downloads/
   - Download the same version you installed

2. **Run Installer**
   - Run the installer
   - Select **"Uninstall"** option
   - Follow the prompts

## Option 4: Manual Removal (Advanced - Not Recommended)

⚠️ **Warning:** Manual removal can leave registry entries and break things.

### Steps

1. **Remove Python Directory**
   ```powershell
   # Find Python 3.13 location
   py -3.13 -c "import sys; print(sys.executable)"
   
   # Remove directory (usually)
   Remove-Item -Recurse -Force "C:\Users\ctrpr\AppData\Local\Programs\Python\Python313"
   ```

2. **Remove from PATH**
   - Open **System Properties** → **Environment Variables**
   - Edit **Path** variable
   - Remove Python 3.13 entries:
     - `C:\Users\ctrpr\AppData\Local\Programs\Python\Python313\`
     - `C:\Users\ctrpr\AppData\Local\Programs\Python\Python313\Scripts\`

3. **Remove Registry Entries** (Advanced)
   ```powershell
   # Remove from user registry
   Remove-Item -Recurse -Force "HKCU:\Software\Python\PythonCore\3.13*" -ErrorAction SilentlyContinue
   ```

## Verify Removal

After uninstalling:

```powershell
# Check if Python 3.13 is still available
py -3.13 --version
# Should show: "Python was not found"

# Check all Python versions
py -0p
# Should not show Python 3.13
```

## After Removal

1. **Install Python 3.12** (if you want system-wide)
   - Download from: https://www.python.org/downloads/release/python-3120/
   - Or use the local setup script (recommended)

2. **Or Use Local Python 3.12**
   ```powershell
   cd C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk
   .\setup-local-python.ps1
   ```

## Recommended Approach

**Don't remove Python 3.13** - just use Python 3.12 locally for CDK:

```powershell
cd C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk

# This installs Python 3.12 locally, doesn't touch Python 3.13
.\setup-local-python.ps1

# Use the local Python 3.12 for CDK
.venv-cdk\Scripts\Activate.ps1
python --version  # Shows 3.12.0
cdk synth
```

This way:
- ✅ Python 3.13 stays for other projects
- ✅ Python 3.12 is available for CDK
- ✅ No conflicts
- ✅ Easy to manage

## Troubleshooting

### Issue: "Python 3.13 still appears after uninstall"

**Solution:**
1. Restart your computer
2. Check if multiple Python 3.13 installations exist
3. Remove from PATH manually

### Issue: "Other projects break after removing Python 3.13"

**Solution:**
1. Reinstall Python 3.13
2. Or update those projects to use Python 3.12
3. Or use virtual environments for each project

### Issue: "Can't find Python 3.13 in Apps list"

**Solution:**
- It might be installed via Microsoft Store
- Check Microsoft Store → My Library
- Or use Control Panel method

---

**Recommendation:** Keep Python 3.13 and use local Python 3.12 for CDK. This is the safest approach.
