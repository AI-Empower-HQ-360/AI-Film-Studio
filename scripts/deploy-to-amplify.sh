#!/bin/bash
# Interactive AWS and Amplify Setup for Codespace
# This script will guide you through the entire setup process

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}   AI Film Studio - Amplify CLI Deployment${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Step 1: AWS Authentication
echo -e "${YELLOW}Step 1: AWS Authentication${NC}"
echo ""

if aws sts get-caller-identity &> /dev/null; then
    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    AWS_USER=$(aws sts get-caller-identity --query Arn --output text)
    echo -e "${GREEN}✅ Already authenticated with AWS${NC}"
    echo "   Account: $AWS_ACCOUNT_ID"
    echo "   User: $AWS_USER"
else
    echo -e "${YELLOW}⚠️  Not authenticated with AWS${NC}"
    echo ""
    echo "Please authenticate with AWS first:"
    echo ""
    echo "  Method 1 - Using AWS credentials:"
    echo "    aws configure"
    echo ""
    echo "  Method 2 - Using environment variables:"
    echo "    export AWS_ACCESS_KEY_ID='your-key'"
    echo "    export AWS_SECRET_ACCESS_KEY='your-secret'"
    echo "    export AWS_DEFAULT_REGION='us-east-1'"
    echo ""
    read -p "Press Enter after authenticating, or Ctrl+C to exit..."
    
    if ! aws sts get-caller-identity &> /dev/null; then
        echo -e "${RED}❌ Still not authenticated. Please run 'aws configure' first.${NC}"
        exit 1
    fi
fi

echo ""

# Step 2: GitHub Token
echo -e "${YELLOW}Step 2: GitHub Personal Access Token${NC}"
echo ""
echo "You need a GitHub token to connect your repository to Amplify."
echo "Generate one at: https://github.com/settings/tokens/new"
echo ""
echo "Required scopes:"
echo "  ✓ repo (Full control of private repositories)"
echo "  ✓ admin:repo_hook (Full control of repository hooks)"
echo ""
read -sp "Enter your GitHub token (input hidden): " GITHUB_TOKEN
echo ""

if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${RED}❌ GitHub token is required${NC}"
    exit 1
fi

echo -e "${GREEN}✅ GitHub token received${NC}"
echo ""

# Step 3: Configuration
echo -e "${YELLOW}Step 3: Configuration${NC}"
echo ""

# Set defaults
APP_NAME="ai-film-studio-frontend"
GITHUB_REPO="AI-Empower-HQ-360/AI-Film-Studio"
REGION="us-east-1"

echo "App Name: $APP_NAME"
echo "GitHub Repo: $GITHUB_REPO"
echo "AWS Region: $REGION"
echo ""

read -p "Use these defaults? (Y/n): " USE_DEFAULTS
USE_DEFAULTS=${USE_DEFAULTS:-Y}

if [[ ! $USE_DEFAULTS =~ ^[Yy]$ ]]; then
    read -p "Enter App Name [$APP_NAME]: " INPUT_APP_NAME
    APP_NAME=${INPUT_APP_NAME:-$APP_NAME}
    
    read -p "Enter GitHub Repo [$GITHUB_REPO]: " INPUT_REPO
    GITHUB_REPO=${INPUT_REPO:-$GITHUB_REPO}
    
    read -p "Enter AWS Region [$REGION]: " INPUT_REGION
    REGION=${INPUT_REGION:-$REGION}
fi

echo ""

# Step 4: Create IAM Role
echo -e "${YELLOW}Step 4: Creating IAM Service Role${NC}"
echo ""

ROLE_NAME="amplifyconsole-backend-role"

if aws iam get-role --role-name $ROLE_NAME &> /dev/null; then
    echo -e "${GREEN}✅ Role already exists: $ROLE_NAME${NC}"
else
    echo "Creating IAM role..."
    
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

    aws iam create-role \
        --role-name $ROLE_NAME \
        --assume-role-policy-document file:///tmp/amplify-trust-policy.json \
        --description "Service role for AWS Amplify" \
        --region $REGION
    
    aws iam attach-role-policy \
        --role-name $ROLE_NAME \
        --policy-arn arn:aws:iam::aws:policy/AdministratorAccess-Amplify \
        --region $REGION
    
    echo -e "${GREEN}✅ Role created: $ROLE_NAME${NC}"
fi

AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ROLE_ARN="arn:aws:iam::$AWS_ACCOUNT_ID:role/$ROLE_NAME"

echo ""

# Step 5: Create or Get Amplify App
echo -e "${YELLOW}Step 5: Creating Amplify App${NC}"
echo ""

APP_ID=$(aws amplify list-apps --region $REGION --query "apps[?name=='$APP_NAME'].appId" --output text)

if [ -z "$APP_ID" ]; then
    echo "Creating new Amplify app..."
    
    APP_ID=$(aws amplify create-app \
        --name "$APP_NAME" \
        --repository "https://github.com/$GITHUB_REPO" \
        --access-token "$GITHUB_TOKEN" \
        --iam-service-role-arn "$ROLE_ARN" \
        --region $REGION \
        --platform WEB \
        --enable-auto-branch-creation \
        --query 'app.appId' \
        --output text)
    
    echo -e "${GREEN}✅ Amplify app created: $APP_ID${NC}"
else
    echo -e "${GREEN}✅ Using existing Amplify app: $APP_ID${NC}"
fi

echo ""

# Step 6: Configure Environment Variables
echo -e "${YELLOW}Step 6: Configuring Environment Variables${NC}"
echo ""

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
        NEXT_PUBLIC_ENABLE_SUBTITLE_GENERATION=true \
        > /dev/null

echo -e "${GREEN}✅ Environment variables configured${NC}"
echo ""

# Step 7: Connect Branches
echo -e "${YELLOW}Step 7: Connecting Branches${NC}"
echo ""

connect_branch() {
    local BRANCH_NAME=$1
    local ENV_NAME=$2
    local API_URL=$3
    
    if aws amplify get-branch --app-id "$APP_ID" --branch-name "$BRANCH_NAME" --region $REGION &> /dev/null; then
        echo "  ✓ $BRANCH_NAME (already connected)"
    else
        aws amplify create-branch \
            --app-id "$APP_ID" \
            --branch-name "$BRANCH_NAME" \
            --region $REGION \
            --enable-auto-build \
            --environment-variables \
                NEXT_PUBLIC_ENV=$ENV_NAME \
                NEXT_PUBLIC_API_URL=$API_URL \
                NEXT_PUBLIC_WS_URL="${API_URL/https/wss}" \
                > /dev/null
        
        echo "  ✓ $BRANCH_NAME (connected)"
    fi
}

connect_branch "main" "production" "https://api-prod.aifilmstudio.com"
connect_branch "staging" "staging" "https://api-staging.aifilmstudio.com"
connect_branch "sandbox" "sandbox" "https://api-sandbox.aifilmstudio.com"
connect_branch "dev" "development" "https://api-dev.aifilmstudio.com"

echo ""

# Step 8: Start Deployment
echo -e "${YELLOW}Step 8: Starting Initial Deployment${NC}"
echo ""

JOB_ID=$(aws amplify start-job \
    --app-id "$APP_ID" \
    --branch-name "main" \
    --job-type RELEASE \
    --region $REGION \
    --query 'jobSummary.jobId' \
    --output text)

echo -e "${GREEN}✅ Deployment started (Job ID: $JOB_ID)${NC}"
echo ""

# Summary
echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}           🎉 Setup Complete! 🎉${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""
echo -e "${GREEN}App ID:${NC} $APP_ID"
echo -e "${GREEN}Region:${NC} $REGION"
echo ""
echo -e "${YELLOW}Console URL:${NC}"
echo "  https://console.aws.amazon.com/amplify/home?region=$REGION#/$APP_ID"
echo ""
echo -e "${YELLOW}Branch URLs (available after deployment):${NC}"
echo "  main:    https://main.$APP_ID.amplifyapp.com"
echo "  staging: https://staging.$APP_ID.amplifyapp.com"
echo "  sandbox: https://sandbox.$APP_ID.amplifyapp.com"
echo "  dev:     https://dev.$APP_ID.amplifyapp.com"
echo ""
echo -e "${YELLOW}Monitor deployment:${NC}"
echo "  aws amplify get-job \\"
echo "    --app-id $APP_ID \\"
echo "    --branch-name main \\"
echo "    --job-id $JOB_ID \\"
echo "    --region $REGION"
echo ""
echo -e "${YELLOW}View build logs:${NC}"
echo "  aws logs tail /aws/amplify/$APP_ID/main --follow --region $REGION"
echo ""
echo -e "${GREEN}✨ Your app will be live in 3-5 minutes!${NC}"
echo ""
