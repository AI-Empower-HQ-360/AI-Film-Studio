# Branching Strategy & Merge Plan

## Branch Flow

```
feature/* → dev → sandbox → staging → main
              ↓       ↓         ↓        ↓
            Dev    QA/Test   Pre-prod  Production
```

## Current Status

### Feature Branch
- **Branch:** `feature/studio-operating-system`
- **Target:** `dev` (first merge)
- **Status:** Ready to merge

### Merge Sequence

1. **feature/studio-operating-system → dev**
   - Deploys to: **Dev** environment
   - Automatic deployment via GitHub Actions

2. **dev → sandbox**
   - Deploys to: **QA/Test** environment
   - Testing and QA validation

3. **sandbox → staging**
   - Deploys to: **Pre-production** environment
   - Final validation before production

4. **staging → main**
   - Deploys to: **Production** environment
   - Live user traffic

## PR Creation Plan

### PR 1: feature/studio-operating-system → dev
**URL:** https://github.com/AI-Empower-HQ-360/AI-Film-Studio/compare/dev...feature/studio-operating-system

**Title:** `feat: Enterprise Studio Operating System Architecture`

**After merge:** Auto-deploys to Dev environment

### PR 2: dev → sandbox (after PR 1 merged)
**URL:** https://github.com/AI-Empower-HQ-360/AI-Film-Studio/compare/sandbox...dev

**Title:** `chore: Promote to sandbox/QA environment`

**After merge:** Auto-deploys to QA/Test environment

### PR 3: sandbox → staging (after PR 2 merged)
**URL:** https://github.com/AI-Empower-HQ-360/AI-Film-Studio/compare/staging...sandbox

**Title:** `chore: Promote to staging/pre-production environment`

**After merge:** Auto-deploys to Pre-production environment

### PR 4: staging → main (after PR 3 merged)
**URL:** https://github.com/AI-Empower-HQ-360/AI-Film-Studio/compare/main...staging

**Title:** `chore: Release to production`

**After merge:** Auto-deploys to Production environment via GitHub Pages

## Deployment Environments

| Branch | Environment | Purpose | Auto-Deploy |
|--------|-------------|---------|-------------|
| `dev` | Development | Rapid development and testing | ✅ Yes |
| `sandbox` | QA/Test | Integration and QA testing | ✅ Yes |
| `staging` | Pre-production | Pre-production validation | ⚠️ Manual approval |
| `main` | Production | Live user traffic | ⚠️ Manual approval |

## What's in the Feature Branch

- ✅ 8 core engine modules
- ✅ AWS CDK infrastructure
- ✅ Complete documentation
- ✅ GitHub Actions workflows
- ✅ CI/CD configuration
- ✅ All blueprint requirements implemented

---

**Next Step:** Create PR 1 (feature → dev)
