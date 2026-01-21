# AWS CloudShell Commands for Amplify Management

## Quick Reference Guide

### Access AWS CloudShell

1. Open AWS Console: https://console.aws.amazon.com/
2. Click the CloudShell icon (terminal icon) in the top navigation bar
3. CloudShell opens in the bottom panel

---

## Setup Commands

### 1. Run Automated Setup Script

```bash
# Clone repository (if not already in CloudShell)
git clone https://github.com/AI-Empower-HQ-360/AI-Film-Studio.git
cd AI-Film-Studio

# Make script executable
chmod +x scripts/amplify-cloudshell-setup.sh

# Run setup
./scripts/amplify-cloudshell-setup.sh
```

### 2. Manual Setup (Alternative)

#### Check AWS CLI Version
```bash
aws --version
aws amplify help
```

#### Verify AWS Account
```bash
aws sts get-caller-identity
```

#### List Existing Amplify Apps
```bash
aws amplify list-apps --region us-east-1
```

---

## Managing Amplify App

### View App Details

```bash
# Set your app ID (get from Amplify Console)
APP_ID="d1234abcd5678"
REGION="us-east-1"

# Get app info
aws amplify get-app --app-id $APP_ID --region $REGION

# List branches
aws amplify list-branches --app-id $APP_ID --region $REGION
```

### Update Environment Variables

```bash
# Update global environment variables
aws amplify update-app \
  --app-id $APP_ID \
  --region $REGION \
  --environment-variables \
    NODE_VERSION=18 \
    NEXT_PUBLIC_API_URL=https://api-prod.aifilmstudio.com \
    NEXT_PUBLIC_WS_URL=wss://api-prod.aifilmstudio.com \
    NEXT_PUBLIC_ENABLE_ANALYTICS=true
```

### Update Branch-Specific Variables

```bash
# Update staging branch variables
aws amplify update-branch \
  --app-id $APP_ID \
  --branch-name staging \
  --region $REGION \
  --environment-variables \
    NEXT_PUBLIC_ENV=staging \
    NEXT_PUBLIC_API_URL=https://api-staging.aifilmstudio.com \
    NEXT_PUBLIC_ENABLE_ANALYTICS=false
```

---

## Deployment Management

### Trigger Manual Deployment

```bash
# Deploy main branch
aws amplify start-job \
  --app-id $APP_ID \
  --branch-name main \
  --job-type RELEASE \
  --region $REGION

# Deploy staging branch
aws amplify start-job \
  --app-id $APP_ID \
  --branch-name staging \
  --job-type RELEASE \
  --region $REGION
```

### Monitor Deployment

```bash
# List recent jobs
aws amplify list-jobs \
  --app-id $APP_ID \
  --branch-name main \
  --region $REGION \
  --max-results 5

# Get specific job details
JOB_ID="1"
aws amplify get-job \
  --app-id $APP_ID \
  --branch-name main \
  --job-id $JOB_ID \
  --region $REGION
```

### Stop Deployment

```bash
aws amplify stop-job \
  --app-id $APP_ID \
  --branch-name main \
  --job-id $JOB_ID \
  --region $REGION
```

---

## Branch Management

### Create New Branch

```bash
# Create and configure new branch
aws amplify create-branch \
  --app-id $APP_ID \
  --branch-name feature-branch \
  --region $REGION \
  --enable-auto-build \
  --environment-variables \
    NEXT_PUBLIC_ENV=development \
    NEXT_PUBLIC_API_URL=https://api-dev.aifilmstudio.com
```

### Delete Branch

```bash
aws amplify delete-branch \
  --app-id $APP_ID \
  --branch-name feature-branch \
  --region $REGION
```

### Update Branch Settings

```bash
# Enable/disable auto-build
aws amplify update-branch \
  --app-id $APP_ID \
  --branch-name dev \
  --region $REGION \
  --enable-auto-build

# Disable auto-build
aws amplify update-branch \
  --app-id $APP_ID \
  --branch-name dev \
  --region $REGION \
  --no-enable-auto-build
```

---

## Domain Management

### Add Custom Domain

```bash
# Add domain
aws amplify create-domain-association \
  --app-id $APP_ID \
  --domain-name aifilmstudio.com \
  --region $REGION \
  --sub-domain-settings \
    prefix=www,branchName=main \
    prefix=staging,branchName=staging \
    prefix=sandbox,branchName=sandbox \
    prefix=dev,branchName=dev
```

### Get Domain Status

```bash
aws amplify get-domain-association \
  --app-id $APP_ID \
  --domain-name aifilmstudio.com \
  --region $REGION
```

### Delete Domain

```bash
aws amplify delete-domain-association \
  --app-id $APP_ID \
  --domain-name aifilmstudio.com \
  --region $REGION
```

---

## Logging & Monitoring

### View Build Logs via CloudWatch

```bash
# List log groups
aws logs describe-log-groups \
  --log-group-name-prefix /aws/amplify/$APP_ID \
  --region $REGION

# Tail logs
aws logs tail /aws/amplify/$APP_ID/main \
  --follow \
  --region $REGION
```

### Export Logs to S3

```bash
# Create S3 bucket for logs
BUCKET_NAME="ai-film-studio-amplify-logs"
aws s3 mb s3://$BUCKET_NAME --region $REGION

# Export logs
aws logs create-export-task \
  --log-group-name /aws/amplify/$APP_ID/main \
  --from $(date -d '7 days ago' +%s)000 \
  --to $(date +%s)000 \
  --destination $BUCKET_NAME \
  --destination-prefix amplify-logs \
  --region $REGION
```

---

## Webhooks (for Custom CI/CD)

### Create Webhook

```bash
# Create webhook for branch
aws amplify create-webhook \
  --app-id $APP_ID \
  --branch-name main \
  --region $REGION
```

### List Webhooks

```bash
aws amplify list-webhooks \
  --app-id $APP_ID \
  --region $REGION
```

### Trigger Webhook Manually

```bash
# Get webhook URL from list-webhooks command
WEBHOOK_URL="https://webhooks.amplify.us-east-1.amazonaws.com/..."

curl -X POST $WEBHOOK_URL
```

---

## IAM & Security

### Verify Service Role

```bash
# Check if role exists
aws iam get-role --role-name amplifyconsole-backend-role

# List attached policies
aws iam list-attached-role-policies \
  --role-name amplifyconsole-backend-role
```

### Update App to Use Different Role

```bash
# Get account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Update app with new role
aws amplify update-app \
  --app-id $APP_ID \
  --region $REGION \
  --iam-service-role-arn "arn:aws:iam::$ACCOUNT_ID:role/amplifyconsole-backend-role"
```

---

## Performance & Cost Monitoring

### Get Build Statistics

```bash
# List all jobs with timing
aws amplify list-jobs \
  --app-id $APP_ID \
  --branch-name main \
  --region $REGION \
  --max-results 10 \
  --query 'jobSummaries[*].[jobId,status,startTime,endTime]' \
  --output table
```

### Check App Usage

```bash
# Get app metrics (requires CloudWatch)
aws cloudwatch get-metric-statistics \
  --namespace AWS/Amplify \
  --metric-name BuildTime \
  --dimensions Name=App,Value=$APP_ID \
  --start-time $(date -u -d '30 days ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 86400 \
  --statistics Average,Maximum \
  --region $REGION
```

---

## Troubleshooting

### Get Recent Build Errors

```bash
# Get failed jobs
aws amplify list-jobs \
  --app-id $APP_ID \
  --branch-name main \
  --region $REGION \
  --max-results 5 \
  --query 'jobSummaries[?status==`FAILED`]'
```

### Validate Build Configuration

```bash
# Get branch configuration
aws amplify get-branch \
  --app-id $APP_ID \
  --branch-name main \
  --region $REGION \
  --query 'branch.[buildSpec,environmentVariables]'
```

### Reset Branch

```bash
# Delete and recreate branch (WARNING: destructive)
aws amplify delete-branch --app-id $APP_ID --branch-name dev --region $REGION
aws amplify create-branch --app-id $APP_ID --branch-name dev --region $REGION --enable-auto-build
```

---

## Useful Aliases for CloudShell

Add these to your CloudShell environment:

```bash
# Create aliases file
cat > ~/.amplify_aliases <<'EOF'
# Amplify CLI Aliases
export APP_ID="d1234abcd5678"  # Replace with your app ID
export REGION="us-east-1"

alias amp-info='aws amplify get-app --app-id $APP_ID --region $REGION'
alias amp-branches='aws amplify list-branches --app-id $APP_ID --region $REGION'
alias amp-jobs='aws amplify list-jobs --app-id $APP_ID --branch-name main --region $REGION --max-results 5'
alias amp-deploy='aws amplify start-job --app-id $APP_ID --branch-name main --job-type RELEASE --region $REGION'
alias amp-logs='aws logs tail /aws/amplify/$APP_ID/main --follow --region $REGION'
EOF

# Load aliases
source ~/.amplify_aliases

# Add to .bashrc for persistence
echo 'source ~/.amplify_aliases' >> ~/.bashrc
```

---

## Quick Deployment Script

Save this as a quick deployment command:

```bash
#!/bin/bash
# deploy-amplify.sh - Quick deployment script

APP_ID="${1:-d1234abcd5678}"
BRANCH="${2:-main}"
REGION="${3:-us-east-1}"

echo "Deploying $BRANCH branch..."
JOB_ID=$(aws amplify start-job \
  --app-id $APP_ID \
  --branch-name $BRANCH \
  --job-type RELEASE \
  --region $REGION \
  --query 'jobSummary.jobId' \
  --output text)

echo "Job ID: $JOB_ID"
echo "Monitor: aws amplify get-job --app-id $APP_ID --branch-name $BRANCH --job-id $JOB_ID --region $REGION"
```

---

## Additional Resources

- **AWS Amplify CLI Reference**: https://docs.aws.amazon.com/cli/latest/reference/amplify/
- **CloudShell User Guide**: https://docs.aws.amazon.com/cloudshell/latest/userguide/
- **Amplify Console**: https://console.aws.amazon.com/amplify/

---

*Last updated: January 2026*
