# AWS Amplify Console Setup Guide

## Complete Step-by-Step AWS Console Configuration

This guide provides detailed instructions for setting up AWS Amplify through the AWS Console with screenshots references and exact navigation paths.

---

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] **AWS Account** with billing enabled
- [ ] **GitHub Account** with admin access to repository
- [ ] **IAM Permissions** (see [IAM_PERMISSIONS.md](./IAM_PERMISSIONS.md))
- [ ] **Domain Name** (optional, for custom domains)
- [ ] **API Endpoints** ready for each environment

**Minimum IAM Permissions Required:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "amplify:*",
        "cloudfront:*",
        "route53:*",
        "certificatemanager:*",
        "iam:PassRole"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## 🚀 Part 1: Initial App Setup (15 minutes)

### Step 1: Access AWS Amplify Console

1. **Log in to AWS Console**
   - Navigate to: https://console.aws.amazon.com/
   - Sign in with your AWS credentials

2. **Open Amplify Service**
   - In the search bar, type "Amplify"
   - Click **"AWS Amplify"** from the results
   - Or direct link: https://console.aws.amazon.com/amplify/home

3. **Select Region**
   - Top-right corner: Select **US East (N. Virginia) us-east-1**
   - ⚠️ Important: All environments should use the same region

### Step 2: Create New Amplify App

1. **Click "New app"** (orange button, top-right)
2. Select **"Host web app"**
3. You'll see these options:
   ```
   ○ GitHub
   ○ GitLab  
   ○ Bitbucket
   ○ AWS CodeCommit
   ○ Deploy without Git provider
   ```
4. **Select "GitHub"** → Click **"Continue"**

### Step 3: Authorize GitHub Integration

1. **GitHub Authorization Popup**
   - Click **"Authorize aws-amplify-console"**
   - Enter your GitHub password if prompted
   - Grant repository access

2. **Select Repository**
   - Organization: `AI-Empower-HQ-360`
   - Repository: `AI-Film-Studio`
   - Branch: `main`
   - Click **"Next"**

### Step 4: Configure Build Settings

**Build Settings Detection:**
Amplify will auto-detect `amplify.yml` in your repository.

**Manual Configuration (if needed):**

1. **App name:** `ai-film-studio-frontend`
2. **Branch:** `main`
3. **Build and test settings:**
   ```yaml
   version: 1
   frontend:
     phases:
       preBuild:
         commands:
           - cd frontend
           - npm ci
       build:
         commands:
           - npm run build
     artifacts:
       baseDirectory: frontend/.next
       files:
         - '**/*'
     cache:
       paths:
         - frontend/node_modules/**/*
   ```

4. **Advanced settings:**
   - Check **"Enable server-side rendering (SSR)"** ✅
   - Uncheck "Enable automatic builds for this branch" (temporarily)

5. **Service role:**
   - Select **"Create new role"** if first time
   - Or choose existing: `amplifyconsole-backend-role`

6. Click **"Next"** → **"Save and deploy"**

---

## ⚙️ Part 2: Environment Variables Configuration

### Step 1: Navigate to Environment Variables

1. In Amplify Console, click your app: **"ai-film-studio-frontend"**
2. Left sidebar: **"App settings"** → **"Environment variables"**
3. Click **"Manage variables"** button

### Step 2: Add Required Variables

**For Production (main branch):**

Click **"Add variable"** for each:

| Variable | Value | Description |
|----------|-------|-------------|
| `NODE_VERSION` | `18` | Node.js version |
| `NEXT_PUBLIC_API_URL` | `https://api-prod.aifilmstudio.com` | Backend API endpoint |
| `NEXT_PUBLIC_WS_URL` | `wss://api-prod.aifilmstudio.com` | WebSocket endpoint |
| `NEXT_PUBLIC_ENV` | `production` | Environment name |
| `NEXT_PUBLIC_ENABLE_ANALYTICS` | `true` | Enable analytics |
| `NEXT_PUBLIC_ENABLE_VIDEO_GENERATION` | `true` | Feature flag |
| `NEXT_PUBLIC_ENABLE_VOICE_SYNTHESIS` | `true` | Feature flag |
| `NEXT_PUBLIC_ENABLE_LIPSYNC` | `true` | Feature flag |
| `NEXT_PUBLIC_ENABLE_MUSIC_GENERATION` | `true` | Feature flag |
| `NEXT_PUBLIC_ENABLE_PODCAST_VIDEO` | `true` | Feature flag |
| `NEXT_PUBLIC_ENABLE_SUBTITLE_GENERATION` | `true` | Feature flag |

**Optional (Analytics & Monitoring):**

| Variable | Value | Description |
|----------|-------|-------------|
| `NEXT_PUBLIC_GOOGLE_ANALYTICS_ID` | `G-XXXXXXXXXX` | Google Analytics tracking ID |
| `NEXT_PUBLIC_SENTRY_DSN` | `https://xxx@xxx.ingest.sentry.io/xxx` | Sentry error tracking |
| `NEXT_PUBLIC_MIXPANEL_TOKEN` | `your_token_here` | Mixpanel analytics |

### Step 3: Save Variables

1. Click **"Save"** at the bottom
2. Variables are now available to all branches (override per branch later)

---

## 🌿 Part 3: Multi-Branch Deployments

### Step 1: Connect Additional Branches

1. **Navigate to App home** (click app name in breadcrumb)
2. Click **"Connect branch"** button
3. **Select branch:** `staging`
4. **Build settings:** Uses same `amplify.yml`
5. Click **"Save and deploy"**

**Repeat for:**
- `sandbox` branch
- `dev` branch

### Step 2: Configure Branch-Specific Variables

**For each branch:**

1. Go to **"App settings" → "Environment variables"**
2. Switch to **"Branch-specific overrides"** tab
3. Select branch (e.g., `staging`)
4. Click **"Add override"**

**Staging Branch Overrides:**
```bash
NEXT_PUBLIC_ENV=staging
NEXT_PUBLIC_API_URL=https://api-staging.aifilmstudio.com
NEXT_PUBLIC_WS_URL=wss://api-staging.aifilmstudio.com
NEXT_PUBLIC_ENABLE_ANALYTICS=false
```

**Sandbox Branch Overrides:**
```bash
NEXT_PUBLIC_ENV=sandbox
NEXT_PUBLIC_API_URL=https://api-sandbox.aifilmstudio.com
NEXT_PUBLIC_WS_URL=wss://api-sandbox.aifilmstudio.com
NEXT_PUBLIC_ENABLE_ANALYTICS=false
```

**Dev Branch Overrides:**
```bash
NEXT_PUBLIC_ENV=development
NEXT_PUBLIC_API_URL=https://api-dev.aifilmstudio.com
NEXT_PUBLIC_WS_URL=wss://api-dev.aifilmstudio.com
NEXT_PUBLIC_ENABLE_ANALYTICS=false
```

### Step 3: Verify Branch Deployments

After connecting branches, you should see:

```
✅ main      → https://main.d1234abcd5678.amplifyapp.com       (Production)
✅ staging   → https://staging.d1234abcd5678.amplifyapp.com    (Pre-prod)
✅ sandbox   → https://sandbox.d1234abcd5678.amplifyapp.com    (QA)
✅ dev       → https://dev.d1234abcd5678.amplifyapp.com        (Development)
```

---

## 🔒 Part 4: Custom Domain Setup

### Option A: Using Route 53 (Recommended)

1. **Navigate to Domain management**
   - Left sidebar: **"App settings" → "Domain management"**
   - Click **"Add domain"**

2. **Enter domain details**
   ```
   Domain: aifilmstudio.com
   ```
   - Amplify will detect if domain is in Route 53

3. **Configure subdomains**
   ```
   ✅ www.aifilmstudio.com          → main branch
   ✅ staging.aifilmstudio.com      → staging branch
   ✅ sandbox.aifilmstudio.com      → sandbox branch
   ✅ dev.aifilmstudio.com          → dev branch
   ```

4. **SSL Certificate**
   - Amplify automatically provisions ACM certificate
   - DNS validation (automatic if Route 53)
   - Wait 5-15 minutes for certificate

5. Click **"Save"**

### Option B: Using External DNS Provider

1. **Add domain in Amplify**
   - Enter: `aifilmstudio.com`
   - Click **"Continue"**

2. **Copy DNS records**
   Amplify will provide CNAME records:
   ```
   www.aifilmstudio.com     → d1234abcd5678.cloudfront.net
   staging.aifilmstudio.com → d1234abcd5678.cloudfront.net
   ```

3. **Add to your DNS provider** (GoDaddy, Namecheap, etc.)
   - Log in to DNS provider
   - Add CNAME records as provided
   - TTL: 300 seconds

4. **Verify in Amplify**
   - Wait 15-30 minutes for DNS propagation
   - Amplify will show: ✅ Domain verified

---

## 🔐 Part 5: Security Configuration

### Step 1: Custom Headers

Headers are configured in `amplify.yml`, but verify in Console:

1. **Navigate to:** "App settings" → "Rewrites and redirects"
2. Scroll to **"Custom headers"** section
3. Verify these headers are applied:

```yaml
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
```

### Step 2: Access Control (Optional)

**Enable password protection for non-production:**

1. **Navigate to:** "Access control"
2. Select branch: `dev` or `sandbox`
3. Click **"Manage access"**
4. Choose **"Restricted - password required"**
5. Set username/password:
   ```
   Username: aifilmstudio
   Password: [generate strong password]
   ```
6. Save

**Good for:**
- Protecting staging/dev environments
- Preventing unauthorized access
- Client preview links

---

## 📊 Part 6: Monitoring & Notifications

### Step 1: Enable Build Notifications

1. **Navigate to:** "Notifications"
2. Click **"Add notification"**

**Email Notifications:**
```
Email: deployments@aifilmstudio.com
Events:
  ✅ Build started
  ✅ Build succeeded
  ✅ Build failed
```

**Slack Notifications (if applicable):**
1. Generate Slack webhook: https://api.slack.com/messaging/webhooks
2. Add webhook URL to Amplify
3. Choose events (same as email)

### Step 2: CloudWatch Integration

**View logs in CloudWatch:**

1. In Amplify Console, click a deployment
2. Click **"View in CloudWatch"** link
3. Logs group: `/aws/amplify/ai-film-studio-frontend/main`

**Set up alarms (optional):**
```bash
aws cloudwatch put-metric-alarm \
  --alarm-name amplify-build-failures \
  --alarm-description "Alert on Amplify build failures" \
  --metric-name BuildFailures \
  --namespace AWS/Amplify \
  --statistic Sum \
  --period 300 \
  --threshold 1 \
  --comparison-operator GreaterThanThreshold
```

---

## 🧪 Part 7: PR Previews & Testing

### Enable Pull Request Previews

1. **Navigate to:** "Previews"
2. Toggle **"Enable pull request previews"** to ON
3. **Configure:**
   ```
   Base branch: main
   Preview expiration: 7 days
   ```

**How it works:**
- Every PR creates a preview URL
- Example: `https://pr-42.d1234abcd5678.amplifyapp.com`
- Automatically deleted when PR is merged/closed

**Best practices:**
- Use for QA review before merging
- Share with stakeholders
- Run automated tests on preview URLs

---

## 💾 Part 8: Performance Optimization

### Enable Build Caching

1. **Navigate to:** "Build settings"
2. **Build image settings:**
   ```
   Build image: Amazon Linux:2
   Node.js version: 18
   ```

3. **Cache settings (already in amplify.yml):**
   ```yaml
   cache:
     paths:
       - node_modules/**/*
       - .next/cache/**/*
   ```

4. **Build timeout:** 30 minutes (default)

### CloudFront Optimization

**Automatic optimizations:**
- ✅ GZIP compression
- ✅ HTTP/2 enabled
- ✅ Edge caching
- ✅ SSL/TLS 1.2+

**Manual optimizations:**
1. Go to **CloudFront console**
2. Find distribution ID (in Amplify → App details)
3. Edit **Behavior**:
   ```
   Cache policy: CachingOptimized
   Compress objects: Yes
   ```

---

## ✅ Final Verification Checklist

### Pre-Launch Checks

**Infrastructure:**
- [ ] All 4 branches connected and deploying
- [ ] Environment variables set for each branch
- [ ] Custom domain configured with SSL
- [ ] Build notifications enabled
- [ ] PR previews enabled

**Security:**
- [ ] HTTPS enforced (Strict-Transport-Security header)
- [ ] Security headers configured
- [ ] Access control on staging/dev (if desired)
- [ ] IAM roles properly scoped

**Performance:**
- [ ] Build caching enabled
- [ ] CloudFront distribution active
- [ ] Static asset caching configured
- [ ] Build times < 5 minutes

**Testing:**
- [ ] Test deployment on all branches
- [ ] Verify API connectivity on each environment
- [ ] Test custom domain resolution
- [ ] Check mobile responsiveness
- [ ] Verify all routes work (no 404s)

### Post-Launch Monitoring

**Week 1:**
- [ ] Monitor build success rate (target: >95%)
- [ ] Check CloudFront cache hit ratio
- [ ] Review CloudWatch logs for errors
- [ ] Test automated deployments on PR merge

**Ongoing:**
- [ ] Weekly review of build times
- [ ] Monthly review of AWS costs
- [ ] Quarterly security audit
- [ ] Update Node.js version as needed

---

## 🚨 Common Issues & Solutions

### Issue 1: Build Fails with "Module not found"

**Symptom:**
```
Error: Cannot find module 'next'
```

**Solution:**
1. Check `package.json` in `frontend/` directory
2. Verify `preBuild` commands in `amplify.yml`:
   ```yaml
   preBuild:
     commands:
       - cd frontend  # ← Critical!
       - npm ci
   ```
3. Re-deploy

### Issue 2: Environment Variables Not Loading

**Symptom:**
```
NEXT_PUBLIC_API_URL is undefined
```

**Solution:**
1. Go to **Environment variables** in Amplify Console
2. Verify variables start with `NEXT_PUBLIC_`
3. Check branch-specific overrides are applied
4. **Important:** Re-deploy after adding variables

### Issue 3: Custom Domain Shows "Pending Verification"

**Symptom:**
Domain stuck in "Pending" status for >30 minutes

**Solution:**
1. Check DNS records in your provider
2. Verify CNAME points to CloudFront distribution
3. Use `dig` to verify DNS:
   ```bash
   dig www.aifilmstudio.com +short
   ```
4. Wait up to 48 hours for full DNS propagation

### Issue 4: 404 on Page Refresh

**Symptom:**
Direct URL navigation works, but refresh shows 404

**Solution:**
1. Go to **"Rewrites and redirects"**
2. Add rule:
   ```
   Source: /<*>
   Target: /index.html
   Status: 404-200 (Rewrite)
   ```

---

## 📞 Getting Help

**AWS Support:**
- Console: https://console.aws.amazon.com/support
- Developer plan: $29/month (recommended)
- Business plan: $100/month (24/7 support)

**Community Resources:**
- Amplify Discord: https://discord.gg/amplify
- AWS Forums: https://forums.aws.amazon.com/forum.jspa?forumID=314
- Stack Overflow: Tag `aws-amplify`

**Internal Team:**
- Slack: #ai-film-studio-devops
- Email: devops@aifilmstudio.com

---

## 📚 Additional References

- [AWS Amplify Documentation](https://docs.aws.amazon.com/amplify/)
- [Next.js 14 Deployment Guide](https://nextjs.org/docs/deployment)
- [IAM Permissions Guide](./IAM_PERMISSIONS.md)
- [Backend API Setup](./AWS_BACKEND_SETUP.md)
- [Branching Strategy](../BRANCHING_STRATEGY.md)

---

*Last updated: January 2026*
*Maintained by: AI Film Studio DevOps Team*
