# Install Testing Tools for AI Film Studio (PowerShell)
# This script installs all required testing tools for backend and frontend

Write-Host "=== AI Film Studio - Testing Tools Installation ===" -ForegroundColor Cyan
Write-Host ""

# Backend Testing Tools
Write-Host "📦 Installing Backend Testing Tools..." -ForegroundColor Yellow
Set-Location $PSScriptRoot\..

# Install Python testing tools
pip install -r tests\requirements-test.txt

# Install additional backend tools
pip install pytest-xdist pytest-html freezegun pytest-benchmark pytest-json-report ruff

Write-Host "✅ Backend testing tools installed" -ForegroundColor Green
Write-Host ""

# Frontend Testing Tools
Write-Host "📦 Installing Frontend Testing Tools..." -ForegroundColor Yellow
Set-Location frontend

# Install npm packages
npm install

# Install Playwright browsers
npx playwright install --with-deps

Write-Host "✅ Frontend testing tools installed" -ForegroundColor Green
Write-Host ""

Write-Host "🎉 All testing tools installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "  Backend:  pytest tests/ -v"
Write-Host "  Frontend: npm test"
Write-Host "  E2E:      npm run test:e2e"
