#!/bin/bash
# AWS CloudShell Setup Script for AI Film Studio Amplify Deployment
# Run this script in AWS CloudShell to configure Amplify from CLI

set -e

echo "================================================"
echo "AI Film Studio - AWS Amplify CloudShell Setup"
echo "================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration variables
GITHUB_REPO="AI-Empower-HQ-360/AI-Film-Studio"
APP_NAME="ai-film-studio-frontend"
REGION="us-east-1"

echo -e "${YELLOW}Step 1: Checking AWS CLI version...${NC}"
aws --version

echo -e "${YELLOW}Step 2: Verifying AWS credentials...${NC}"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo -e "${GREEN}✓ AWS Account ID: $AWS_ACCOUNT_ID${NC}"

echo ""
echo -e "${YELLOW}Step 3: Creating Amplify Service Role (if not exists)...${NC}"

# Check if role exists
if aws iam get-role --role-name amplifyconsole-backend-role 2>/dev/null; then
    echo -e "${GREEN}✓ Role amplifyconsole-backend-role already exists${NC}"
else
    echo "Creating role..."
    
    # Create trust policy
    cat > /tmp/amplify-trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "amplify.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

    # Create role
    aws iam create-role \
        --role-name amplifyconsole-backend-role \
        --assume-role-policy-document file:///tmp/amplify-trust-policy.json \
        --description "Service role for AWS Amplify"
    
    # Attach policy
    aws iam attach-role-policy \
        --role-name amplifyconsole-backend-role \
        --policy-arn arn:aws:iam::aws:policy/AdministratorAccess-Amplify
    
    echo -e "${GREEN}✓ Role created and policy attached${NC}"
fi

echo ""
echo -e "${YELLOW}Step 4: Checking for existing Amplify app...${NC}"

# Check if app exists
APP_ID=$(aws amplify list-apps --region $REGION --query "apps[?name=='$APP_NAME'].appId" --output text)

if [ -z "$APP_ID" ]; then
    echo -e "${RED}✗ Amplify app not found${NC}"
    echo ""
    echo "To create the app, you need a GitHub personal access token."
    echo "Generate one at: https://github.com/settings/tokens"
    echo "Required scopes: repo, admin:repo_hook"
    echo ""
    read -p "Enter GitHub personal access token: " GITHUB_TOKEN
    
    if [ -z "$GITHUB_TOKEN" ]; then
        echo -e "${RED}✗ Token required. Exiting.${NC}"
        exit 1
    fi
    
    echo ""
    echo "Creating Amplify app..."
    
    APP_ID=$(aws amplify create-app \
        --name "$APP_NAME" \
        --repository "https://github.com/$GITHUB_REPO" \
        --access-token "$GITHUB_TOKEN" \
        --iam-service-role-arn "arn:aws:iam::$AWS_ACCOUNT_ID:role/amplifyconsole-backend-role" \
        --region $REGION \
        --platform WEB \
        --query 'app.appId' \
        --output text)
    
    echo -e "${GREEN}✓ Amplify app created: $APP_ID${NC}"
else
    echo -e "${GREEN}✓ Amplify app exists: $APP_ID${NC}"
fi

echo ""
echo -e "${YELLOW}Step 5: Configuring environment variables...${NC}"

# Set environment variables
aws amplify update-app \
    --app-id "$APP_ID" \
    --region $REGION \
    --environment-variables \
        NODE_VERSION=18 \
        NEXT_PUBLIC_API_URL=https://api.aifilmstudio.com \
        NEXT_PUBLIC_WS_URL=wss://api.aifilmstudio.com \
        NEXT_PUBLIC_ENV=production \
        NEXT_PUBLIC_ENABLE_ANALYTICS=true \
        NEXT_PUBLIC_ENABLE_VIDEO_GENERATION=true \
        NEXT_PUBLIC_ENABLE_VOICE_SYNTHESIS=true \
        NEXT_PUBLIC_ENABLE_LIPSYNC=true \
        NEXT_PUBLIC_ENABLE_MUSIC_GENERATION=true \
        NEXT_PUBLIC_ENABLE_PODCAST_VIDEO=true \
        NEXT_PUBLIC_ENABLE_SUBTITLE_GENERATION=true

echo -e "${GREEN}✓ Environment variables configured${NC}"

echo ""
echo -e "${YELLOW}Step 6: Connecting branches...${NC}"

# Function to connect branch
connect_branch() {
    local BRANCH_NAME=$1
    local ENV_NAME=$2
    local API_URL=$3
    
    echo "Connecting branch: $BRANCH_NAME"
    
    # Check if branch exists
    BRANCH_EXISTS=$(aws amplify list-branches \
        --app-id "$APP_ID" \
        --region $REGION \
        --query "branches[?branchName=='$BRANCH_NAME'].branchName" \
        --output text)
    
    if [ -z "$BRANCH_EXISTS" ]; then
        aws amplify create-branch \
            --app-id "$APP_ID" \
            --branch-name "$BRANCH_NAME" \
            --region $REGION \
            --enable-auto-build \
            --environment-variables \
                NEXT_PUBLIC_ENV=$ENV_NAME \
                NEXT_PUBLIC_API_URL=$API_URL \
                NEXT_PUBLIC_WS_URL="${API_URL/https/wss}"
        
        echo -e "${GREEN}✓ Branch $BRANCH_NAME connected${NC}"
    else
        echo -e "${GREEN}✓ Branch $BRANCH_NAME already connected${NC}"
    fi
}

# Connect main branch
connect_branch "main" "production" "https://api-prod.aifilmstudio.com"

# Connect other branches
connect_branch "staging" "staging" "https://api-staging.aifilmstudio.com"
connect_branch "sandbox" "sandbox" "https://api-sandbox.aifilmstudio.com"
connect_branch "dev" "development" "https://api-dev.aifilmstudio.com"

echo ""
echo -e "${YELLOW}Step 7: Starting initial deployment...${NC}"

aws amplify start-job \
    --app-id "$APP_ID" \
    --branch-name "main" \
    --job-type RELEASE \
    --region $REGION

echo -e "${GREEN}✓ Deployment started${NC}"

echo ""
echo "================================================"
echo -e "${GREEN}Setup Complete!${NC}"
echo "================================================"
echo ""
echo "App ID: $APP_ID"
echo "Console URL: https://console.aws.amazon.com/amplify/home?region=$REGION#/$APP_ID"
echo ""
echo "Branch URLs will be available after deployment:"
echo "  main:    https://main.$APP_ID.amplifyapp.com"
echo "  staging: https://staging.$APP_ID.amplifyapp.com"
echo "  sandbox: https://sandbox.$APP_ID.amplifyapp.com"
echo "  dev:     https://dev.$APP_ID.amplifyapp.com"
echo ""
echo "Monitor deployment:"
echo "  aws amplify list-jobs --app-id $APP_ID --branch-name main --region $REGION"
echo ""
