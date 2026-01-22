# ✅ Environment Setup Checklist

Complete checklist for setting up all GitHub environments and secrets.

## 📋 Prerequisites

- [ ] AWS CLI installed and configured
- [ ] GitHub repository access
- [ ] AWS account with IAM permissions to create users
- [ ] AWS Account ID: `996099991638` (for dev/production)

---

## 🔐 Step 1: Repository-Level Secrets

**Location:** Settings → Secrets and variables → Actions → Repository secrets

- [ ] `AWS_REGION` = `us-east-1`

**How to add:**
1. Go to Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `AWS_REGION`, Value: `us-east-1`
4. Click "Add secret"

---

## 📁 Step 2: Create GitHub Environments

**Location:** Settings → Environments

Create these environments (if they don't exist):

- [ ] `dev`
- [ ] `development` (can reuse dev)
- [ ] `sandbox` (optional)
- [ ] `staging` (optional)
- [ ] `production`
- [ ] `github-pages` (auto-created)

**How to create:**
1. Go to Settings → Environments
2. Click "New environment"
3. Enter environment name
4. Click "Configure environment"
5. For production: Enable protection rules (require approval, restrict to main branch)

---

## 🔑 Step 3: Create AWS IAM Users

### Option A: Automated (Recommended)

Run the PowerShell script:

```powershell
cd Deployment-Process
.\create-iam-users.ps1 -CreateAll
```

This will create:
- `dev-deployer`
- `staging-deployer`
- `sandbox-deployer`
- `prod-deployer`

### Option B: Manual

Follow instructions in `GITHUB_ENVIRONMENTS_SETUP.md`

---

## 📝 Step 4: Add Secrets to Environments

### Environment: dev

**Location:** Settings → Environments → dev → Environment secrets

- [ ] `AWS_ACCESS_KEY_ID` (from `dev-deployer` IAM user)
- [ ] `AWS_SECRET_ACCESS_KEY` (from `dev-deployer` IAM user)
- [ ] `AWS_ACCOUNT_ID` = `996099991638`

**How to add:**
1. Go to Settings → Environments → dev
2. Scroll to "Environment secrets"
3. Click "Add secret"
4. Enter name and value
5. Click "Add secret"
6. Repeat for each secret

### Environment: development

**Location:** Settings → Environments → development → Environment secrets

- [ ] `AWS_ACCESS_KEY_ID` (same as dev, or create separate)
- [ ] `AWS_SECRET_ACCESS_KEY` (same as dev, or create separate)
- [ ] `AWS_ACCOUNT_ID` = `996099991638`

### Environment: sandbox (Optional)

**Location:** Settings → Environments → sandbox → Environment secrets

- [ ] `AWS_ACCESS_KEY_ID` (from `sandbox-deployer`)
- [ ] `AWS_SECRET_ACCESS_KEY` (from `sandbox-deployer`)
- [ ] `AWS_ACCOUNT_ID` (sandbox AWS account ID)
- [ ] `SALESFORCE_CLIENT_ID` (from Salesforce Connected App)
- [ ] `SALESFORCE_CLIENT_SECRET` (from Salesforce Connected App)

### Environment: staging (Optional)

**Location:** Settings → Environments → staging → Environment secrets

- [ ] `AWS_ACCESS_KEY_ID` (from `staging-deployer`)
- [ ] `AWS_SECRET_ACCESS_KEY` (from `staging-deployer`)
- [ ] `AWS_ACCOUNT_ID` (staging AWS account ID)

### Environment: production

**Location:** Settings → Environments → production → Environment secrets

- [ ] `AWS_ACCESS_KEY_ID` (from `prod-deployer`)
- [ ] `AWS_SECRET_ACCESS_KEY` (from `prod-deployer`)
- [ ] `AWS_ACCOUNT_ID` (production AWS account ID)
- [ ] `STABILITY_AI_API_KEY` (from stability.ai dashboard)
- [ ] `ELEVENLABS_API_KEY` (from elevenlabs.io dashboard)
- [ ] `OPENAI_API_KEY` (from platform.openai.com)

**Protection Rules (Important for Production):**
- [ ] Enable "Required reviewers" (add at least 1 reviewer)
- [ ] Enable "Deployment branches" → "Selected branches" → Add `main`
- [ ] Enable "Wait timer" (optional, recommended: 5 minutes)

### Environment: github-pages

**Location:** Settings → Environments → github-pages

- [ ] `GITHUB_TOKEN` (auto-provided, no setup needed)

---

## 🧪 Step 5: Test Configuration

### Test Dev Environment

1. [ ] Push to `develop` branch
2. [ ] Check GitHub Actions workflow runs
3. [ ] Verify deployment succeeds
4. [ ] Check AWS resources created

### Test Production Environment

1. [ ] Create PR to `main` branch
2. [ ] Verify workflow triggers
3. [ ] Check if approval is required (should be for production)
4. [ ] After approval, verify deployment

---

## 📊 Step 6: Verify Setup

### Check IAM Users

```bash
aws iam list-users --query "Users[?contains(UserName, 'deployer')].UserName" --output table
```

Expected output:
```
dev-deployer
staging-deployer
sandbox-deployer
prod-deployer
```

### Check GitHub Environments

1. Go to Settings → Environments
2. Verify all environments exist
3. Click on each environment
4. Verify secrets are added

### Check GitHub Secrets

```bash
# Via GitHub CLI (if installed)
gh secret list --env dev
gh secret list --env production
```

---

## 🔒 Step 7: Security Verification

### IAM User Permissions

- [ ] Dev/staging users have PowerUserAccess (or custom policy)
- [ ] Production user has restricted permissions
- [ ] All users have only necessary permissions

### GitHub Protection

- [ ] Production environment requires approval
- [ ] Production environment restricted to `main` branch
- [ ] Secrets are environment-specific (not repository-level for sensitive data)

### Access Key Security

- [ ] Access keys stored only in GitHub Secrets
- [ ] No access keys in code or logs
- [ ] Output file from script deleted after copying secrets

---

## 📚 Documentation

After setup, verify you have:

- [ ] `GITHUB_ENVIRONMENTS_SETUP.md` - Complete setup guide
- [ ] `create-iam-users.ps1` - Automated IAM user creation
- [ ] `ENVIRONMENT_SETUP_CHECKLIST.md` - This checklist
- [ ] `.github/workflows/aws-cdk-deploy.yml` - Updated workflow

---

## 🆘 Troubleshooting

### "Secret not found" in workflow
- [ ] Verify secret name matches exactly (case-sensitive)
- [ ] Check secret is in correct environment
- [ ] Ensure workflow references correct environment name

### "Access Denied" error
- [ ] Verify IAM user has correct permissions
- [ ] Check access key is active
- [ ] Verify AWS account ID matches

### Workflow doesn't trigger
- [ ] Check branch name matches workflow conditions
- [ ] Verify workflow file is in `.github/workflows/`
- [ ] Check workflow syntax is valid

---

## ✅ Completion Status

### Minimum Required (for basic deployment)
- [x] Repository secret: `AWS_REGION`
- [ ] Environment: `dev` with 3 secrets
- [ ] Environment: `production` with 3+ secrets
- [ ] IAM users: `dev-deployer`, `prod-deployer`

### Complete Setup (all environments)
- [ ] All environments created
- [ ] All secrets added
- [ ] All IAM users created
- [ ] Protection rules configured
- [ ] Tested and verified

---

## 🎯 Quick Reference

### Dev Environment Secrets
```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_ACCOUNT_ID = 996099991638
```

### Production Environment Secrets
```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_ACCOUNT_ID
STABILITY_AI_API_KEY
ELEVENLABS_API_KEY
OPENAI_API_KEY
```

### IAM Users to Create
```
dev-deployer
staging-deployer
sandbox-deployer
prod-deployer
```

---

**Last Updated:** 2026-01-22  
**Status:** Ready for setup
