# AWS CDK Infrastructure for AI Film Studio

## Overview

This directory contains AWS CDK (Cloud Development Kit) infrastructure code for deploying the AI Film Studio backend and worker infrastructure on AWS.

**Note:** Frontend deployment remains on **GitHub Pages**. This AWS CDK setup is for:
- Backend API (FastAPI)
- GPU Worker instances (AI processing)
- Database (RDS PostgreSQL)
- Asset storage (S3)
- Job queues (SQS)
- Content delivery (CloudFront)

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CloudFront CDN                        │
│              (S3 Assets Distribution)                    │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              Application Load Balancer                   │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              ECS Fargate Cluster                         │
│  ┌────────────────────────────────────────────────┐    │
│  │  Backend API Service (FastAPI)                 │    │
│  │  - Character Engine                            │    │
│  │  - Writing Engine                              │    │
│  │  - Production Management                       │    │
│  │  - All 8 Engines                               │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   RDS        │  │  S3 Buckets  │  │  SQS Queues  │
│ PostgreSQL   │  │  - Assets    │  │  - Jobs      │
│              │  │  - Characters│  │  - Video     │
│              │  │  - Marketing │  │  - Voice     │
└──────────────┘  └──────────────┘  └──────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│          GPU Worker Instances (EC2)                      │
│  - Video Generation                                      │
│  - Voice Synthesis                                       │
│  - AI Processing                                         │
└─────────────────────────────────────────────────────────┘
```

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** configured
3. **Python 3.11 or 3.12** ⚠️ (Python 3.13 is not yet supported by AWS CDK)
   - See [PYTHON_VERSION_REQUIREMENT.md](./PYTHON_VERSION_REQUIREMENT.md) for details
4. **Node.js 18+** (for CDK)
5. **AWS CDK CLI**: `npm install -g aws-cdk`

**⚠️ Important:** If you have Python 3.13 installed, you must install Python 3.12 or 3.11 separately for CDK. Use `py -3.12` to create the virtual environment.

## Setup

### 1. Install Dependencies

**⚠️ Python Version Check:**
```bash
# Check if Python 3.12 is available
py -3.12 --version  # Windows
python3.12 --version  # Linux/Mac

# If not installed, download from:
# https://www.python.org/downloads/release/python-3120/
```

**Create Virtual Environment:**
```bash
cd infrastructure/aws-cdk

# Windows (use Python 3.12)
py -3.12 -m venv .venv-cdk
.venv-cdk\Scripts\Activate.ps1

# Linux/Mac (use Python 3.12)
python3.12 -m venv .venv-cdk
source .venv-cdk/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

**Note:** If you only have Python 3.13, see [PYTHON_VERSION_REQUIREMENT.md](./PYTHON_VERSION_REQUIREMENT.md) for installation instructions.

### 2. Configure AWS

```bash
aws configure
# Enter AWS Access Key ID
# Enter AWS Secret Access Key
# Enter region: us-east-1 (or your preferred region)
```

### 3. Bootstrap CDK (First Time Only)

```bash
cdk bootstrap aws://ACCOUNT-ID/REGION
# Example: cdk bootstrap aws://123456789012/us-east-1
```

### 4. Configure Environment

Set context variables in `cdk.json` or via command line:

```bash
# Development
cdk deploy --context environment=dev --context region=us-east-1

# Production
cdk deploy --context environment=production --context region=us-east-1
```

## Deployment

### Deploy All Stacks

```bash
cdk deploy
```

### Deploy Specific Environment

```bash
# Development
cdk deploy --context environment=dev

# Staging
cdk deploy --context environment=staging

# Production
cdk deploy --context environment=production
```

### Preview Changes

```bash
cdk diff
```

### Destroy Stack

```bash
cdk destroy
```

## Stack Components

### 1. VPC
- Public subnets for load balancer
- Private subnets for ECS services
- Isolated subnets for database
- NAT Gateway for outbound internet access

### 2. ECS Fargate
- Backend API service
- Auto-scaling (1-50 instances)
- Load balanced via ALB
- CloudWatch logging

### 3. RDS PostgreSQL
- Multi-AZ in production
- Automated backups
- Secret Manager for credentials
- Encrypted storage

### 4. S3 Buckets
- **Assets Bucket**: Videos, images, audio files
- **Characters Bucket**: Character assets
- **Marketing Bucket**: Marketing materials
- Versioning enabled
- Lifecycle policies

### 5. SQS Queues
- Main job queue
- Video generation queue
- Voice synthesis queue
- Dead-letter queues

### 6. ElastiCache Redis
- Caching layer for API responses
- Session storage
- Job state caching
- Character consistency cache

### 7. SNS Topics
- Job completion notifications
- Error notifications
- System alerts

### 8. CloudWatch Monitoring
- CPU and memory alarms
- Database performance alarms
- Queue depth monitoring
- Automated alerting via SNS

### 9. CloudFront CDN
- Global content delivery
- S3 origin
- HTTPS enabled
- Cache optimization

### 10. ECR Repositories
- Backend container images
- Worker container images
- Image scanning enabled

### 11. GPU Workers
- EC2 G4DN instances
- Launch template configuration
- Auto-scaling ready
- ECS integration ready

## Environment Configuration

### Development
- Smaller instance sizes
- Single AZ deployment
- No deletion protection
- Minimal backups

### Production
- Larger instance sizes
- Multi-AZ deployment
- Deletion protection enabled
- Extended backups

## Cost Estimation

### Development Environment
- ECS Fargate: ~$15-30/month
- RDS: ~$15-20/month
- ElastiCache Redis: ~$10-15/month
- S3 Storage: ~$5-10/month
- CloudFront: ~$5-15/month
- SNS: ~$1-2/month
- CloudWatch: ~$5-10/month
- **Total: ~$51-102/month**

### Production Environment
- ECS Fargate: ~$100-300/month
- RDS Multi-AZ: ~$50-150/month
- ElastiCache Redis: ~$30-80/month
- S3 Storage: ~$20-50/month
- CloudFront: ~$30-100/month
- GPU Workers: ~$200-500/month
- SNS: ~$2-5/month
- CloudWatch: ~$20-50/month
- **Total: ~$452-1235/month**

## Outputs

After deployment, CDK outputs:
- Backend API URL
- Assets bucket name
- CloudFront distribution domain
- Database endpoint
- Redis endpoint and port
- ECR repository URIs
- SNS topic ARNs (job completion, errors, alerts)

## CI/CD Integration

### GitHub Actions

Add to `.github/workflows/aws-cdk-deploy.yml`:

```yaml
name: Deploy AWS CDK Infrastructure

on:
  workflow_dispatch:
    inputs:
      environment:
        required: true
        type: choice
        options:
          - dev
          - staging
          - production

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install CDK
        run: npm install -g aws-cdk
      
      - name: Install dependencies
        working-directory: infrastructure/aws-cdk
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: CDK Deploy
        working-directory: infrastructure/aws-cdk
        run: |
          cdk deploy --context environment=${{ github.event.inputs.environment }} --require-approval never
```

## Security

- All data encrypted at rest
- VPC isolation
- Security groups with least privilege
- IAM roles with minimal permissions
- Secrets stored in AWS Secrets Manager
- HTTPS only (CloudFront)

## Monitoring

- CloudWatch Logs for all services
- CloudWatch Metrics for ECS
- CloudWatch Alarms (configure as needed)
- X-Ray tracing (optional)

## Troubleshooting

### CDK Bootstrap Error
```bash
cdk bootstrap aws://ACCOUNT-ID/REGION
```

### Permission Errors
Ensure IAM user/role has:
- CloudFormation full access
- S3, ECS, RDS, EC2, VPC permissions

### Deployment Fails
Check CloudFormation console for detailed error messages.

## Next Steps

1. Configure domain names
2. Set up SSL certificates
3. Configure auto-scaling policies
4. Set up monitoring and alerts
5. Configure backup policies
6. Set up disaster recovery

## Documentation

- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/)
- [CDK Python Reference](https://docs.aws.amazon.com/cdk/api/v2/python/)
# Triggered deployment Fri Jan 23 02:18:18 UTC 2026
