# AI Film Studio Documentation

Welcome to the AI Film Studio documentation! This directory contains comprehensive guides and documentation for the project.

## 📚 Documentation Structure

### 🌿 Branching & Deployment Strategy

- **[BRANCHING_STRATEGY.md](./BRANCHING_STRATEGY.md)** - Complete branch strategy for CI/CD workflow
  - Branch overview and descriptions
  - Development workflow examples
  - Branch protection rules
  - Hotfix procedures
  - Environment mapping
  - Release tagging conventions

- **[BRANCH_SETUP_GUIDE.md](./BRANCH_SETUP_GUIDE.md)** - Step-by-step setup instructions
  - Creating environment branches
  - Configuring branch protection rules
  - Setting up GitHub environments
  - CODEOWNERS file setup
  - Verification checklist

- **[BRANCH_QUICK_REFERENCE.md](./BRANCH_QUICK_REFERENCE.md)** - Quick reference guide
  - Common workflows
  - PR approval requirements
  - Deployment checklists
  - Emergency procedures
  - Support contacts

### 🌍 Environment Documentation

The [`environments/`](./environments/) directory contains detailed documentation for each deployment environment:

- **[BRANCH_DEV.md](./environments/BRANCH_DEV.md)** - Development environment
  - Purpose and access details
  - Deployment process
  - Testing requirements
  - Configuration and monitoring

- **[BRANCH_SANDBOX.md](./environments/BRANCH_SANDBOX.md)** - Sandbox/QA environment
  - QA workflow
  - Testing focus areas
  - Integration with Salesforce Sandbox

- **[BRANCH_STAGING.md](./environments/BRANCH_STAGING.md)** - Staging environment
  - Pre-production validation
  - UAT procedures
  - Pre-deployment checklist
  - Rollback procedures

- **[BRANCH_PRODUCTION.md](./environments/BRANCH_PRODUCTION.md)** - Production environment
  - Deployment workflow
  - Incident response
  - Security requirements
  - SLA targets and monitoring
  - Disaster recovery

### 🏗️ Architecture

The [`architecture/`](./architecture/) directory contains system design and architecture documentation.

### 📋 Requirements

The [`requirements/`](./requirements/) directory contains business and functional requirements documentation.

## 🚀 Quick Start

### For Developers

1. Read the [Quick Reference Guide](./BRANCH_QUICK_REFERENCE.md) to understand the workflow
2. Review the [Development Environment Guide](./environments/BRANCH_DEV.md)
3. Follow the feature development workflow in [BRANCHING_STRATEGY.md](./BRANCHING_STRATEGY.md)

### For DevOps Engineers

1. Follow the [Branch Setup Guide](./BRANCH_SETUP_GUIDE.md) to create environment branches
2. Configure branch protection rules as documented
3. Set up GitHub environments with deployment secrets
4. Review environment-specific documentation for each deployment target

### For QA Engineers

1. Review the [Sandbox Environment Guide](./environments/BRANCH_SANDBOX.md)
2. Understand the QA workflow and testing requirements
3. Learn about PR approval responsibilities

### For Release Managers

1. Study the complete [Branching Strategy](./BRANCHING_STRATEGY.md)
2. Review [Staging](./environments/BRANCH_STAGING.md) and [Production](./environments/BRANCH_PRODUCTION.md) procedures
3. Understand deployment checklists and approval requirements
4. Familiarize yourself with rollback procedures

## 📖 Document Overview

### Branching Strategy Documents

| Document | Purpose | Audience |
|----------|---------|----------|
| BRANCHING_STRATEGY.md | Complete branch strategy and workflows | All team members |
| BRANCH_SETUP_GUIDE.md | Setup instructions for branch structure | DevOps, Admins |
| BRANCH_QUICK_REFERENCE.md | Quick reference for daily tasks | Developers, DevOps |

### Environment Documents

| Document | Environment | Audience |
|----------|-------------|----------|
| BRANCH_DEV.md | Development | Developers |
| BRANCH_SANDBOX.md | Testing/QA | QA Engineers, Developers |
| BRANCH_STAGING.md | Pre-production | DevOps, Release Managers |
| BRANCH_PRODUCTION.md | Production | Release Managers, SRE, DevOps |

## 🔄 Common Tasks

### Creating a Feature Branch
```bash
git checkout dev
git pull origin dev
git checkout -b feature/your-feature-name
```
📖 See: [BRANCH_QUICK_REFERENCE.md](./BRANCH_QUICK_REFERENCE.md)

### Promoting Between Environments
```bash
# Dev → Sandbox
git checkout sandbox
git merge dev
git push origin sandbox
```
📖 See: [BRANCHING_STRATEGY.md](./BRANCHING_STRATEGY.md#workflow-example)

### Deploying to Production
Review the complete checklist and procedure:
📖 See: [BRANCH_PRODUCTION.md](./environments/BRANCH_PRODUCTION.md)

## 🛡️ Branch Protection Overview

| Branch | Approvals | Status Checks | Special Rules |
|--------|-----------|---------------|---------------|
| dev | 1 | Unit tests | - |
| sandbox | 1 (QA) | Unit + Integration | - |
| staging | 2 | All tests + Security | Restricted push |
| main | 3 (+ code owner) | All + Performance | Signed commits |

📖 See: [BRANCH_SETUP_GUIDE.md](./BRANCH_SETUP_GUIDE.md#step-2-configure-branch-protection-rules)

## 🌍 Environment URLs

| Environment | Branch | URL |
|-------------|--------|-----|
| Development | dev | https://dev.aifilmstudio.com |
| Sandbox | sandbox | https://sandbox.aifilmstudio.com |
| Staging | staging | https://staging.aifilmstudio.com |
| Production | main | https://aifilmstudio.com |

## 🚨 Emergency Contacts

| Issue | Contact | Channel |
|-------|---------|---------|
| Dev environment | Dev Team | #dev-environment |
| Sandbox issues | QA Team | #sandbox-environment |
| Staging/Prod | DevOps Team | #staging-production |
| Production incidents | On-Call SRE | PagerDuty / #incidents |

## 🤝 Contributing to Documentation

To update or add documentation:

1. Create a feature branch from `dev`
2. Make your changes
3. Submit a PR with `docs:` prefix in commit message
4. Tag `@AI-Empower-HQ-360/tech-writers` for review

Example:
```bash
git checkout dev
git checkout -b feature/update-docs
# Make changes
git commit -m "docs: update branching strategy"
git push origin feature/update-docs
```

## 📅 Documentation Maintenance

- **Review Frequency**: Quarterly
- **Last Review**: 2025-12-31
- **Next Review**: 2026-03-31
- **Maintainer**: DevOps Team

## 📞 Support

If you have questions about any documentation:

- **Slack**: #documentation
- **Email**: docs@aifilmstudio.com
- **Wiki**: [Internal Wiki Link]

---

**Last Updated**: 2025-12-31  
**Version**: 1.0.0
