# AWS Free Tier Backend for AI Film Studio

## Services Used (All Free Tier)

| Service | Free Tier Limit | Purpose |
|---------|-----------------|---------|
| Lambda | 1M requests/month | API endpoints |
| API Gateway | 1M calls/month | REST API |
| DynamoDB | 25GB storage | User data, projects |
| S3 | 5GB (12 months) | Media storage |
| Cognito | 50K MAU | Authentication |

## Quick Setup (5 minutes)

### 1. Create S3 Bucket
```bash
aws s3 mb s3://ai-film-studio-assets-$(aws sts get-caller-identity --query Account --output text) --region us-east-1
```

### 2. Create DynamoDB Table
```bash
aws dynamodb create-table \
    --table-name ai-film-studio-projects \
    --attribute-definitions AttributeName=userId,AttributeType=S AttributeName=projectId,AttributeType=S \
    --key-schema AttributeName=userId,KeyType=HASH AttributeName=projectId,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1
```

### 3. Create Lambda Function
```bash
# Package the Lambda code
cd infrastructure/lambda
zip -r function.zip .

# Create Lambda
aws lambda create-function \
    --function-name ai-film-studio-api \
    --runtime python3.11 \
    --handler handler.lambda_handler \
    --zip-file fileb://function.zip \
    --role arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/lambda-execution-role \
    --region us-east-1
```

### 4. Create API Gateway
```bash
aws apigatewayv2 create-api \
    --name ai-film-studio-api \
    --protocol-type HTTP \
    --cors-configuration AllowOrigins="https://ai-empower-hq-360.github.io",AllowMethods="*",AllowHeaders="*" \
    --region us-east-1
```

## GitHub Pages Frontend URL
```
https://ai-empower-hq-360.github.io/AI-Film-Studio/
```

## API Gateway Backend URL
```
https://{api-id}.execute-api.us-east-1.amazonaws.com/prod
```
