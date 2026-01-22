# AWS Infrastructure Quick Start

Get your AI Film Studio infrastructure deployed in 10 minutes!

## Prerequisites Checklist

- [ ] AWS Account created
- [ ] AWS CLI installed (`aws --version`)
- [ ] AWS CLI configured (`aws configure`)
- [ ] AWS CDK installed (`npm install -g aws-cdk`)
- [ ] Python 3.12 installed (`py -3.12 --version`)
- [ ] Docker installed (`docker --version`)

## Quick Setup (5 Steps)

### 1. Install Prerequisites

```powershell
# AWS CLI
choco install awscli

# AWS CDK
npm install -g aws-cdk

# Verify
aws --version
cdk --version
```

### 2. Configure AWS

```powershell
aws configure
# Enter your AWS credentials
```

### 3. Set Up CDK Project

```powershell
cd C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk

# Create virtual environment
py -3.12 -m venv .venv-cdk
.venv-cdk\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 4. Bootstrap CDK

```powershell
# Get account ID
$accountId = (aws sts get-caller-identity --query Account --output text)

# Bootstrap
cdk bootstrap aws://$accountId/us-east-1
```

### 5. Deploy

```powershell
# Deploy to dev environment
cdk deploy --context environment=dev

# Or use deployment script
.\deploy.ps1
```

## Verify Deployment

```powershell
# Get backend URL
$backendUrl = (aws cloudformation describe-stacks --stack-name AIFilmStudio --query 'Stacks[0].Outputs[?OutputKey==`BackendURL`].OutputValue' --output text)

# Test
Invoke-WebRequest "$backendUrl/api/v1/health"
```

## What Gets Deployed

✅ VPC with public/private subnets  
✅ ECS Fargate cluster for backend  
✅ RDS PostgreSQL database  
✅ S3 buckets for assets  
✅ SQS queues for jobs  
✅ ElastiCache Redis for caching  
✅ CloudFront CDN  
✅ ECR repositories  
✅ CloudWatch monitoring  

## Next Steps

1. Build and push Docker images
2. Configure database
3. Set up secrets
4. Test API endpoints

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions.
