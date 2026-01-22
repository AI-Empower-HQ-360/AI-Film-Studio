# AWS Infrastructure Setup Guide - AI Film Studio

Complete guide to set up and deploy the AI Film Studio infrastructure on AWS.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Configuration](#configuration)
4. [Deployment](#deployment)
5. [Post-Deployment](#post-deployment)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### 1. Required Tools

#### AWS CLI
```powershell
# Windows (Chocolatey)
choco install awscli

# Or download from:
# https://aws.amazon.com/cli/

# Verify
aws --version
```

#### AWS CDK CLI
```powershell
npm install -g aws-cdk
cdk --version
```

#### Python 3.11 or 3.12
```powershell
# Check available Python versions
py -0

# If Python 3.12 not available, install it
# See: PYTHON_VERSION_REQUIREMENT.md
```

#### Docker (for building images)
```powershell
# Download Docker Desktop from:
# https://www.docker.com/products/docker-desktop
```

### 2. AWS Account Setup

1. **Create AWS Account**
   - Go to: https://aws.amazon.com/
   - Sign up for an account

2. **Create IAM User**
   ```powershell
   # Or use AWS Console:
   # IAM → Users → Create User
   # Attach policies:
   # - AdministratorAccess (for initial setup)
   # - Or create custom policy with required permissions
   ```

3. **Configure AWS CLI**
   ```powershell
   aws configure
   # Enter:
   # - AWS Access Key ID
   # - AWS Secret Access Key
   # - Default region: us-east-1
   # - Default output format: json
   ```

4. **Verify Configuration**
   ```powershell
   aws sts get-caller-identity
   ```

---

## Initial Setup

### Step 1: Navigate to Infrastructure Directory

```powershell
cd C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk
```

### Step 2: Create Python Virtual Environment

```powershell
# Use Python 3.12 (required for CDK)
py -3.12 -m venv .venv-cdk

# Activate
.venv-cdk\Scripts\Activate.ps1

# Verify Python version
python --version
# Should show: Python 3.12.x
```

### Step 3: Install Dependencies

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install CDK dependencies
pip install -r requirements.txt

# Verify CDK
cdk --version
```

### Step 4: Bootstrap CDK (First Time Only)

```powershell
# Get your AWS account ID
$accountId = (aws sts get-caller-identity --query Account --output text)
$region = "us-east-1"  # or your preferred region

# Bootstrap CDK
cdk bootstrap aws://$accountId/$region
```

---

## Configuration

### Environment Variables

Set context in `cdk.json` or via command line:

**Option 1: Edit cdk.json**
```json
{
  "context": {
    "environment": "dev",
    "account": "YOUR_ACCOUNT_ID",
    "region": "us-east-1"
  }
}
```

**Option 2: Command Line**
```powershell
cdk deploy --context environment=dev --context account=YOUR_ACCOUNT_ID --context region=us-east-1
```

### Environment Options

- `dev` - Development (smaller instances, single AZ)
- `staging` - Staging (medium instances, single AZ)
- `production` - Production (larger instances, multi-AZ)

---

## Deployment

### Option 1: Automated Deployment Script

```powershell
# Windows
.\deploy.ps1

# Linux/Mac
./deploy.sh
```

### Option 2: Manual CDK Commands

```powershell
# 1. Synthesize CloudFormation template
cdk synth

# 2. View differences
cdk diff

# 3. Deploy stack
cdk deploy

# 4. Confirm when prompted
```

### Option 3: Deploy Specific Environment

```powershell
# Development
cdk deploy --context environment=dev

# Staging
cdk deploy --context environment=staging

# Production
cdk deploy --context environment=production
```

---

## Post-Deployment

### 1. Get Stack Outputs

```powershell
# View all outputs
aws cloudformation describe-stacks --stack-name AIFilmStudio --query 'Stacks[0].Outputs'

# Get specific output
aws cloudformation describe-stacks --stack-name AIFilmStudio --query 'Stacks[0].Outputs[?OutputKey==`BackendURL`].OutputValue' --output text
```

### 2. Build and Push Docker Images

```powershell
# Get ECR repository URIs from outputs
$backendRepo = (aws cloudformation describe-stacks --stack-name AIFilmStudio --query 'Stacks[0].Outputs[?OutputKey==`BackendRepositoryURI`].OutputValue' --output text)
$workerRepo = (aws cloudformation describe-stacks --stack-name AIFilmStudio --query 'Stacks[0].Outputs[?OutputKey==`WorkerRepositoryURI`].OutputValue' --output text)

# Authenticate Docker to ECR
$region = "us-east-1"
$accountId = (aws sts get-caller-identity --query Account --output text)
aws ecr get-login-password --region $region | docker login --username AWS --password-stdin $accountId.dkr.ecr.$region.amazonaws.com

# Build backend image
cd ..\..\  # Root directory
docker build -f infrastructure/aws-cdk/Dockerfile.backend -t ai-film-studio-backend .
docker tag ai-film-studio-backend:latest $backendRepo:latest
docker push $backendRepo:latest

# Build worker image
docker build -f infrastructure/aws-cdk/Dockerfile.worker -t ai-film-studio-worker .
docker tag ai-film-studio-worker:latest $workerRepo:latest
docker push $workerRepo:latest
```

### 3. Configure Database

```powershell
# Get database endpoint
$dbEndpoint = (aws cloudformation describe-stacks --stack-name AIFilmStudio --query 'Stacks[0].Outputs[?OutputKey==`DatabaseEndpoint`].OutputValue' --output text)

# Get database credentials
$dbSecret = (aws secretsmanager get-secret-value --secret-id AIFilmStudio/DatabaseSecret --query SecretString --output text | ConvertFrom-Json)

# Connect to database (using psql or your preferred tool)
# Host: $dbEndpoint
# Port: 5432
# Database: aifilmstudio
# Username: $dbSecret.username
# Password: $dbSecret.password
```

### 4. Set Up Secrets

```powershell
# Create secrets for API keys (if needed)
aws secretsmanager create-secret `
  --name ai-film-studio/openai-api-key `
  --secret-string '{"api_key":"YOUR_OPENAI_KEY"}'

aws secretsmanager create-secret `
  --name ai-film-studio/youtube-api-key `
  --secret-string '{"api_key":"YOUR_YOUTUBE_KEY"}'
```

---

## Verification

### Check Deployment Status

```powershell
# Check CloudFormation stack
aws cloudformation describe-stacks --stack-name AIFilmStudio

# Check ECS service
aws ecs list-services --cluster ai-film-studio-dev

# Check RDS instance
aws rds describe-db-instances --db-instance-identifier AIFilmStudio-Database*

# Check S3 buckets
aws s3 ls | Select-String "ai-film-studio"
```

### Test Backend API

```powershell
# Get backend URL
$backendUrl = (aws cloudformation describe-stacks --stack-name AIFilmStudio --query 'Stacks[0].Outputs[?OutputKey==`BackendURL`].OutputValue' --output text)

# Test health endpoint
Invoke-WebRequest "$backendUrl/api/v1/health"
```

### View Logs

```powershell
# ECS service logs
aws logs tail /ecs/ai-film-studio/backend-dev --follow

# CloudWatch Logs Insights
aws logs tail /ecs/ai-film-studio/backend-dev --since 1h
```

---

## Troubleshooting

### Issue: CDK Bootstrap Fails

**Error:** `Error: Need to perform AWS calls for account`

**Solution:**
```powershell
# Verify AWS credentials
aws sts get-caller-identity

# Bootstrap with explicit account/region
cdk bootstrap aws://ACCOUNT-ID/REGION
```

### Issue: Python Version Error

**Error:** `Python 3.13 is not supported`

**Solution:**
```powershell
# Use Python 3.12
py -3.12 -m venv .venv-cdk
.venv-cdk\Scripts\Activate.ps1

# Or see: PYTHON_VERSION_REQUIREMENT.md
```

### Issue: Docker Push Fails

**Error:** `denied: Permission denied`

**Solution:**
```powershell
# Re-authenticate Docker
$region = "us-east-1"
$accountId = (aws sts get-caller-identity --query Account --output text)
aws ecr get-login-password --region $region | docker login --username AWS --password-stdin $accountId.dkr.ecr.$region.amazonaws.com
```

### Issue: ECS Service Not Starting

**Check:**
```powershell
# View service events
aws ecs describe-services --cluster ai-film-studio-dev --services BackendService

# Check task definition
aws ecs describe-task-definition --task-definition AIFilmStudio-BackendTaskDefinition

# View CloudWatch logs
aws logs tail /ecs/ai-film-studio/backend-dev --since 1h
```

### Issue: Database Connection Fails

**Check:**
```powershell
# Verify security group allows access
aws ec2 describe-security-groups --filters "Name=group-name,Values=*Database*"

# Check database status
aws rds describe-db-instances --db-instance-identifier AIFilmStudio-Database*

# Verify credentials
aws secretsmanager get-secret-value --secret-id AIFilmStudio/DatabaseSecret
```

---

## Architecture Overview

### Components Deployed

1. **VPC** - Network isolation
   - Public subnets (ALB)
   - Private subnets (ECS)
   - Isolated subnets (RDS)

2. **ECS Fargate** - Backend API
   - Auto-scaling (1-50 tasks)
   - Load balanced via ALB
   - CloudWatch logging

3. **RDS PostgreSQL** - Database
   - Multi-AZ (production)
   - Automated backups
   - Encrypted storage

4. **S3 Buckets** - Asset storage
   - Assets bucket
   - Characters bucket
   - Marketing bucket

5. **SQS Queues** - Job processing
   - Main job queue
   - Video generation queue
   - Voice synthesis queue

6. **ElastiCache Redis** - Caching
   - API response caching
   - Session storage
   - Job state cache

7. **SNS Topics** - Notifications
   - Job completion
   - Error alerts
   - System alerts

8. **CloudFront** - CDN
   - Global content delivery
   - S3 origin
   - HTTPS enabled

9. **ECR Repositories** - Container images
   - Backend images
   - Worker images

10. **GPU Workers** - AI processing
    - EC2 G4DN instances
    - Launch template ready

11. **CloudWatch** - Monitoring
    - Logs aggregation
    - Metrics and alarms
    - Automated alerting

---

## Cost Management

### Development Environment
- **Estimated:** $50-100/month
- **Components:**
  - ECS Fargate: ~$15-30
  - RDS: ~$15-20
  - ElastiCache: ~$10-15
  - S3: ~$5-10
  - CloudFront: ~$5-15

### Production Environment
- **Estimated:** $450-1200/month
- **Components:**
  - ECS Fargate: ~$100-300
  - RDS Multi-AZ: ~$50-150
  - ElastiCache: ~$30-80
  - S3: ~$20-50
  - CloudFront: ~$30-100
  - GPU Workers: ~$200-500

### Cost Optimization Tips

1. **Use Reserved Instances** for production RDS
2. **Enable S3 Lifecycle Policies** for old assets
3. **Use Spot Instances** for GPU workers (dev/staging)
4. **Monitor CloudWatch** for unused resources
5. **Set up Billing Alarms** in CloudWatch

---

## Security Best Practices

1. **IAM Roles** - Use least privilege
2. **Security Groups** - Restrict access
3. **Secrets Manager** - Store credentials securely
4. **Encryption** - Enable at rest and in transit
5. **VPC** - Isolate resources
6. **CloudTrail** - Enable audit logging

---

## Next Steps

1. **Configure Custom Domain**
   - Set up Route 53
   - Configure SSL certificate
   - Update CloudFront distribution

2. **Set Up CI/CD**
   - GitHub Actions workflow
   - Automated deployments
   - Image building pipeline

3. **Enable Monitoring**
   - Configure CloudWatch dashboards
   - Set up alerting
   - Enable X-Ray tracing

4. **Backup Strategy**
   - RDS automated backups
   - S3 versioning
   - Disaster recovery plan

---

## Quick Reference

```powershell
# Deploy
cdk deploy

# Destroy
cdk destroy

# View outputs
aws cloudformation describe-stacks --stack-name AIFilmStudio --query 'Stacks[0].Outputs'

# View logs
aws logs tail /ecs/ai-film-studio/backend-dev --follow

# Scale service
aws ecs update-service --cluster ai-film-studio-dev --service BackendService --desired-count 2
```

---

## Support

- **CDK Documentation:** https://docs.aws.amazon.com/cdk/
- **AWS Services:** https://aws.amazon.com/documentation/
- **Project Issues:** Check repository issues
