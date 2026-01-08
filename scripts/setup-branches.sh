#!/bin/bash

# Environment Branches Setup Script
# This script creates the environment branches for AI Film Studio

set -e  # Exit on error

echo "🌿 AI Film Studio - Environment Branches Setup"
echo "=============================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}Error: Not in a git repository${NC}"
    exit 1
fi

# Check if we're in the right repository
REPO_NAME=$(basename `git rev-parse --show-toplevel`)
if [ "$REPO_NAME" != "AI-Film-Studio" ]; then
    echo -e "${YELLOW}Warning: Repository name is '$REPO_NAME', expected 'AI-Film-Studio'${NC}"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo -e "${BLUE}Step 1: Fetching latest changes from remote...${NC}"
git fetch origin

echo -e "${BLUE}Step 2: Checking out main branch...${NC}"
git checkout main
git pull origin main

echo -e "${BLUE}Step 3: Creating environment branches...${NC}"
echo ""

# Array of branches to create
BRANCHES=("dev" "sandbox" "staging")

for BRANCH in "${BRANCHES[@]}"; do
    echo -e "${YELLOW}Creating branch: $BRANCH${NC}"
    
    # Check if branch already exists locally
    if git show-ref --verify --quiet refs/heads/$BRANCH; then
        echo -e "${YELLOW}  Branch '$BRANCH' already exists locally, skipping creation${NC}"
    else
        git checkout -b $BRANCH main
        echo -e "${GREEN}  ✓ Created local branch '$BRANCH'${NC}"
    fi
    
    # Check if branch exists on remote
    if git ls-remote --heads origin $BRANCH | grep -q $BRANCH; then
        echo -e "${YELLOW}  Branch '$BRANCH' already exists on remote${NC}"
    else
        echo -e "${BLUE}  Pushing '$BRANCH' to remote...${NC}"
        git push -u origin $BRANCH
        echo -e "${GREEN}  ✓ Pushed '$BRANCH' to remote${NC}"
    fi
    
    echo ""
done

echo -e "${BLUE}Step 4: Returning to main branch...${NC}"
git checkout main

echo -e "${BLUE}Step 5: Verifying branches...${NC}"
echo ""
echo "Local branches:"
git branch
echo ""
echo "Remote branches:"
git branch -r | grep -E "(dev|sandbox|staging|main)"
echo ""

echo -e "${GREEN}✓ Environment branches setup complete!${NC}"
echo ""
echo "Branches created:"
echo "  • dev      - Development environment"
echo "  • sandbox  - Testing/QA environment"
echo "  • staging  - Pre-production environment"
echo "  • main     - Production environment (already exists)"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Configure branch protection rules (see docs/BRANCH_SETUP_GUIDE.md)"
echo "2. Set up GitHub environments with secrets (see docs/BRANCH_SETUP_GUIDE.md)"
echo "3. Create CODEOWNERS file (see docs/BRANCH_SETUP_GUIDE.md)"
echo "4. Train team on branching strategy (see docs/BRANCHING_STRATEGY.md)"
echo ""
echo "For detailed instructions, see: docs/BRANCH_SETUP_GUIDE.md"
