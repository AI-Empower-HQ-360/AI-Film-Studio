#!/bin/bash
# Test Script for Cline AI Extension
# Tests various Cline functionality

echo "=== Cline AI Extension Test Suite ==="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test 1: Check if Cline extension is installed
echo -e "${YELLOW}Test 1: Checking Cline extension installation...${NC}"
if code --list-extensions | grep -i "cline" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Cline extension is installed${NC}"
else
    echo -e "${RED}❌ Cline extension not found${NC}"
    echo "Install with: code --install-extension [cline-extension-id]"
fi
echo ""

# Test 2: Check configuration
echo -e "${YELLOW}Test 2: Checking Cline configuration...${NC}"
if [ -f ".vscode/settings.json" ]; then
    if grep -q "cline" .vscode/settings.json; then
        echo -e "${GREEN}✅ Cline configuration found${NC}"
    else
        echo -e "${YELLOW}⚠️  No Cline settings in .vscode/settings.json${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  No .vscode/settings.json found${NC}"
fi
echo ""

# Test 3: Check API key (if in env)
echo -e "${YELLOW}Test 3: Checking API key configuration...${NC}"
if [ -n "$CLINE_API_KEY" ] || [ -n "$OPENAI_API_KEY" ] || [ -n "$ANTHROPIC_API_KEY" ]; then
    echo -e "${GREEN}✅ API key environment variable found${NC}"
else
    echo -e "${YELLOW}⚠️  No API key in environment variables${NC}"
    echo "Set: export CLINE_API_KEY=your-key"
fi
echo ""

# Test 4: Check project structure (for context awareness)
echo -e "${YELLOW}Test 4: Checking project structure...${NC}"
if [ -d "src" ] && [ -d "tests" ]; then
    echo -e "${GREEN}✅ Project structure detected${NC}"
    echo "  - Source code: src/"
    echo "  - Tests: tests/"
else
    echo -e "${YELLOW}⚠️  Project structure may not be optimal for Cline${NC}"
fi
echo ""

# Test 5: Sample code file for testing
echo -e "${YELLOW}Test 5: Creating test file for Cline...${NC}"
TEST_FILE="test_cline_generation.py"
cat > "$TEST_FILE" << 'EOF'
# Cline Test File
# Try asking Cline to generate a function here

# TODO: Ask Cline to generate a function that validates email addresses

# TODO: Ask Cline to explain the code below
def example_function(x: int, y: int) -> int:
    return x + y

EOF
echo -e "${GREEN}✅ Test file created: $TEST_FILE${NC}"
echo "Open this file and test Cline's code generation"
echo ""

# Summary
echo "=========================================="
echo -e "${GREEN}Test suite complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Open $TEST_FILE in Cursor/VS Code"
echo "2. Try Cline's code generation features"
echo "3. Test code completion and explanation"
echo "4. Verify refactoring suggestions"
echo ""
