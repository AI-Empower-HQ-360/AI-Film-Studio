# Environment Branches Setup Guide

This guide provides step-by-step instructions for creating and configuring the environment branches for the AI Film Studio project.

## Prerequisites

- Git installed on your local machine
- Write access to the AI Film Studio repository
- Administrator access to configure branch protection rules

## 🌿 Step 1: Create Environment Branches

The following branches need to be created from the `main` branch:

1. **dev** - Development environment
2. **sandbox** - Testing/QA environment
3. **staging** - Pre-production environment

### Option A: Create Branches via Git Command Line

Run the following commands from your local repository:

```bash
# Ensure you have the latest main branch
git checkout main
git pull origin main

# Create and push dev branch
git checkout -b dev
git push -u origin dev

# Create and push sandbox branch from main
git checkout main
git checkout -b sandbox
git push -u origin sandbox

# Create and push staging branch from main
git checkout main
git checkout -b staging
git push -u origin staging

# Verify all branches were created
git branch -r
```

### Option B: Create Branches via GitHub Web Interface

1. Go to https://github.com/AI-Empower-HQ-360/AI-Film-Studio
2. Click on the branch selector dropdown (shows "main" by default)
3. Type `dev` in the text field
4. Click "Create branch: dev from 'main'"
5. Repeat steps 2-4 for `sandbox` and `staging` branches

### Option C: Create Branches via GitHub CLI

```bash
# Install GitHub CLI if not already installed
# https://cli.github.com/

gh repo clone AI-Empower-HQ-360/AI-Film-Studio
cd AI-Film-Studio

# Create branches
git checkout main
git checkout -b dev && git push origin dev
git checkout main
git checkout -b sandbox && git push origin sandbox
git checkout main
git checkout -b staging && git push origin staging
```

## 🛡️ Step 2: Configure Branch Protection Rules

After creating the branches, configure protection rules for each branch to ensure code quality and safe deployments.

### For `dev` Branch

1. Go to: **Settings → Branches → Add rule**
2. Branch name pattern: `dev`
3. Configure:
   - ✅ Require pull request reviews before merging (1 approval)
   - ✅ Require status checks to pass before merging
     - Search and add: `build-and-test` (or your CI workflow name)
   - ✅ Require branches to be up to date before merging
   - ✅ Require conversation resolution before merging
4. Click **Create** or **Save changes**

### For `sandbox` Branch

1. Go to: **Settings → Branches → Add rule**
2. Branch name pattern: `sandbox`
3. Configure:
   - ✅ Require pull request reviews before merging (1 approval)
   - ✅ Require review from Code Owners (optional)
   - ✅ Require status checks to pass before merging
     - Add: `build-and-test`, `integration-tests`
   - ✅ Require branches to be up to date before merging
   - ✅ Dismiss stale pull request approvals when new commits are pushed
   - ✅ Require conversation resolution before merging
4. Click **Create** or **Save changes**

### For `staging` Branch

1. Go to: **Settings → Branches → Add rule**
2. Branch name pattern: `staging`
3. Configure:
   - ✅ Require pull request reviews before merging (2 approvals)
   - ✅ Require review from Code Owners
   - ✅ Require status checks to pass before merging
     - Add all relevant checks: `build-and-test`, `integration-tests`, `security-scan`
   - ✅ Require branches to be up to date before merging
   - ✅ Dismiss stale pull request approvals when new commits are pushed
   - ✅ Require conversation resolution before merging
   - ✅ Restrict who can push to matching branches
     - Add: Release Managers, DevOps team
   - ✅ Allow force pushes: **Disabled**
   - ✅ Allow deletions: **Disabled**
4. Click **Create** or **Save changes**

### For `main` Branch (Production)

1. Go to: **Settings → Branches → Add rule**
2. Branch name pattern: `main`
3. Configure:
   - ✅ Require pull request reviews before merging (3 approvals)
   - ✅ Require review from Code Owners
   - ✅ Require status checks to pass before merging
     - Add all checks: `build-and-test`, `integration-tests`, `e2e-tests`, `security-scan`, `performance-tests`
   - ✅ Require branches to be up to date before merging
   - ✅ Require signed commits
   - ✅ Dismiss stale pull request approvals when new commits are pushed
   - ✅ Require conversation resolution before merging
   - ✅ Restrict who can push to matching branches
     - Add: Release Managers, Administrators only
   - ✅ Require linear history
   - ✅ Include administrators (enforce for admins too)
   - ✅ Allow force pushes: **Disabled**
   - ✅ Allow deletions: **Disabled**
4. Click **Create** or **Save changes**

## 🔐 Step 3: Configure GitHub Environments

Set up deployment environments with protection rules and secrets:

### Create Dev Environment

1. Go to: **Settings → Environments → New environment**
2. Name: `dev`
3. Configure:
   - Environment protection rules: None (auto-deploy)
   - Environment secrets:
     - `AWS_ACCESS_KEY_ID` (Dev account)
     - `AWS_SECRET_ACCESS_KEY` (Dev account)
     - `DATABASE_URL` (Dev database)
4. Click **Save protection rules**

### Create Sandbox Environment

1. Go to: **Settings → Environments → New environment**
2. Name: `sandbox`
3. Configure:
   - Environment protection rules:
     - ✅ Required reviewers: Add QA team members (1 required)
     - ⏱️ Wait timer: 0 minutes
   - Environment secrets:
     - `AWS_ACCESS_KEY_ID` (Test account)
     - `AWS_SECRET_ACCESS_KEY` (Test account)
     - `DATABASE_URL` (Test database)
     - `SALESFORCE_SANDBOX_URL`
4. Click **Save protection rules**

### Create Staging Environment

1. Go to: **Settings → Environments → New environment**
2. Name: `staging`
3. Configure:
   - Environment protection rules:
     - ✅ Required reviewers: Add DevOps team and Release Managers (2 required)
     - ⏱️ Wait timer: 5 minutes
   - Environment secrets:
     - `AWS_ACCESS_KEY_ID` (Prod account - staging VPC)
     - `AWS_SECRET_ACCESS_KEY` (Prod account - staging VPC)
     - `DATABASE_URL` (Staging database)
4. Click **Save protection rules**

### Create Production Environment

1. Go to: **Settings → Environments → New environment**
2. Name: `production`
3. Configure:
   - Environment protection rules:
     - ✅ Required reviewers: Add Release Managers and Engineering Lead (3 required)
     - ⏱️ Wait timer: 15 minutes
     - 🔒 Deployment branches: Selected branches only → `main`
   - Environment secrets:
     - `AWS_ACCESS_KEY_ID` (Production account)
     - `AWS_SECRET_ACCESS_KEY` (Production account)
     - `DATABASE_URL` (Production database)
     - `DATABASE_REPLICA_URL` (Production read replica)
     - `SALESFORCE_PRODUCTION_URL`
4. Click **Save protection rules**

## 📋 Step 4: Set Up CODEOWNERS File

Create a `.github/CODEOWNERS` file to automatically request reviews from code owners:

```bash
# Create CODEOWNERS file
cat > .github/CODEOWNERS << 'EOF'
# CODEOWNERS file for AI Film Studio

# Default owners for everything in the repo
* @AI-Empower-HQ-360/engineering-team

# Infrastructure and DevOps
/infrastructure/ @AI-Empower-HQ-360/devops-team
/.github/workflows/ @AI-Empower-HQ-360/devops-team

# Backend
/backend/ @AI-Empower-HQ-360/backend-team
/src/ @AI-Empower-HQ-360/backend-team

# Worker/AI Pipeline
/worker/ @AI-Empower-HQ-360/ml-team
/py/ @AI-Empower-HQ-360/ml-team

# Documentation
/docs/ @AI-Empower-HQ-360/tech-writers

# Security-sensitive files
*.yml @AI-Empower-HQ-360/security-team
*.yaml @AI-Empower-HQ-360/security-team
Dockerfile @AI-Empower-HQ-360/security-team @AI-Empower-HQ-360/devops-team
EOF

# Commit and push
git add .github/CODEOWNERS
git commit -m "Add CODEOWNERS file"
git push origin main
```

## 🚀 Step 5: Update Default Branch (Optional)

If you want to make `dev` the default branch for development:

1. Go to: **Settings → General → Default branch**
2. Click the switch icon next to the current default branch
3. Select `dev` from the dropdown
4. Click **Update** and confirm

**Note**: It's common to keep `main` as the default branch to prevent accidental changes to production.

## ✅ Step 6: Verify Setup

Run this verification checklist:

```bash
# Clone the repository fresh
git clone https://github.com/AI-Empower-HQ-360/AI-Film-Studio.git
cd AI-Film-Studio

# Verify all branches exist
git branch -r

# Expected output:
# origin/dev
# origin/main
# origin/sandbox
# origin/staging

# Verify each branch is at the same commit as main initially
git show-ref --heads

# Test the workflow
git checkout dev
git checkout -b feature/test-workflow
echo "Test" >> test.txt
git add test.txt
git commit -m "test: verify workflow"
git push origin feature/test-workflow
# Create PR to dev branch on GitHub
```

## 📚 Step 7: Team Training

Ensure all team members understand the new workflow:

1. Share the `docs/BRANCHING_STRATEGY.md` document
2. Review environment-specific documentation in `docs/environments/`
3. Conduct a team meeting to explain:
   - When to use each branch
   - How to create feature branches
   - PR approval requirements
   - Deployment process
4. Set up Slack/Teams notifications for deployments

## 🎉 Completion

Once all steps are complete:

- ✅ All environment branches created
- ✅ Branch protection rules configured
- ✅ GitHub environments set up with protection rules
- ✅ CODEOWNERS file created
- ✅ Team trained on new workflow
- ✅ First test deployment successful

## 📞 Support

If you encounter issues during setup:

- Check: `docs/BRANCHING_STRATEGY.md` for detailed workflow information
- Consult: Individual branch documentation in `docs/environments/`
- Contact: DevOps team for assistance

---

**Setup completed**: `[DATE]`  
**Configured by**: `[YOUR_NAME]`  
**Last updated**: 2025-12-31
