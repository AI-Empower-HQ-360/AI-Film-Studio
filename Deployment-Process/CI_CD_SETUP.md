# CI/CD Setup Guide

## Problem Fixed

**Issue:** PostgreSQL version 15.3 not available in AWS RDS  
**Solution:** Updated to PostgreSQL 16.1 (widely available)

## CI/CD Pipeline Overview

The GitHub Actions workflow (`.github/workflows/aws-cdk-deploy.yml`) provides:

1. **Automated Testing**: Runs infrastructure tests before deployment
2. **Multi-Environment Support**: Dev, Staging, Production
3. **Manual Triggers**: Deploy on-demand with environment selection
4. **Auto-Deploy**: Automatic deployment on branch pushes

## Setup Instructions

### 1. Configure GitHub Secrets

Go to: **Settings → Secrets and variables → Actions**

Add these secrets:

```
AWS_ACCESS_KEY_ID          # AWS access key for CI/CD
AWS_SECRET_ACCESS_KEY      # AWS secret key for CI/CD
AWS_REGION                 # us-east-1 (or your region)
```

### 2. Create IAM User for CI/CD

```bash
# Create IAM user
aws iam create-user --user-name github-actions-cdk

# Attach policy (or create custom policy with CDK permissions)
aws iam attach-user-policy \
  --user-name github-actions-cdk \
  --policy-arn arn:aws:iam::aws:policy/PowerUserAccess

# Create access key
aws iam create-access-key --user-name github-actions-cdk
```

**Copy the Access Key ID and Secret Access Key** to GitHub secrets.

### 3. Bootstrap CDK (First Time Only)

```bash
cd infrastructure/aws-cdk

# Get your AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Bootstrap CDK
cdk bootstrap aws://$ACCOUNT_ID/us-east-1
```

Or let CI/CD do it automatically (it will skip if already bootstrapped).

## Workflow Triggers

### Automatic Deployment

- **Push to `main` branch** → Deploys to production
- **Push to `develop` branch** → Deploys to dev
- **Changes in `infrastructure/aws-cdk/**`** → Triggers deployment

### Manual Deployment

1. Go to **Actions** tab in GitHub
2. Select **"Deploy AWS CDK Infrastructure"** workflow
3. Click **"Run workflow"**
4. Select:
   - **Environment**: dev, staging, or production
   - **Deploy images**: true/false (build and push Docker images)

## Workflow Jobs

### 1. Test Job
- Runs infrastructure unit tests
- Synthesizes CDK stack
- Validates configuration
- **Must pass before deployment**

### 2. Deploy Job
- Configures AWS credentials
- Bootstraps CDK (if needed)
- Shows CDK diff (changes preview)
- Synthesizes stack
- Deploys infrastructure
- Displays stack outputs

### 3. Build and Push Images (Optional)
- Builds Docker images
- Pushes to ECR
- Updates ECS services

## Monitoring Deployments

### View Deployment Status

1. **GitHub Actions Tab**: See workflow runs and status
2. **AWS Console**: Check CloudFormation stack status
3. **Stack Outputs**: View in workflow logs or AWS Console

### Common Issues

#### PostgreSQL Version Error
**Error:** `Cannot find version 15.3 for postgres`  
**Fix:** Already fixed - using PostgreSQL 16.1

#### Bootstrap Error
**Error:** `CDK toolkit stack not found`  
**Fix:** Run `cdk bootstrap` manually or let CI/CD handle it

#### Permission Errors
**Error:** `Access Denied`  
**Fix:** Check IAM user permissions and GitHub secrets

#### Test Failures
**Error:** Tests fail before deployment  
**Fix:** Review test output, fix infrastructure code

## Environment-Specific Configuration

### Development
- Smaller instance sizes
- Single AZ deployment
- Shorter backup retention
- Deletion protection: OFF

### Production
- Larger instance sizes
- Multi-AZ deployment
- Longer backup retention
- Deletion protection: ON

## Best Practices

1. **Always test locally first:**
   ```bash
   cd infrastructure/aws-cdk
   pytest tests/
   cdk synth
   cdk diff
   ```

2. **Review CDK diff before deploying:**
   - Check what resources will be created/modified
   - Verify no unintended changes

3. **Use feature branches:**
   - Test changes in dev environment first
   - Merge to main only after validation

4. **Monitor costs:**
   - Review AWS billing dashboard
   - Use cost allocation tags

5. **Keep secrets secure:**
   - Never commit AWS credentials
   - Use GitHub secrets
   - Rotate keys regularly

## Troubleshooting

### Deployment Fails

1. **Check workflow logs** in GitHub Actions
2. **Check CloudFormation events** in AWS Console
3. **Verify AWS credentials** are correct
4. **Check resource limits** (e.g., VPC limits, instance limits)

### Stack Rollback

If deployment fails, CloudFormation will rollback:
1. Check **Events** tab in CloudFormation console
2. Identify failed resource
3. Fix the issue in code
4. Re-run deployment

### Clean Up Failed Stack

```bash
# Delete failed stack
aws cloudformation delete-stack --stack-name AIFilmStudio

# Wait for deletion
aws cloudformation wait stack-delete-complete --stack-name AIFilmStudio
```

## Next Steps

1. ✅ PostgreSQL version fixed (16.1)
2. ✅ CI/CD workflow created
3. ⏭️ Add GitHub secrets
4. ⏭️ Test deployment
5. ⏭️ Monitor and optimize

## Support

For issues:
- Check workflow logs in GitHub Actions
- Review CloudFormation events in AWS Console
- Check AWS CloudWatch logs
- Review `DEPLOYMENT_FIX.md` for common issues
