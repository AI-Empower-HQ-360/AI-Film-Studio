# Branch Strategy Quick Reference

## 🌿 Available Branches

| Branch | Purpose | Deploy To | Auto-Deploy |
|--------|---------|-----------|-------------|
| `dev` | Active development | Dev AWS | ✅ Yes |
| `sandbox` | QA & Testing | Sandbox AWS | ✅ Yes (after QA approval) |
| `staging` | Pre-production | Staging AWS | ❌ Manual |
| `main` | Production | Production AWS | ❌ Manual (requires approvals) |

## 🔄 Common Workflows

### Creating a New Feature

```bash
# Start from dev
git checkout dev
git pull origin dev

# Create feature branch
git checkout -b feature/your-feature-name

# Work on your feature
git add .
git commit -m "feat: your feature description"

# Push and create PR to dev
git push origin feature/your-feature-name
```

### Promoting to Higher Environments

```bash
# Dev → Sandbox
git checkout sandbox
git pull origin sandbox
git merge dev
git push origin sandbox

# Sandbox → Staging (after QA approval)
git checkout staging
git pull origin staging
git merge sandbox
git push origin staging

# Staging → Production (requires multiple approvals)
git checkout main
git pull origin main
git merge staging
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin main --tags
```

### Hotfix to Production

```bash
# Create hotfix from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-fix

# Make fix
git add .
git commit -m "fix: critical bug"
git push origin hotfix/critical-fix

# Create PR to main
# After merge, backport to other branches
git checkout staging && git cherry-pick <commit>
git checkout sandbox && git cherry-pick <commit>
git checkout dev && git cherry-pick <commit>
```

## ✅ PR Approval Requirements

| Target Branch | Required Approvals | Status Checks | Special Requirements |
|---------------|-------------------|---------------|----------------------|
| `dev` | 1 | Unit tests | - |
| `sandbox` | 1 (QA team) | Unit + Integration tests | - |
| `staging` | 2 (DevOps/Release) | All tests + Security | Restricted push |
| `main` | 3 (including code owner) | All tests + Security + Performance | Signed commits, Restricted push |

## 📋 Deployment Checklist

### Before Deploying to Staging
- [ ] All tests passing in sandbox
- [ ] QA sign-off received
- [ ] Security scan clean
- [ ] Performance benchmarks met
- [ ] Documentation updated

### Before Deploying to Production
- [ ] All staging criteria met
- [ ] 48+ hours stable in staging
- [ ] Change management ticket created
- [ ] Rollback plan documented
- [ ] Stakeholders notified
- [ ] On-call team briefed
- [ ] Deployment window scheduled

## 🚨 Emergency Procedures

### Rollback Production
```bash
# Option 1: Revert via Git
git revert <bad-commit>
git push origin main

# Option 2: Switch traffic back to previous version
# (via AWS Console - Blue/Green deployment)

# Option 3: Deploy previous tagged version
git checkout v1.0.0
# Trigger deployment workflow
```

### Disable Feature (Feature Flag)
```bash
# Update feature flag in environment config
# Deploy config change (faster than code rollback)
```

## 📞 Support Contacts

| Issue | Contact | Channel |
|-------|---------|---------|
| Dev environment | Dev Team | #dev-environment |
| Sandbox issues | QA Team | #sandbox-environment |
| Staging/Prod | DevOps Team | #staging-production |
| Incidents | On-Call SRE | PagerDuty / #incidents |

## 📚 Full Documentation

- **Detailed Strategy**: [`docs/BRANCHING_STRATEGY.md`](./BRANCHING_STRATEGY.md)
- **Setup Guide**: [`docs/BRANCH_SETUP_GUIDE.md`](./BRANCH_SETUP_GUIDE.md)
- **Dev Environment**: [`docs/environments/BRANCH_DEV.md`](./environments/BRANCH_DEV.md)
- **Sandbox Environment**: [`docs/environments/BRANCH_SANDBOX.md`](./environments/BRANCH_SANDBOX.md)
- **Staging Environment**: [`docs/environments/BRANCH_STAGING.md`](./environments/BRANCH_STAGING.md)
- **Production Environment**: [`docs/environments/BRANCH_PRODUCTION.md`](./environments/BRANCH_PRODUCTION.md)

---

**Last Updated**: 2025-12-31
