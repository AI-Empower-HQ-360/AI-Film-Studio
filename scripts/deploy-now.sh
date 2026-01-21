#!/bin/bash
# Automated Amplify Deployment with Pre-configured Credentials
# AI Film Studio

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
GITHUB_TOKEN="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"
APP_NAME="ai-film-studio-frontend"
GITHUB_REPO="AI-Empower-HQ-360/AI-Film-Studio"
REGION="us-east-1"
ROLE_NAME="amplifyconsole-backend-role"

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}   AI Film Studio - Amplify Deployment${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Verify AWS authentication
echo -e "${YELLOW}Verifying AWS credentials...${NC}"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_USER=$(aws sts get-caller-identity --query Arn --output text)
echo -e "${GREEN}✅ Authenticated${NC}"
echo "   Account: $AWS_ACCOUNT_ID"
echo "   User: $AWS_USER"
echo ""

# Create IAM Role
echo -e "${YELLOW}Creating IAM service role...${NC}"
if aws iam get-role --role-name $ROLE_NAME 2>/dev/null >/dev/null; then
    echo -e "${GREEN}✅ Role already exists${NC}"
else
    cat > /tmp/amplify-trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Service": "amplify.amazonaws.com"},
    "Action": "sts:AssumeRole"
  }]
}
EOF

    aws iam create-role \
        --role-name $ROLE_NAME \
        --assume-role-policy-document file:///tmp/amplify-trust-policy.json \
        --description "Service role for AWS Amplify" 2>/dev/null
    
    aws iam attach-role-policy \
        --role-name $ROLE_NAME \
        --policy-arn arn:aws:iam::aws:policy/AdministratorAccess-Amplify 2>/dev/null
    
    echo -e "${GREEN}✅ Role created${NC}"
    sleep 5  # Wait for role to propagate
fi

ROLE_ARN="arn:aws:iam::$AWS_ACCOUNT_ID:role/$ROLE_NAME"
echo ""

# Create/Get Amplify App
echo -e "${YELLOW}Setting up Amplify app...${NC}"
APP_ID=$(aws amplify list-apps --region $REGION --query "apps[?name=='$APP_NAME'].appId" --output text 2>/dev/null)

if [ -z "$APP_ID" ]; then
    echo "Creating new app..."
    APP_ID=$(aws amplify create-app \
        --name "$APP_NAME" \
        --repository "https://github.com/$GITHUB_REPO" \
        --access-token "$GITHUB_TOKEN" \
        --iam-service-role-arn "$ROLE_ARN" \
        --region $REGION \
        --platform WEB \
        --enable-auto-branch-creation \
        --query 'app.appId' \
        --output text 2>/dev/null)
    echo -e "${GREEN}✅ App created: $APP_ID${NC}"
else
    echo -e "${GREEN}✅ Using existing app: $APP_ID${NC}"
fi
echo ""

# Configure environment variables
echo -e "${YELLOW}Configuring environment variables...${NC}"
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
        2>/dev/null >/dev/null

echo -e "${GREEN}✅ Environment variables configured${NC}"
echo ""

# Connect branches
echo -e "${YELLOW}Connecting branches...${NC}"

connect_branch() {
    local BRANCH_NAME=$1
    local ENV_NAME=$2
    local API_URL=$3
    
    if aws amplify get-branch --app-id "$APP_ID" --branch-name "$BRANCH_NAME" --region $REGION 2>/dev/null >/dev/null; then
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
                2>/dev/null >/dev/null || true
        
        echo "  ✓ $BRANCH_NAME (connected)"
    fi
}

connect_branch "main" "production" "https://api-prod.aifilmstudio.com"
connect_branch "staging" "staging" "https://api-staging.aifilmstudio.com"
connect_branch "sandbox" "sandbox" "https://api-sandbox.aifilmstudio.com"
connect_branch "dev" "development" "https://api-dev.aifilmstudio.com"

echo ""

# Start deployment
echo -e "${YELLOW}Starting deployment...${NC}"
JOB_ID=$(aws amplify start-job \
    --app-id "$APP_ID" \
    --branch-name "main" \
    --job-type RELEASE \
    --region $REGION \
    --query 'jobSummary.jobId' \
    --output text 2>/dev/null)

echo -e "${GREEN}✅ Deployment started (Job #$JOB_ID)${NC}"
echo ""

# Summary
echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}           🎉 Deployment Started! 🎉${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""
echo -e "${GREEN}App ID:${NC} $APP_ID"
echo -e "${GREEN}Region:${NC} $REGION"
echo ""
echo -e "${YELLOW}🔗 Console URL:${NC}"
echo "https://console.aws.amazon.com/amplify/home?region=$REGION#/$APP_ID"
echo ""
echo -e "${YELLOW}🌐 Your App URLs (live in 3-5 minutes):${NC}"
echo "  Production: https://main.$APP_ID.amplifyapp.com"
echo "  Staging:    https://staging.$APP_ID.amplifyapp.com"
echo "  Sandbox:    https://sandbox.$APP_ID.amplifyapp.com"
echo "  Dev:        https://dev.$APP_ID.amplifyapp.com"
echo ""
echo -e "${YELLOW}📊 Monitor deployment:${NC}"
echo "aws amplify get-job --app-id $APP_ID --branch-name main --job-id $JOB_ID --region $REGION"
echo ""
echo -e "${GREEN}✨ Building your app now... Check the console for progress!${NC}"
echo ""
