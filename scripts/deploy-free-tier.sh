#!/bin/bash
# Deploy AWS Free Tier Backend for AI Film Studio
# Creates Lambda + API Gateway + DynamoDB + S3

set -e

# Use correct AWS CLI path
alias aws='/usr/bin/aws'
export PATH="/usr/bin:$PATH"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}   AI Film Studio - AWS Free Tier Backend${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Get AWS Account ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=${AWS_REGION:-us-east-1}
PROJECT_NAME="ai-film-studio"

echo -e "${GREEN}✅ AWS Account: $AWS_ACCOUNT_ID${NC}"
echo -e "${GREEN}✅ Region: $AWS_REGION${NC}"
echo ""

# 1. Create S3 Bucket
echo -e "${YELLOW}Step 1: Creating S3 bucket...${NC}"
BUCKET_NAME="${PROJECT_NAME}-assets-${AWS_ACCOUNT_ID}"

if aws s3 ls "s3://${BUCKET_NAME}" 2>&1 | grep -q 'NoSuchBucket'; then
    aws s3 mb "s3://${BUCKET_NAME}" --region $AWS_REGION
    aws s3api put-bucket-cors --bucket $BUCKET_NAME --cors-configuration '{
        "CORSRules": [{
            "AllowedOrigins": ["https://ai-empower-hq-360.github.io", "http://localhost:3000"],
            "AllowedMethods": ["GET", "PUT", "POST"],
            "AllowedHeaders": ["*"],
            "MaxAgeSeconds": 3600
        }]
    }'
    echo -e "${GREEN}✅ S3 bucket created: ${BUCKET_NAME}${NC}"
else
    echo -e "${GREEN}✅ S3 bucket already exists${NC}"
fi
echo ""

# 2. Create DynamoDB Table
echo -e "${YELLOW}Step 2: Creating DynamoDB table...${NC}"
TABLE_NAME="${PROJECT_NAME}-projects"

if ! aws dynamodb describe-table --table-name $TABLE_NAME 2>/dev/null; then
    aws dynamodb create-table \
        --table-name $TABLE_NAME \
        --attribute-definitions \
            AttributeName=userId,AttributeType=S \
            AttributeName=projectId,AttributeType=S \
        --key-schema \
            AttributeName=userId,KeyType=HASH \
            AttributeName=projectId,KeyType=RANGE \
        --billing-mode PAY_PER_REQUEST \
        --region $AWS_REGION
    echo -e "${GREEN}✅ DynamoDB table created: ${TABLE_NAME}${NC}"
else
    echo -e "${GREEN}✅ DynamoDB table already exists${NC}"
fi
echo ""

# 3. Create IAM Role for Lambda
echo -e "${YELLOW}Step 3: Creating IAM role...${NC}"
ROLE_NAME="${PROJECT_NAME}-lambda-role"

if ! aws iam get-role --role-name $ROLE_NAME 2>/dev/null; then
    # Create trust policy
    cat > /tmp/trust-policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {"Service": "lambda.amazonaws.com"},
        "Action": "sts:AssumeRole"
    }]
}
EOF

    aws iam create-role \
        --role-name $ROLE_NAME \
        --assume-role-policy-document file:///tmp/trust-policy.json

    # Attach policies
    aws iam attach-role-policy \
        --role-name $ROLE_NAME \
        --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

    aws iam attach-role-policy \
        --role-name $ROLE_NAME \
        --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess

    aws iam attach-role-policy \
        --role-name $ROLE_NAME \
        --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

    echo -e "${GREEN}✅ IAM role created${NC}"
    echo "Waiting for role to propagate..."
    sleep 10
else
    echo -e "${GREEN}✅ IAM role already exists${NC}"
fi

ROLE_ARN="arn:aws:iam::${AWS_ACCOUNT_ID}:role/${ROLE_NAME}"
echo ""

# 4. Create Lambda Function
echo -e "${YELLOW}Step 4: Creating Lambda function...${NC}"
FUNCTION_NAME="${PROJECT_NAME}-api"

cd /workspaces/AI-Film-Studio/infrastructure/lambda
zip -r /tmp/lambda-function.zip handler.py

if ! aws lambda get-function --function-name $FUNCTION_NAME 2>/dev/null; then
    aws lambda create-function \
        --function-name $FUNCTION_NAME \
        --runtime python3.11 \
        --handler handler.lambda_handler \
        --zip-file fileb:///tmp/lambda-function.zip \
        --role $ROLE_ARN \
        --timeout 30 \
        --memory-size 256 \
        --environment "Variables={PROJECTS_TABLE=${TABLE_NAME},ASSETS_BUCKET=${BUCKET_NAME}}" \
        --region $AWS_REGION
    echo -e "${GREEN}✅ Lambda function created${NC}"
else
    aws lambda update-function-code \
        --function-name $FUNCTION_NAME \
        --zip-file fileb:///tmp/lambda-function.zip
    echo -e "${GREEN}✅ Lambda function updated${NC}"
fi
echo ""

# 5. Create API Gateway
echo -e "${YELLOW}Step 5: Creating API Gateway...${NC}"
API_NAME="${PROJECT_NAME}-http-api"

API_ID=$(aws apigatewayv2 get-apis --query "Items[?Name=='${API_NAME}'].ApiId" --output text)

if [ -z "$API_ID" ]; then
    API_ID=$(aws apigatewayv2 create-api \
        --name $API_NAME \
        --protocol-type HTTP \
        --cors-configuration 'AllowOrigins=["https://ai-empower-hq-360.github.io","http://localhost:3000"],AllowMethods=["*"],AllowHeaders=["*"],AllowCredentials=false' \
        --query 'ApiId' \
        --output text)
    echo -e "${GREEN}✅ API Gateway created: ${API_ID}${NC}"
else
    echo -e "${GREEN}✅ API Gateway already exists: ${API_ID}${NC}"
fi

# Create Lambda integration
INTEGRATION_ID=$(aws apigatewayv2 get-integrations --api-id $API_ID --query "Items[0].IntegrationId" --output text 2>/dev/null || echo "")

if [ -z "$INTEGRATION_ID" ] || [ "$INTEGRATION_ID" == "None" ]; then
    INTEGRATION_ID=$(aws apigatewayv2 create-integration \
        --api-id $API_ID \
        --integration-type AWS_PROXY \
        --integration-uri "arn:aws:lambda:${AWS_REGION}:${AWS_ACCOUNT_ID}:function:${FUNCTION_NAME}" \
        --payload-format-version "2.0" \
        --query 'IntegrationId' \
        --output text)
    echo -e "${GREEN}✅ Lambda integration created${NC}"
fi

# Create route
aws apigatewayv2 create-route \
    --api-id $API_ID \
    --route-key 'ANY /{proxy+}' \
    --target "integrations/${INTEGRATION_ID}" 2>/dev/null || true

# Create default stage
aws apigatewayv2 create-stage \
    --api-id $API_ID \
    --stage-name prod \
    --auto-deploy 2>/dev/null || true

# Add Lambda permission for API Gateway
aws lambda add-permission \
    --function-name $FUNCTION_NAME \
    --statement-id apigateway-invoke \
    --action lambda:InvokeFunction \
    --principal apigateway.amazonaws.com \
    --source-arn "arn:aws:execute-api:${AWS_REGION}:${AWS_ACCOUNT_ID}:${API_ID}/*" 2>/dev/null || true

echo ""

# 6. Output URLs
API_URL="https://${API_ID}.execute-api.${AWS_REGION}.amazonaws.com/prod"
GITHUB_PAGES_URL="https://ai-empower-hq-360.github.io/AI-Film-Studio/"

echo -e "${BLUE}================================================${NC}"
echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""
echo -e "${YELLOW}Frontend (GitHub Pages):${NC}"
echo "  $GITHUB_PAGES_URL"
echo ""
echo -e "${YELLOW}Backend API:${NC}"
echo "  $API_URL"
echo ""
echo -e "${YELLOW}Test the API:${NC}"
echo "  curl ${API_URL}/api/health"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "  1. Push to GitHub to trigger GitHub Pages deployment"
echo "  2. Set API_URL in GitHub repo settings:"
echo "     Settings → Secrets → Variables → New variable"
echo "     Name: API_URL"
echo "     Value: ${API_URL}"
echo ""
