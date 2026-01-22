# 🚀 Deploy Now - Step by Step

## Quick Check: Are You Ready?

### ✅ Prerequisites Checklist

Before deploying, verify you have:

- [ ] **GitHub Secrets Configured:**
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_ACCOUNT_ID`
  - `AWS_REGION` (optional, defaults to us-east-1)

- [ ] **AWS Account Access:**
  - IAM user with deployment permissions
  - AWS CLI configured (for manual deployment)

## 🎯 Recommended: Deploy via GitHub Actions (Easiest)

### Step 1: Verify Secrets
1. Go to: `https://github.com/AI-Empower-HQ-360/AI-Film-Studio/settings/secrets/actions`
2. Verify these secrets exist:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_ACCOUNT_ID`

### Step 2: Trigger Deployment
1. Go to: `https://github.com/AI-Empower-HQ-360/AI-Film-Studio/actions`
2. Click on **"AWS CDK Deploy"** workflow
3. Click **"Run workflow"** button (top right)
4. Select:
   - **Environment:** `dev` (for first deployment)
   - **Action:** `deploy`
5. Click **"Run workflow"**

### Step 3: Monitor Progress
- Watch the workflow run in real-time
- Check each step:
  - ✅ Test Infrastructure
  - ✅ Synthesize CDK
  - ✅ Deploy to dev

**Expected Time:** 15-30 minutes

## 🔧 Alternative: Manual Deployment

If you prefer to deploy manually:

```powershell
# 1. Navigate to CDK directory
cd C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk

# 2. Activate Python virtual environment
.venv-cdk\Scripts\activate

# 3. Install dependencies (if not done)
pip install -r requirements.txt

# 4. Configure AWS (if not done)
aws configure

# 5. Preview changes
cdk diff

# 6. Deploy
cdk deploy --require-approval never
```

## 📊 What Happens During Deployment

1. **Infrastructure Tests** (2-3 min)
   - Validates CDK stack
   - Runs unit tests

2. **CDK Synthesis** (1-2 min)
   - Generates CloudFormation template
   - Validates configuration

3. **CDK Bootstrap** (if first time, 2-3 min)
   - Sets up CDK toolkit in AWS account

4. **Resource Creation** (10-20 min)
   - VPC and networking
   - RDS database
   - ECS cluster and service
   - Load balancer
   - S3 buckets
   - CloudFront
   - Other resources

## ✅ After Deployment

You'll receive:
- **Backend URL:** `http://ai-film-studio-alb-xxx.us-east-1.elb.amazonaws.com`
- **Database Endpoint:** `ai-film-studio-db-dev.xxx.us-east-1.rds.amazonaws.com`
- **CloudFront URL:** `https://d1234567890.cloudfront.net`
- **S3 Buckets:** Listed in stack outputs

## 🔍 Verify Deployment

```bash
# Check stack status
aws cloudformation describe-stacks --stack-name AIFilmStudio-dev

# Check ECS service
aws ecs describe-services --cluster ai-film-studio-cluster-dev --services ai-film-studio-backend-service-dev

# Check database
aws rds describe-db-instances --db-instance-identifier ai-film-studio-db-dev
```

## ⚠️ Troubleshooting

**If deployment fails:**

1. **Check GitHub Actions logs:**
   - Go to Actions → Failed workflow → View logs

2. **Common issues:**
   - **Missing secrets:** Add them in GitHub Settings
   - **IAM permissions:** Verify IAM user has required permissions
   - **AWS limits:** Check service quotas in AWS Console
   - **Region issues:** Ensure region is supported

3. **Check CloudFormation:**
   - Go to AWS Console → CloudFormation
   - View stack events for errors

## 💰 Cost Reminder

**Development Environment:** ~$60-100/month
- RDS: ~$15-20
- ECS: ~$10-15
- ALB: ~$16
- Other: ~$20-50

**You can stop/delete resources anytime to avoid charges.**

## 🎉 Ready?

**If you have GitHub secrets configured, you're ready to deploy!**

Go to: https://github.com/AI-Empower-HQ-360/AI-Film-Studio/actions

---

**Need help? Check:**
- `Deployment-Process/DETAILED_DEPLOYMENT_GUIDE.md`
- `Deployment-Process/DEPLOYMENT_READINESS.md`
- `QUICK_DEPLOY.md`
