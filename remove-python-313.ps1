# remove-python-313.ps1
# Safely uninstall Python 3.13 from Windows

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  Python 3.13 Uninstaller" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "⚠️  This script requires Administrator privileges." -ForegroundColor Yellow
    Write-Host "   Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "Continue anyway? (y/n)"
    if ($response -ne "y" -and $response -ne "Y") {
        exit 0
    }
}

# Find Python 3.13 components
Write-Host "🔍 Searching for Python 3.13 components..." -ForegroundColor Cyan

$pythonComponents = Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | 
    Where-Object { $_.DisplayName -like "*Python 3.13*" }

if ($pythonComponents.Count -eq 0) {
    Write-Host "✅ No Python 3.13 components found in registry." -ForegroundColor Green
    Write-Host "   Python 3.13 may already be uninstalled or installed differently." -ForegroundColor Yellow
    exit 0
}

Write-Host "   Found $($pythonComponents.Count) Python 3.13 components:" -ForegroundColor White
foreach ($component in $pythonComponents) {
    Write-Host "   - $($component.DisplayName)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "⚠️  WARNING: This will uninstall Python 3.13 completely." -ForegroundColor Red
Write-Host "   Make sure no other projects depend on Python 3.13." -ForegroundColor Yellow
Write-Host ""
$confirm = Read-Host "Are you sure you want to continue? (type 'yes' to confirm)"

if ($confirm -ne "yes") {
    Write-Host "❌ Uninstallation cancelled." -ForegroundColor Yellow
    exit 0
}

# Uninstall each component
Write-Host ""
Write-Host "🗑️  Uninstalling Python 3.13 components..." -ForegroundColor Cyan

$uninstalled = 0
$failed = 0

foreach ($component in $pythonComponents) {
    $name = $component.DisplayName
    $uninstallString = $component.UninstallString
    
    Write-Host "   Uninstalling: $name" -ForegroundColor White
    
    try {
        # Extract the uninstall command
        if ($uninstallString -match '^(.+\.exe)\s+(.+)$') {
            $exe = $matches[1]
            $args = $matches[2]
            
            # Run uninstall silently
            $process = Start-Process -FilePath $exe -ArgumentList $args, "/quiet", "/norestart" -Wait -PassThru -NoNewWindow
            
            if ($process.ExitCode -eq 0) {
                Write-Host "   ✅ Uninstalled: $name" -ForegroundColor Green
                $uninstalled++
            } else {
                Write-Host "   ⚠️  Exit code: $($process.ExitCode) for: $name" -ForegroundColor Yellow
                $failed++
            }
        } else {
            Write-Host "   ⚠️  Could not parse uninstall string: $uninstallString" -ForegroundColor Yellow
            $failed++
        }
    } catch {
        Write-Host "   ❌ Failed to uninstall: $name" -ForegroundColor Red
        Write-Host "      Error: $_" -ForegroundColor Gray
        $failed++
    }
}

# Remove Python directory if it exists
$pythonDir = "C:\Users\ctrpr\AppData\Local\Programs\Python\Python313"
if (Test-Path $pythonDir) {
    Write-Host ""
    Write-Host "🗑️  Removing Python 3.13 directory..." -ForegroundColor Cyan
    try {
        Remove-Item -Recurse -Force $pythonDir -ErrorAction Stop
        Write-Host "   ✅ Removed: $pythonDir" -ForegroundColor Green
    } catch {
        Write-Host "   ⚠️  Could not remove directory (may be in use): $pythonDir" -ForegroundColor Yellow
        Write-Host "      You may need to remove it manually after restarting." -ForegroundColor Yellow
    }
}

# Remove from PATH (User)
Write-Host ""
Write-Host "🔧 Cleaning up PATH environment variable..." -ForegroundColor Cyan

$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
$pathEntries = $userPath -split ';'
$newPathEntries = $pathEntries | Where-Object { 
    $_ -notlike "*Python313*" -and 
    $_ -notlike "*Python\Python313*"
}

if ($newPathEntries.Count -lt $pathEntries.Count) {
    $newPath = $newPathEntries -join ';'
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "   ✅ Removed Python 3.13 from PATH" -ForegroundColor Green
} else {
    Write-Host "   ℹ️  No Python 3.13 entries found in PATH" -ForegroundColor Gray
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Uninstallation Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Uninstalled: $uninstalled components" -ForegroundColor Green
if ($failed -gt 0) {
    Write-Host "   Failed: $failed components" -ForegroundColor Red
}
Write-Host ""

# Verify
Write-Host "🔍 Verifying removal..." -ForegroundColor Cyan
$remaining = Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | 
    Where-Object { $_.DisplayName -like "*Python 3.13*" }

if ($remaining.Count -eq 0) {
    Write-Host "   ✅ Python 3.13 successfully removed!" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Some components may still be installed:" -ForegroundColor Yellow
    foreach ($item in $remaining) {
        Write-Host "      - $($item.DisplayName)" -ForegroundColor Gray
    }
    Write-Host "   You may need to uninstall them manually from Settings → Apps" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "💡 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Restart your computer (recommended)" -ForegroundColor White
Write-Host "   2. Install Python 3.12 for CDK:" -ForegroundColor White
Write-Host "      cd infrastructure\aws-cdk" -ForegroundColor Gray
Write-Host "      .\setup-local-python.ps1" -ForegroundColor Gray
Write-Host ""
