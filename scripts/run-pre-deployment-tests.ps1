# Pre-Deployment Testing Script (PowerShell)
# Run all required tests before deployment

$ErrorActionPreference = "Stop"

Write-Host "=== AI Film Studio - Pre-Deployment Testing ===" -ForegroundColor Cyan
Write-Host ""

$Failed = 0

function Run-Test {
    param(
        [string]$TestName,
        [string]$TestCommand
    )
    
    Write-Host "Running: $TestName..." -ForegroundColor Yellow
    try {
        Invoke-Expression $TestCommand
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ $TestName passed" -ForegroundColor Green
            Write-Host ""
        } else {
            Write-Host "❌ $TestName failed" -ForegroundColor Red
            $script:Failed = 1
            Write-Host ""
        }
    } catch {
        Write-Host "❌ $TestName failed: $_" -ForegroundColor Red
        $script:Failed = 1
        Write-Host ""
    }
}

# 1. Unit Tests
Run-Test "Unit Tests" "pytest tests/unit/ -v --cov=src --cov-report=term-missing --maxfail=5"

# 2. Integration Tests
Run-Test "Integration Tests" "pytest tests/integration/ -v -m integration --maxfail=3"

# 3. E2E Tests
Run-Test "E2E Tests" "pytest tests/e2e/ -v -m e2e --maxfail=3"

# 4. Smoke Tests
Run-Test "Smoke Tests" "pytest tests/smoke/ -v -m smoke"

# 5. Security Tests
Run-Test "Security Tests" "pytest tests/security/ -v -m security --maxfail=2"

# 6. Code Quality
Run-Test "Linting (flake8)" "flake8 src/ --max-line-length=120 --exclude=__pycache__,venv,.venv"
Run-Test "Type Checking (mypy)" "mypy src/ --ignore-missing-imports"

# 7. Frontend Tests
if (Test-Path "frontend") {
    Write-Host "Running Frontend Tests..." -ForegroundColor Yellow
    Push-Location frontend
    try {
        npm run test:run
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Frontend unit tests passed" -ForegroundColor Green
        } else {
            Write-Host "❌ Frontend unit tests failed" -ForegroundColor Red
            $Failed = 1
        }
    } catch {
        Write-Host "❌ Frontend tests failed: $_" -ForegroundColor Red
        $Failed = 1
    }
    Pop-Location
    Write-Host ""
}

# Summary
Write-Host "=========================================="
if ($Failed -eq 0) {
    Write-Host "🎉 All pre-deployment tests passed!" -ForegroundColor Green
    Write-Host "Ready for deployment." -ForegroundColor Green
    exit 0
} else {
    Write-Host "❌ Some tests failed." -ForegroundColor Red
    Write-Host "Please fix issues before deploying." -ForegroundColor Red
    exit 1
}
