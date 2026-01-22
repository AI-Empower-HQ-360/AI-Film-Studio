# AI Film Studio - CI/CD Configuration Summary

## Overview

This document summarizes the **CI/CD pipeline configuration** for AI Film Studio, based on **GitHub Actions workflows** and **GitHub Pages** deployment.

---

## 🚀 CI/CD Workflows

### 1. **GitHub Pages Deployment** (Primary CI/CD)
**File:** `.github/workflows/deploy-pages.yml`

**Purpose:** Deploys static website to GitHub Pages

**Triggers:**
- Push to `main` branch
- Changes to `website/**` directory
- Manual trigger via `workflow_dispatch`

**Workflow:**
```
1. Checkout code
2. Setup Pages configuration
3. Upload website directory as artifact
4. Deploy to GitHub Pages
```

**Deployment URL:** Configured via GitHub Pages settings

**Permissions:**
- `contents: read`
- `pages: write`
- `id-token: write`

---

### 2. **Next.js GitHub Pages Deployment**
**File:** `.github/workflows/deploy.yml`

**Purpose:** Builds and deploys Next.js frontend to GitHub Pages

**Triggers:**
- Push to `main` branch

**Workflow:**
```
1. Checkout code
2. Setup Node.js 18
3. Configure Pages for Next.js
4. Install dependencies (npm ci)
5. Build Next.js app (npm run build)
6. Upload frontend/out as artifact
7. Deploy to GitHub Pages
```

**Output:** Next.js static export deployed to GitHub Pages

---

### 3. **Cloud Development Platform**
**File:** `.github/workflows/cloud-dev.yml`

**Purpose:** CI/CD for backend, infrastructure, and cloud deployment

**Triggers:**
- Push to any branch
- Pull requests
- Manual trigger

**Jobs:**

#### A. **CI Job** - Lint & Test
- Runs on: `ubuntu-latest`
- Python 3.12
- Installs dependencies from `requirements.txt`
- Runs pytest tests

#### B. **CD Job** - Build & Deploy (main only)
- **Condition:** Only runs on `main` branch if AWS secrets are configured
- Builds Docker image: `backend:${{ github.sha }}`
- **Placeholder:** Needs ECR_REPO_BACKEND, ECR_REPO_WORKER, S3_FRONTEND_BUCKET secrets
- **Current Status:** Deployment commands are placeholders

#### C. **Infra Job** - Terraform Plan/Apply
- **Condition:** Runs if AWS secrets are configured
- Terraform directory: `infrastructure/terraform/environments/dev`
- Runs `terraform init`, `terraform plan`
- Applies on `workflow_dispatch` (manual trigger)

**Required Secrets:**
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`

---

### 4. **CodeQL Security Scanning**
**File:** `.github/workflows/codeql.yml`

**Purpose:** Advanced security code analysis

**Triggers:**
- Push to `main` branch
- Pull requests to `main`
- Scheduled: Every Tuesday at 2:24 PM UTC

**Languages Analyzed:**
- Actions
- JavaScript/TypeScript
- Python

**Security Features:**
- Vulnerability detection
- Code quality analysis
- Security event reporting

---

### 5. **Environment Deployment**
**File:** `.github/workflows/environment-deployment.yml`

**Purpose:** Multi-environment deployment pipeline

**Triggers:**
- Push to: `dev`, `sandbox`, `staging`, `main`
- Manual trigger with environment selection

**Environments:**

| Branch | Environment | Deployment Type | URL |
|--------|-------------|----------------|-----|
| `dev` | Development | Automatic | https://dev.aifilmstudio.com |
| `sandbox` | Sandbox/QA | Automatic | https://sandbox.aifilmstudio.com |
| `staging` | Staging | Manual (approval) | https://staging.aifilmstudio.com |
| `main` | Production | Manual (approval) | https://aifilmstudio.com |

**Pipeline Stages:**

1. **Determine Environment** - Maps branch to environment
2. **Build and Test**
   - Setup Python 3.11
   - Free disk space
   - Install dependencies
   - Run unit tests (placeholder)
   - Run linting (placeholder)
3. **Deploy to Environment** - Environment-specific deployment
4. **Post-Deployment**
   - Integration tests (Sandbox)
   - Smoke tests (Staging)
   - Verification (Production)
   - Team notifications

**Deployment Strategy:**
- **Dev/Sandbox:** Automatic deployment
- **Staging/Production:** Requires manual approval
- **Production:** Creates deployment tags, blue-green/canary ready

---

## 📦 Build Configuration

### AWS Amplify (Legacy/Alternative)
**File:** `amplify.yml`

**Note:** This is configured for AWS Amplify, but the primary CI/CD is GitHub Pages.

**Features:**
- Multi-branch configuration (main, staging, sandbox, dev)
- Environment-specific variables
- Next.js build configuration
- Custom security headers
- Cache optimization

**Environments:**
- `main` → Production API URLs
- `staging` → Staging API URLs
- `sandbox` → Sandbox API URLs
- `dev` → Dev API URLs

---

## 🔐 Required Secrets

### GitHub Secrets (Settings → Secrets and variables → Actions)

**For Cloud Deployment:**
- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `AWS_REGION` - AWS region (default: us-east-1)

**For Full Deployment (Future):**
- `ECR_REPO_BACKEND` - ECR repository for backend
- `ECR_REPO_WORKER` - ECR repository for worker
- `S3_FRONTEND_BUCKET` - S3 bucket for frontend

---

## 📊 Current CI/CD Status

### ✅ Active Workflows

1. **GitHub Pages Deployment** - ✅ Active
   - Deploys `website/` directory
   - Triggered on push to `main`

2. **Next.js Deployment** - ✅ Active
   - Builds and deploys Next.js frontend
   - Triggered on push to `main`

3. **CodeQL Security** - ✅ Active
   - Security scanning on every push/PR

4. **Cloud Dev CI** - ✅ Active (CI only)
   - Runs tests on every push
   - CD requires AWS secrets

### ⚠️ Partial/Placeholder Workflows

1. **Cloud Dev CD** - ⚠️ Requires AWS secrets
   - Infrastructure deployment is placeholder
   - Needs ECR and S3 configuration

2. **Environment Deployment** - ⚠️ Deployment steps are placeholders
   - Structure is ready
   - Actual deployment commands need implementation

---

## 🎯 Deployment Targets

### GitHub Pages (Primary)
- **Static Website:** `website/` directory
- **Next.js Frontend:** `frontend/out` (static export)
- **URL:** Configured via GitHub Pages settings
- **Status:** ✅ Active

### AWS (Future)
- **Backend:** ECS/EKS (when secrets configured)
- **Frontend:** S3 + CloudFront (when configured)
- **Worker:** GPU instances (when configured)
- **Status:** ⚠️ Requires configuration

---

## 🔄 Workflow Triggers Summary

| Workflow | Trigger | Branch | Status |
|----------|---------|--------|--------|
| `deploy-pages.yml` | Push | `main` | ✅ Active |
| `deploy.yml` | Push | `main` | ✅ Active |
| `cloud-dev.yml` | Push/PR | All branches | ✅ CI Active |
| `codeql.yml` | Push/PR/Schedule | `main` | ✅ Active |
| `environment-deployment.yml` | Push | `dev/sandbox/staging/main` | ⚠️ Partial |

---

## 📝 Notes

1. **Primary CI/CD:** GitHub Pages workflows are the main CI/CD
2. **AWS Integration:** Cloud deployment workflows require AWS secrets configuration
3. **Environment Strategy:** Multi-environment support is structured but needs deployment implementation
4. **Static Site:** Current deployment is for static sites (website/ and Next.js export)
5. **Future Enhancements:** Backend/worker deployment needs ECR and infrastructure setup

---

## 🚀 Quick Start

### To Deploy to GitHub Pages:

1. **Static Website:**
   ```bash
   # Push to main branch
   git push origin main
   # Workflow: deploy-pages.yml will deploy website/ directory
   ```

2. **Next.js Frontend:**
   ```bash
   # Push to main branch
   git push origin main
   # Workflow: deploy.yml will build and deploy Next.js app
   ```

### To Enable Cloud Deployment:

1. Add AWS secrets to GitHub:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_REGION`

2. Configure additional secrets:
   - `ECR_REPO_BACKEND`
   - `ECR_REPO_WORKER`
   - `S3_FRONTEND_BUCKET`

3. Push to trigger deployment

---

## 📚 Related Documentation

- [Branching Strategy](./docs/BRANCHING_STRATEGY.md)
- [Environment Setup](./docs/environments/)
- [Deployment Guides](./docs/deployment/)
- [GitHub Pages Setup](./.github/workflows/deploy-pages.yml)
