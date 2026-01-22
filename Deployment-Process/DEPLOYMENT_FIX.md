# PostgreSQL Version Fix & CI/CD Setup

## Issue
The deployment failed with error:
```
Cannot find version 15.3 for postgres (Service: Rds, Status Code: 400)
```

## Root Cause
PostgreSQL version 15.3 is not available in all AWS regions. The CDK code was using `VER_15_4` which may resolve to 15.3 in some cases, or the region doesn't support that specific minor version.

## Solution
Updated to PostgreSQL 16.1 which is widely available across all AWS regions:

```python
engine=rds.DatabaseInstanceEngine.postgres(
    version=rds.PostgresEngineVersion.VER_16_1  # Updated to widely available version
)
```

## CI/CD Automation

### GitHub Actions Workflow
Created `.github/workflows/aws-cdk-deploy.yml` with:

1. **Test Job**: Runs infrastructure tests before deployment
2. **Deploy Jobs**: Separate jobs for dev, staging, and production
3. **Manual Trigger**: Can be triggered manually with environment selection
4. **Auto Deploy**: 
   - `develop` branch → deploys to dev
   - `main` branch → deploys to production

### Required GitHub Secrets

Add these secrets to your GitHub repository:

#### Development:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_ACCOUNT_ID`

#### Staging (if different account):
- `AWS_ACCESS_KEY_ID_STAGING`
- `AWS_SECRET_ACCESS_KEY_STAGING`
- `AWS_ACCOUNT_ID_STAGING`

#### Production:
- `AWS_ACCESS_KEY_ID_PROD`
- `AWS_SECRET_ACCESS_KEY_PROD`
- `AWS_ACCOUNT_ID_PROD`

### Setup Instructions

1. **Add GitHub Secrets:**
   ```bash
   # Go to: Settings → Secrets and variables → Actions
   # Add all required secrets listed above
   ```

2. **Create IAM User for CI/CD:**
   ```bash
   # Create IAM user with CDK deployment permissions
   aws iam create-user --user-name github-actions-cdk
   
   # Attach CDK deployment policy
   aws iam attach-user-policy \
     --user-name github-actions-cdk \
     --policy-arn arn:aws:iam::aws:policy/PowerUserAccess
   ```

3. **Generate Access Keys:**
   ```bash
   aws iam create-access-key --user-name github-actions-cdk
   ```

4. **Bootstrap CDK (First Time):**
   ```bash
   cd infrastructure/aws-cdk
   cdk bootstrap aws://ACCOUNT-ID/us-east-1
   ```

### Deployment Workflow

#### Automatic Deployment:
- Push to `develop` → Deploys to dev environment
- Push to `main` → Deploys to production environment

#### Manual Deployment:
1. Go to Actions tab in GitHub
2. Select "AWS CDK Deploy" workflow
3. Click "Run workflow"
4. Select environment (dev/staging/production)
5. Select action (synth/diff/deploy/destroy)

### Workflow Features

- ✅ **Pre-deployment Testing**: Runs all infrastructure tests before deployment
- ✅ **CDK Diff**: Shows changes before deploying
- ✅ **Multi-environment**: Separate jobs for dev/staging/production
- ✅ **Manual Trigger**: Can be triggered manually with options
- ✅ **Stack Outputs**: Displays stack outputs after deployment
- ✅ **Error Handling**: Continues on bootstrap errors (already bootstrapped)

### Testing the Fix

1. **Verify PostgreSQL Version:**
   ```bash
   cd infrastructure/aws-cdk
   cdk synth
   # Check that VER_16_1 is used
   ```

2. **Test Locally:**
   ```bash
   cdk diff
   cdk deploy --require-approval never
   ```

3. **Test via CI/CD:**
   - Push changes to `develop` branch
   - Check GitHub Actions for deployment status

## Alternative PostgreSQL Versions

If PostgreSQL 16.1 is not available, try:
- `VER_15_4` (if available in your region)
- `VER_16_0`
- `VER_14_9` (older but stable)

To check available versions:
```bash
aws rds describe-db-engine-versions \
  --engine postgres \
  --query "DBEngineVersions[].EngineVersion" \
  --output table
```

## Next Steps

1. ✅ PostgreSQL version updated to 16.1
2. ✅ CI/CD workflow created
3. ⏭️ Add GitHub secrets
4. ⏭️ Test deployment via CI/CD
5. ⏭️ Monitor deployment status
