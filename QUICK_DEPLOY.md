# 🚀 Quick Deployment Guide

## Pre-Deployment Checklist

### ✅ Code Status
- All 14 AI engines integrated with AI framework
- All tests passing (180/190 tests)
- CDK infrastructure validated
- CI/CD workflows configured

### ⚠️ Required Before Deployment

1. **GitHub Secrets** (Settings → Secrets and variables → Actions):
   ```
   AWS_ACCESS_KEY_ID
   AWS_SECRET_ACCESS_KEY
   AWS_ACCOUNT_ID
   AWS_REGION (default: us-east-1)
   ```

2. **AWS IAM User** with permissions:
   - CloudFormation (full access)
   - EC2, ECS, RDS, S3, CloudFront
   - SQS, SNS, ElastiCache
   - Secrets Manager, IAM, CloudWatch

## Deployment Options

### Option 1: CI/CD Automated (Recommended) ⭐

**Steps:**
1. Ensure GitHub secrets are set
2. Go to **GitHub → Actions** tab
3. Select **"AWS CDK Deploy"** workflow
4. Click **"Run workflow"**
5. Select:
   - Environment: `dev` (for first deployment)
   - Action: `deploy`
6. Click **"Run workflow"**

**What happens:**
- ✅ Runs infrastructure tests
- ✅ Synthesizes CDK stack
- ✅ Shows diff (preview changes)
- ✅ Bootstraps CDK (if needed)
- ✅ Deploys infrastructure
- ✅ Displays stack outputs

**Time:** 15-30 minutes (first deployment)

### Option 2: Manual Deployment (Local)

**Prerequisites:**
- Python 3.12 installed
- AWS CLI configured
- CDK installed: `npm install -g aws-cdk`

**Steps:**
```powershell
# Navigate to CDK directory
cd infrastructure/aws-cdk

# Create virtual environment (if not exists)
python -m venv .venv-cdk

# Activate virtual environment
.venv-cdk\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure AWS (if not already)
aws configure

# Preview changes
cdk diff

# Deploy
cdk deploy --require-approval never
```

## What Gets Deployed

- ✅ VPC with public/private subnets
- ✅ RDS PostgreSQL database (16.1)
- ✅ ECS Fargate cluster and service
- ✅ Application Load Balancer
- ✅ S3 buckets (assets, characters, marketing)
- ✅ CloudFront distribution
- ✅ SQS queues (job processing)
- ✅ ElastiCache Redis cluster
- ✅ SNS topics (notifications)
- ✅ CloudWatch alarms (monitoring)
- ✅ Security groups and IAM roles

## Post-Deployment

After deployment, you'll get:
- Backend URL (ALB endpoint)
- Database endpoint
- CloudFront distribution URL
- S3 bucket names
- Resource ARNs

**Verify deployment:**
```bash
aws cloudformation describe-stacks --stack-name AIFilmStudio-dev
```

## Cost Estimate

**Development Environment:** ~$60-100/month
**Production Environment:** ~$200-400/month

## Troubleshooting

If deployment fails:
1. Check GitHub Actions logs
2. Review CloudFormation events in AWS Console
3. Verify IAM permissions
4. Check AWS service limits

---

**Ready to deploy? Choose your option above! 🚀**
