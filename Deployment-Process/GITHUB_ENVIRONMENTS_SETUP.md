# 🔐 GitHub Environments & Secrets Configuration

Complete guide for setting up GitHub environments and secrets for multi-environment deployments.

## 📋 Overview

This project uses GitHub Environments to manage secrets and deployment configurations for different environments:

- **dev** / **development** - Development environment
- **sandbox** - QA/Salesforce integration testing
- **staging** - Pre-production UAT
- **production** - Live production
- **github-pages** - Static site deployment

---

## 🔐 Repository-Level Secrets (Shared)

These secrets are available to all environments:

| Secret Name | Value | Purpose |
|------------|-------|---------|
| `AWS_REGION` | `us-east-1` | Default AWS region for all deployments |

**How to add:**
1. Go to **Settings → Secrets and variables → Actions**
2. Click **"New repository secret"**
3. Add `AWS_REGION` with value `us-east-1`

---

## 📁 Environment: dev

**Used when:** Pushing to `develop` branch

| Secret Name | How to Get It | Purpose |
|------------|---------------|---------|
| `AWS_ACCESS_KEY_ID` | IAM → Users → `dev-deployer` → Security credentials | Deploy access |
| `AWS_SECRET_ACCESS_KEY` | Generated with access key | Deploy access |
| `AWS_ACCOUNT_ID` | `996099991638` | CDK deployment target |

**Setup Steps:**
1. Create IAM user: `dev-deployer` (see AWS IAM Setup section)
2. Generate access key
3. Go to **Settings → Environments → dev**
4. Add the three secrets above

---

## 📁 Environment: development

**Used when:** Development workflows (same as dev)

| Secret Name | How to Get It | Purpose |
|------------|---------------|---------|
| `AWS_ACCESS_KEY_ID` | Same as dev | Deploy access |
| `AWS_SECRET_ACCESS_KEY` | Same as dev | Deploy access |
| `AWS_ACCOUNT_ID` | `996099991638` | CDK deployment target |

**Note:** Can reuse dev secrets or create separate IAM user.

---

## 📁 Environment: sandbox

**Used when:** QA/Salesforce integration testing

| Secret Name | How to Get It | Purpose |
|------------|---------------|---------|
| `AWS_ACCESS_KEY_ID` | IAM → `sandbox-deployer` | Deploy access |
| `AWS_SECRET_ACCESS_KEY` | Generated with access key | Deploy access |
| `AWS_ACCOUNT_ID` | Sandbox AWS Account ID | CDK deployment |
| `SALESFORCE_CLIENT_ID` | Salesforce Connected App | SF integration |
| `SALESFORCE_CLIENT_SECRET` | Salesforce Connected App | SF integration |

**Setup Steps:**
1. Create IAM user: `sandbox-deployer`
2. Get Salesforce Connected App credentials
3. Go to **Settings → Environments → sandbox**
4. Add all secrets

---

## 📁 Environment: staging

**Used when:** Pre-production UAT environment

| Secret Name | How to Get It | Purpose |
|------------|---------------|---------|
| `AWS_ACCESS_KEY_ID` | IAM → `staging-deployer` | Deploy access |
| `AWS_SECRET_ACCESS_KEY` | Generated with access key | Deploy access |
| `AWS_ACCOUNT_ID` | Staging AWS Account ID | CDK deployment |

**Setup Steps:**
1. Create IAM user: `staging-deployer`
2. Go to **Settings → Environments → staging**
3. Add secrets

---

## 📁 Environment: production

**Used when:** Push to `main` branch (Live production)

| Secret Name | How to Get It | Purpose |
|------------|---------------|---------|
| `AWS_ACCESS_KEY_ID` | IAM → `prod-deployer` | Deploy access |
| `AWS_SECRET_ACCESS_KEY` | Generated with access key | Deploy access |
| `AWS_ACCOUNT_ID` | Production AWS Account ID | CDK deployment |
| `STABILITY_AI_API_KEY` | stability.ai dashboard | Image generation |
| `ELEVENLABS_API_KEY` | elevenlabs.io dashboard | Voice synthesis |
| `OPENAI_API_KEY` | platform.openai.com | AI features |

**Setup Steps:**
1. Create IAM user: `prod-deployer` (with restricted permissions)
2. Get API keys from respective services
3. Go to **Settings → Environments → production**
4. Add all secrets
5. **Enable protection rules** (require approval, restrict branches)

---

## 📁 Environment: github-pages

**Used when:** Static site deployment

| Secret Name | How to Get It | Purpose |
|------------|---------------|---------|
| `GITHUB_TOKEN` | Auto-provided by GitHub | Pages deployment |

**Note:** `GITHUB_TOKEN` is automatically provided by GitHub Actions, no setup needed.

---

## 🛠️ How to Add Secrets in GitHub

### Step 1: Navigate to Environments

1. Go to your GitHub repository
2. Click **Settings** (top menu)
3. Click **Environments** (left sidebar)
4. You'll see a list of environments

### Step 2: Create Environment (if doesn't exist)

1. Click **"New environment"**
2. Enter environment name (e.g., `dev`, `staging`, `production`)
3. Click **"Configure environment"**

### Step 3: Add Secrets to Environment

1. Click on the environment name (e.g., `dev`)
2. Scroll to **"Environment secrets"** section
3. Click **"Add secret"**
4. Enter:
   - **Name:** e.g., `AWS_ACCESS_KEY_ID`
   - **Value:** The actual secret value
5. Click **"Add secret"**
6. Repeat for all required secrets

### Step 4: Configure Protection Rules (Production Only)

For `production` environment:

1. Scroll to **"Deployment branches"**
2. Select **"Selected branches"**
3. Add: `main` (only main branch can deploy)
4. Scroll to **"Required reviewers"**
5. Add reviewers who must approve deployments
6. Save changes

---

## 🔑 Creating AWS IAM Users & Access Keys

### Option 1: Using AWS CLI (Automated)

See `create-iam-users.ps1` script for automated creation.

### Option 2: Using AWS Console (Manual)

#### Step 1: Create IAM User

1. Go to **AWS Console → IAM → Users**
2. Click **"Add users"**
3. Enter username: `dev-deployer` (or `staging-deployer`, `prod-deployer`, etc.)
4. Select **"Provide user access to the AWS Management Console"** (optional)
5. Click **"Next"**

#### Step 2: Set Permissions

**For dev/staging/sandbox:**
- Attach policy: **PowerUserAccess** (full access except IAM)

**For production:**
- Create custom policy with minimal required permissions (see below)
- Or use **PowerUserAccess** with additional restrictions

**Custom Production Policy (Recommended):**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudformation:*",
        "ec2:*",
        "ecs:*",
        "rds:*",
        "s3:*",
        "cloudfront:*",
        "sqs:*",
        "sns:*",
        "elasticache:*",
        "secretsmanager:*",
        "iam:PassRole",
        "iam:GetRole"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Deny",
      "Action": [
        "iam:CreateUser",
        "iam:DeleteUser",
        "iam:CreateRole",
        "iam:DeleteRole"
      ],
      "Resource": "*"
    }
  ]
}
```

#### Step 3: Create Access Key

1. Click on the user name
2. Go to **"Security credentials"** tab
3. Scroll to **"Access keys"** section
4. Click **"Create access key"**
5. Select **"Command Line Interface (CLI)"**
6. Click **"Next"**
7. Add description (optional)
8. Click **"Create access key"**
9. **⚠️ IMPORTANT:** Copy both:
   - **Access key ID** → GitHub secret: `AWS_ACCESS_KEY_ID`
   - **Secret access key** → GitHub secret: `AWS_SECRET_ACCESS_KEY`
10. Click **"Done"**

**⚠️ Warning:** The secret access key is shown only once. Save it immediately!

---

## ✅ Quick Setup Checklist

### Repository-Level Secrets
- [ ] `AWS_REGION` = `us-east-1`

### Environment: dev
- [ ] Create IAM user: `dev-deployer`
- [ ] Generate access key
- [ ] Add `AWS_ACCESS_KEY_ID` to GitHub
- [ ] Add `AWS_SECRET_ACCESS_KEY` to GitHub
- [ ] Add `AWS_ACCOUNT_ID` = `996099991638` to GitHub

### Environment: production
- [ ] Create IAM user: `prod-deployer`
- [ ] Generate access key
- [ ] Add `AWS_ACCESS_KEY_ID` to GitHub
- [ ] Add `AWS_SECRET_ACCESS_KEY` to GitHub
- [ ] Add `AWS_ACCOUNT_ID` to GitHub
- [ ] Add `STABILITY_AI_API_KEY` to GitHub
- [ ] Add `ELEVENLABS_API_KEY` to GitHub
- [ ] Add `OPENAI_API_KEY` to GitHub
- [ ] Enable protection rules (require approval)
- [ ] Restrict to `main` branch only

### Environment: sandbox (Optional)
- [ ] Create IAM user: `sandbox-deployer`
- [ ] Add AWS secrets
- [ ] Add Salesforce secrets

### Environment: staging (Optional)
- [ ] Create IAM user: `staging-deployer`
- [ ] Add AWS secrets

---

## 🔒 Security Best Practices

1. **Separate IAM Users:** Use different IAM users for each environment
2. **Least Privilege:** Give only necessary permissions
3. **Rotate Keys:** Rotate access keys every 90 days
4. **Protect Production:** Require approvals for production deployments
5. **Restrict Branches:** Only allow `main` branch to deploy to production
6. **Audit Logs:** Monitor CloudTrail for access patterns
7. **Use Secrets Manager:** Store sensitive data in AWS Secrets Manager when possible

---

## 🧪 Testing Secrets

After adding secrets, test them:

```bash
# Test dev environment secrets (via GitHub Actions)
# Push to develop branch and check workflow runs

# Test production secrets (via GitHub Actions)
# Create PR to main and verify workflow
```

---

## 📚 Related Documentation

- **AWS IAM Setup:** See `create-iam-users.ps1` script
- **CI/CD Workflow:** See `.github/workflows/aws-cdk-deploy.yml`
- **Deployment Guide:** See `DETAILED_DEPLOYMENT_GUIDE.md`

---

## 🆘 Troubleshooting

### "Secret not found" error
- Verify secret name matches exactly (case-sensitive)
- Check you're using the correct environment
- Ensure secret is added to the right environment

### "Access Denied" error
- Check IAM user has correct permissions
- Verify access key is active
- Check AWS account ID matches

### "Environment not found" error
- Create the environment in GitHub Settings → Environments
- Ensure workflow references correct environment name

---

**Last Updated:** 2026-01-22
