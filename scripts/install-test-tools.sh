#!/bin/bash
# Install Testing Tools for AI Film Studio
# This script installs all required testing tools for backend and frontend

set -e

echo "=== AI Film Studio - Testing Tools Installation ==="
echo ""

# Backend Testing Tools
echo "📦 Installing Backend Testing Tools..."
cd "$(dirname "$0")/.."

# Install Python testing tools
pip install -r tests/requirements-test.txt

# Install additional backend tools
pip install pytest-xdist pytest-html freezegun pytest-benchmark pytest-json-report ruff

echo "✅ Backend testing tools installed"
echo ""

# Frontend Testing Tools
echo "📦 Installing Frontend Testing Tools..."
cd frontend

# Install npm packages
npm install

# Install Playwright browsers
npx playwright install --with-deps

echo "✅ Frontend testing tools installed"
echo ""

echo "🎉 All testing tools installed successfully!"
echo ""
echo "Next steps:"
echo "  Backend:  pytest tests/ -v"
echo "  Frontend: npm test"
echo "  E2E:      npm run test:e2e"
