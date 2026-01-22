# 🔌 Connection Guide - What You Need to Connect

## Overview

To complete deployment and use the AI Film Studio, you need to connect several components:

## 1. 🔐 GitHub Secrets (For CI/CD Deployment)

**Purpose:** Allow GitHub Actions to deploy to AWS

**Where to add:** GitHub → Settings → Secrets and variables → Actions → Repository secrets

**Required Secrets:**
```
AWS_ACCESS_KEY_ID          # From AWS IAM user
AWS_SECRET_ACCESS_KEY      # From AWS IAM user  
AWS_ACCOUNT_ID             # 996099991638 (your account)
AWS_REGION                 # us-east-1
```

**How to get:**
1. Create IAM user in AWS Console
2. Generate access key
3. Copy to GitHub Secrets

**Status:** ✅ You mentioned you stored keys - verify they're in GitHub

---

## 2. 🐳 Docker to ECR (For Building & Pushing Images)

**Purpose:** Build Docker images and push to ECR repositories

**Your ECR Repositories (Already Created):**
- ✅ `996099991638.dkr.ecr.us-east-1.amazonaws.com/ai-film-studio-backend-dev`
- ✅ `996099991638.dkr.ecr.us-east-1.amazonaws.com/ai-film-studio-worker-dev`

### Connect Docker to ECR:

**Step 1: Login to ECR**
```powershell
# Configure AWS CLI (if not done)
aws configure

# Login Docker to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 996099991638.dkr.ecr.us-east-1.amazonaws.com
```

**Step 2: Build Docker Image**
```powershell
cd C:\Users\ctrpr\Projects\AI-Film-Studio

# Build backend image
docker build -t ai-film-studio-backend:latest -f Dockerfile .

# Tag for ECR
docker tag ai-film-studio-backend:latest 996099991638.dkr.ecr.us-east-1.amazonaws.com/ai-film-studio-backend-dev:latest
```

**Step 3: Push to ECR**
```powershell
# Push backend image
docker push 996099991638.dkr.ecr.us-east-1.amazonaws.com/ai-film-studio-backend-dev:latest

# Push worker image (if needed)
docker build -t ai-film-studio-worker:latest -f Dockerfile.worker .
docker tag ai-film-studio-worker:latest 996099991638.dkr.ecr.us-east-1.amazonaws.com/ai-film-studio-worker-dev:latest
docker push 996099991638.dkr.ecr.us-east-1.amazonaws.com/ai-film-studio-worker-dev:latest
```

**Status:** ⏳ Need to login and push images

---

## 3. ☁️ AWS CLI Connection (For Manual Operations)

**Purpose:** Run AWS commands from your local machine

**Setup:**
```powershell
# Install AWS CLI (if not installed)
# Download from: https://aws.amazon.com/cli/

# Configure AWS CLI
aws configure

# Enter:
# AWS Access Key ID: [Your IAM user access key]
# AWS Secret Access Key: [Your IAM user secret key]
# Default region: us-east-1
# Default output format: json
```

**Test Connection:**
```powershell
# Test AWS connection
aws sts get-caller-identity

# Should return your account ID: 996099991638
```

**Status:** ⏳ Need to configure if not done

---

## 4. 🔑 API Keys (For AI Services)

**Purpose:** Enable AI features (image generation, voice synthesis, etc.)

**Required API Keys:**

### For Development:
- Optional (can use mock/fallback)

### For Production:
```
OPENAI_API_KEY          # From https://platform.openai.com/api-keys
STABILITY_AI_API_KEY    # From https://platform.stability.ai/account/keys
ELEVENLABS_API_KEY      # From https://elevenlabs.io/app/settings/api-keys
ANTHROPIC_API_KEY       # From https://console.anthropic.com/settings/keys
```

**Where to add:**
- **Local Development:** `.env` file (never commit!)
- **AWS Production:** AWS Secrets Manager or GitHub Secrets → production environment

**Status:** ⏳ Optional for dev, required for production

---

## 5. 🗄️ Database Connection (After Deployment)

**Purpose:** Connect to RDS PostgreSQL database

**After deployment completes, you'll get:**
```
Database Endpoint: ai-film-studio-db-dev.xxxxx.us-east-1.rds.amazonaws.com
Port: 5432
Database Name: ai_film_studio
Username: [from Secrets Manager]
Password: [from Secrets Manager]
```

**Connection String:**
```python
DATABASE_URL = "postgresql://username:password@ai-film-studio-db-dev.xxxxx.us-east-1.rds.amazonaws.com:5432/ai_film_studio"
```

**Get Credentials:**
```powershell
# Get database secret from AWS Secrets Manager
aws secretsmanager get-secret-value --secret-id ai-film-studio/database/dev --query SecretString --output text
```

**Status:** ⏳ Available after deployment completes

---

## 6. 🌐 Application Endpoints (After Deployment)

**Purpose:** Access deployed application

**After deployment, you'll get:**

1. **Backend API URL:**
   ```
   http://ai-film-studio-alb-xxxxx.us-east-1.elb.amazonaws.com
   ```

2. **CloudFront URL:**
   ```
   https://d1234567890.cloudfront.net
   ```

3. **Health Check:**
   ```
   http://[ALB-URL]/api/v1/health
   ```

**Status:** ⏳ Available after deployment completes

---

## 7. 📊 Monitoring Connections

**Purpose:** Monitor application health and logs

**AWS CloudWatch:**
- Automatically connected via IAM roles
- View logs: AWS Console → CloudWatch → Logs
- View metrics: AWS Console → CloudWatch → Metrics

**Status:** ✅ Automatic (no setup needed)

---

## 📋 Quick Connection Checklist

### Immediate (Before Deployment):
- [ ] **GitHub Secrets:** AWS credentials added
- [ ] **AWS CLI:** Configured locally
- [ ] **Docker:** Logged into ECR

### After Deployment:
- [ ] **Database:** Get connection string from Secrets Manager
- [ ] **Application URL:** Get from CloudFormation outputs
- [ ] **API Keys:** Add to AWS Secrets Manager (for production)

### Optional:
- [ ] **API Keys:** For local development (in `.env`)
- [ ] **Monitoring:** Set up CloudWatch dashboards

---

## 🚀 Quick Setup Commands

### 1. Configure AWS CLI
```powershell
aws configure
# Enter your IAM user credentials
```

### 2. Login Docker to ECR
```powershell
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 996099991638.dkr.ecr.us-east-1.amazonaws.com
```

### 3. Verify Connections
```powershell
# Test AWS
aws sts get-caller-identity

# Test ECR
aws ecr describe-repositories --repository-names ai-film-studio-backend-dev

# Test Docker
docker ps
```

---

## 🎯 What You Need Right Now

Since deployment is **CREATE_IN_PROGRESS**, you need:

1. **✅ GitHub Secrets** - Already stored (you mentioned this)
2. **⏳ Docker to ECR** - Login and push images when ready
3. **⏳ AWS CLI** - Configure for local operations
4. **⏳ Wait for Deployment** - Let CloudFormation finish (15-30 min)

---

## 📚 Related Guides

- **GITHUB_ENVIRONMENTS_SETUP.md** - GitHub secrets setup
- **ECR_SETUP_GUIDE.md** - ECR and Docker setup
- **DEPLOY_NOW_STEPS.md** - Deployment steps
- **CHECK_DEPLOYMENT_STATUS.md** - Check what's deployed

---

**Priority:** 
1. Wait for deployment to complete
2. Then connect Docker to ECR
3. Then configure AWS CLI
4. Then get database credentials
