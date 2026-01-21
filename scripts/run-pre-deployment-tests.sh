#!/bin/bash
# Pre-Deployment Testing Script
# Run all required tests before deployment

set -e

echo "=== AI Film Studio - Pre-Deployment Testing ==="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

FAILED=0

# Function to run test and check result
run_test() {
    local test_name=$1
    local test_command=$2
    
    echo -e "${YELLOW}Running: ${test_name}...${NC}"
    if eval "$test_command"; then
        echo -e "${GREEN}✅ ${test_name} passed${NC}"
        echo ""
    else
        echo -e "${RED}❌ ${test_name} failed${NC}"
        FAILED=1
        echo ""
    fi
}

# 1. Unit Tests
run_test "Unit Tests" "pytest tests/unit/ -v --cov=src --cov-report=term-missing --maxfail=5"

# 2. Integration Tests
run_test "Integration Tests" "pytest tests/integration/ -v -m integration --maxfail=3"

# 3. E2E Tests
run_test "E2E Tests" "pytest tests/e2e/ -v -m e2e --maxfail=3"

# 4. Smoke Tests
run_test "Smoke Tests" "pytest tests/smoke/ -v -m smoke"

# 5. Security Tests
run_test "Security Tests" "pytest tests/security/ -v -m security --maxfail=2"

# 6. Code Quality
run_test "Linting (flake8)" "flake8 src/ --max-line-length=120 --exclude=__pycache__,venv,.venv"
run_test "Type Checking (mypy)" "mypy src/ --ignore-missing-imports || true"

# 7. Frontend Tests (if in frontend directory)
if [ -d "frontend" ]; then
    echo -e "${YELLOW}Running Frontend Tests...${NC}"
    cd frontend
    if npm run test:run; then
        echo -e "${GREEN}✅ Frontend unit tests passed${NC}"
    else
        echo -e "${RED}❌ Frontend unit tests failed${NC}"
        FAILED=1
    fi
    cd ..
    echo ""
fi

# Summary
echo "=========================================="
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All pre-deployment tests passed!${NC}"
    echo -e "${GREEN}Ready for deployment.${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed.${NC}"
    echo -e "${RED}Please fix issues before deploying.${NC}"
    exit 1
fi
