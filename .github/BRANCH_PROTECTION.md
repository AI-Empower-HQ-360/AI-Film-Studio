# Branch Protection Rules for AI Film Studio

## Recommended Branch Protection Configuration

### 🔐 Main Branch (`main`) - Production

**Settings:**
| Rule | Value | Description |
|------|-------|-------------|
| Require PR before merging | ✅ Yes | All changes must go through PR |
| Required approving reviews | 1 | At least 1 approval needed |
| Dismiss stale reviews | ✅ Yes | Re-review after new commits |
| Require status checks | ✅ Yes | CI must pass |
| Required checks | `build`, `backend-test` | Must pass before merge |
| Require up-to-date branches | ✅ Yes | Branch must be current |
| Require signed commits | Optional | For security |
| Allow force pushes | ❌ No | Protect history |
| Allow deletions | ❌ No | Protect branch |

### 🧪 Staging Branch (`staging`) - Pre-Production

**Settings:**
| Rule | Value |
|------|-------|
| Require PR before merging | ✅ Yes |
| Required approving reviews | 1 |
| Require status checks | ✅ Yes |
| Allow force pushes | ❌ No |

### 🔧 Dev Branch (`dev`) - Development

**Settings:**
| Rule | Value |
|------|-------|
| Require status checks | ✅ Yes |
| Allow force pushes | ✅ Yes (for rebasing) |

---

## 🚀 How to Set Up (Manual Steps)

1. Go to: https://github.com/AI-Empower-HQ-360/AI-Film-Studio/settings/branches

2. Click **"Add branch protection rule"**

3. For `main` branch, configure:
   - Branch name pattern: `main`
   - ✅ Require a pull request before merging
     - ✅ Require approvals: 1
     - ✅ Dismiss stale pull request approvals when new commits are pushed
   - ✅ Require status checks to pass before merging
     - ✅ Require branches to be up to date before merging
     - Add required checks: `🏗️ Build Frontend`, `🐍 Backend Tests`
   - ✅ Do not allow bypassing the above settings
   - ❌ Allow force pushes (unchecked)
   - ❌ Allow deletions (unchecked)

4. Click **"Create"**

5. Repeat for `staging` and `dev` branches with appropriate settings.

---

## 📋 GitHub CLI Commands (Requires Admin Token)

If you have an admin token, you can run these commands:

```bash
# Main branch protection
gh api repos/AI-Empower-HQ-360/AI-Film-Studio/branches/main/protection \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  --input - << 'EOF'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["🏗️ Build Frontend", "🐍 Backend Tests"]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 1
  },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF
```

---

## 🔄 Workflow: dev → staging → main

```
Feature Branch
     │
     ▼ (PR + CI checks)
    dev ────────────────► Automatic deploy to Dev environment
     │
     ▼ (PR + 1 approval)
  staging ──────────────► Automatic deploy to Staging environment
     │
     ▼ (PR + 1 approval + all checks pass)
   main ────────────────► Automatic deploy to Production (GitHub Pages)
```
