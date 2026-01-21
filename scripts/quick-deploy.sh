#!/bin/bash
# Quick Deploy to AWS Amplify with Pre-configured Tokens
# This script uses your GitHub token to deploy

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}================================================${NC}"
echo -e "${YELLOW}  Quick AWS Amplify Deployment Setup${NC}"
echo -e "${YELLOW}================================================${NC}"
echo ""

# Check if AWS CLI is authenticated
echo "Checking AWS authentication..."
if aws sts get-caller-identity &> /dev/null; then
    echo -e "${GREEN}✅ AWS credentials configured${NC}"
    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    AWS_USER=$(aws sts get-caller-identity --query Arn --output text)
    echo "   Account: $AWS_ACCOUNT_ID"
    echo "   User: $AWS_USER"
else
    echo -e "${RED}❌ AWS credentials not configured${NC}"
    echo ""
    echo "Please configure AWS credentials first:"
    echo ""
    echo "  aws configure"
    echo ""
    echo "You'll need:"
    echo "  - AWS Access Key ID"
    echo "  - AWS Secret Access Key"
    echo "  - Default region: us-east-1"
    echo ""
    echo -e "${YELLOW}📖 Full guide: docs/deployment/AWS_CREDENTIALS_GUIDE.md${NC}"
    echo ""
    read -p "Press Enter to configure now, or Ctrl+C to exit..."
    aws configure
    
    if ! aws sts get-caller-identity &> /dev/null; then
        echo -e "${RED}❌ Configuration failed. Please try again.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ AWS credentials configured successfully${NC}"
fi

echo ""
echo -e "${GREEN}Ready to deploy to AWS Amplify!${NC}"
echo ""
echo "Run the full deployment script:"
echo "  ./scripts/deploy-to-amplify.sh"
echo ""
