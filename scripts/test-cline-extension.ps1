# Test Script for Cline AI Extension (PowerShell)
# Tests various Cline functionality

Write-Host "=== Cline AI Extension Test Suite ===" -ForegroundColor Cyan
Write-Host ""

# Test 1: Check if Cline extension is installed
Write-Host "Test 1: Checking Cline extension installation..." -ForegroundColor Yellow
try {
    $extensions = code --list-extensions 2>$null
    if ($extensions -match "cline") {
        Write-Host "✅ Cline extension is installed" -ForegroundColor Green
    } else {
        Write-Host "❌ Cline extension not found" -ForegroundColor Red
        Write-Host "Install with: code --install-extension [cline-extension-id]"
    }
} catch {
    Write-Host "⚠️  Could not check extensions (code command not found)" -ForegroundColor Yellow
}
Write-Host ""

# Test 2: Check configuration
Write-Host "Test 2: Checking Cline configuration..." -ForegroundColor Yellow
if (Test-Path ".vscode/settings.json") {
    $settings = Get-Content ".vscode/settings.json" -Raw
    if ($settings -match "cline") {
        Write-Host "✅ Cline configuration found" -ForegroundColor Green
    } else {
        Write-Host "⚠️  No Cline settings in .vscode/settings.json" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  No .vscode/settings.json found" -ForegroundColor Yellow
}
Write-Host ""

# Test 3: Check API key (if in env)
Write-Host "Test 3: Checking API key configuration..." -ForegroundColor Yellow
$hasApiKey = $env:CLINE_API_KEY -or $env:OPENAI_API_KEY -or $env:ANTHROPIC_API_KEY
if ($hasApiKey) {
    Write-Host "✅ API key environment variable found" -ForegroundColor Green
} else {
    Write-Host "⚠️  No API key in environment variables" -ForegroundColor Yellow
    Write-Host "Set: `$env:CLINE_API_KEY='your-key'"
}
Write-Host ""

# Test 4: Check project structure
Write-Host "Test 4: Checking project structure..." -ForegroundColor Yellow
if ((Test-Path "src") -and (Test-Path "tests")) {
    Write-Host "✅ Project structure detected" -ForegroundColor Green
    Write-Host "  - Source code: src/"
    Write-Host "  - Tests: tests/"
} else {
    Write-Host "⚠️  Project structure may not be optimal for Cline" -ForegroundColor Yellow
}
Write-Host ""

# Test 5: Create sample test file
Write-Host "Test 5: Creating test file for Cline..." -ForegroundColor Yellow
$testFile = "test_cline_generation.py"
$testContent = @"
# Cline Test File
# Try asking Cline to generate a function here

# TODO: Ask Cline to generate a function that validates email addresses

# TODO: Ask Cline to explain the code below
def example_function(x: int, y: int) -> int:
    return x + y
"@

Set-Content -Path $testFile -Value $testContent
Write-Host "✅ Test file created: $testFile" -ForegroundColor Green
Write-Host "Open this file and test Cline's code generation"
Write-Host ""

# Summary
Write-Host "=========================================="
Write-Host "Test suite complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Open $testFile in Cursor/VS Code"
Write-Host "2. Try Cline's code generation features"
Write-Host "3. Test code completion and explanation"
Write-Host "4. Verify refactoring suggestions"
Write-Host ""
