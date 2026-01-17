# AWS Amplify Deployment Guide

## Overview

This guide walks through deploying the AI Film Studio frontend to AWS Amplify with automatic CI/CD from GitHub.

## Prerequisites

- AWS Account with Amplify access
- GitHub repository with admin access
- AWS CLI configured (optional, for advanced setup)

---

## 🚀 Quick Setup (10 minutes)

### Step 1: Create Amplify App via AWS Console

1. **Navigate to AWS Amplify Console**
   ```
   https://console.aws.amazon.com/amplify/home
   ```

2. **Click "New app" → "Host web app"**

3. **Connect Your Repository**
   - Select "GitHub"
   - Authorize AWS Amplify to access your repository
   - Choose repository: `AI-Empower-HQ-360/AI-Film-Studio`
   - Select branch: `main` (for production)

### Step 2: Configure Build Settings

Amplify will auto-detect `amplify.yml`. Verify the configuration:

```yaml
# Root: /workspaces/AI-Film-Studio
# Build commands: npm ci && npm run build
# Output directory: frontend/.next
```

**Important**: Set the "Base directory" to `frontend` in Amplify Console.

### Step 3: Set Environment Variables

Go to **App Settings → Environment variables** and add:

#### Required Variables
```bash
NEXT_PUBLIC_API_URL=https://api-prod.aifilmstudio.com
NEXT_PUBLIC_WS_URL=wss://api-prod.aifilmstudio.com
NEXT_PUBLIC_ENV=production
NODE_VERSION=18
```

#### Optional Variables (for analytics, monitoring)
```bash
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_ENABLE_SENTRY=true
SENTRY_DSN=your_sentry_dsn_here
```

### Step 4: Deploy

1. Click **"Save and deploy"**
2. Amplify will:
   - Clone your repository
   - Install dependencies (`npm ci`)
   - Build Next.js app (`npm run build`)
   - Deploy to CloudFront CDN
   - Provide a URL: `https://main.d1234abcd5678.amplifyapp.com`

---

## 🌿 Multi-Branch Deployments

### Enable Branch Deployments

Deploy different branches to separate environments:

| Branch | Environment | URL Pattern |
|--------|-------------|-------------|
| `main` | Production | `https://main.d123.amplifyapp.com` |
| `staging` | Staging | `https://staging.d123.amplifyapp.com` |
| `sandbox` | Sandbox/QA | `https://sandbox.d123.amplifyapp.com` |
| `dev` | Development | `https://dev.d123.amplifyapp.com` |

**Setup Steps:**
1. Go to **App Settings → General → Branch deployments**
2. Click **"Connect branch"**
3. Select branch: `staging`, `sandbox`, or `dev`
4. Set branch-specific environment variables

**Branch-Specific API URLs:**
```yaml
# main branch
NEXT_PUBLIC_API_URL=https://api-prod.aifilmstudio.com

# staging branch
NEXT_PUBLIC_API_URL=https://api-staging.aifilmstudio.com

# sandbox branch
NEXT_PUBLIC_API_URL=https://api-sandbox.aifilmstudio.com

# dev branch
NEXT_PUBLIC_API_URL=https://api-dev.aifilmstudio.com
```

---

## 🔒 Custom Domain Setup

### Add Custom Domain

1. Go to **App Settings → Domain management**
2. Click **"Add domain"**
3. Enter your domain: `www.aifilmstudio.com`
4. Amplify will:
   - Create SSL certificate (via ACM)
   - Configure DNS (if using Route 53)
   - Set up CloudFront distribution

### DNS Configuration

**If using Route 53:**
- Amplify auto-configures DNS records

**If using external DNS (GoDaddy, Namecheap, etc.):**
1. Copy the Amplify DNS records
2. Add CNAME records to your DNS provider:
   ```
   www.aifilmstudio.com → d1234abcd5678.cloudfront.net
   ```

### Branch-Specific Subdomains

```
main      → www.aifilmstudio.com
staging   → staging.aifilmstudio.com
sandbox   → sandbox.aifilmstudio.com
dev       → dev.aifilmstudio.com
```

---

## ⚙️ Advanced Configuration

### Build Performance Optimization

**1. Enable Build Cache**
```yaml
# Already configured in amplify.yml
cache:
  paths:
    - frontend/node_modules/**/*
    - frontend/.next/cache/**/*
```

**2. Parallel Builds**
- Amplify automatically parallelizes builds
- Typical build time: 3-5 minutes

**3. Build Image**
- Default: Amazon Linux 2
- Node.js 18 (specified in `amplify.yml`)

### Custom Headers (Security)

Already configured in `amplify.yml`:
- `Strict-Transport-Security` - Force HTTPS
- `X-Frame-Options` - Prevent clickjacking
- `X-Content-Type-Options` - Prevent MIME sniffing
- `Cache-Control` - Optimize static asset caching

### Rewrites and Redirects

**Add to Amplify Console → Rewrites and redirects:**

```json
[
  {
    "source": "/<*>",
    "target": "/index.html",
    "status": "404-200",
    "condition": null
  },
  {
    "source": "/api/<*>",
    "target": "https://api-prod.aifilmstudio.com/api/<*>",
    "status": "200",
    "condition": null
  }
]
```

---

## 🔄 CI/CD Workflow

### Automatic Deployments

Amplify automatically deploys when:
1. Code is pushed to connected branch
2. PR is merged to connected branch

**Deployment Process:**
1. Webhook triggered on GitHub push
2. Amplify clones repository
3. Runs build commands (`amplify.yml`)
4. Deploys to CloudFront
5. Sends notifications (optional)

### Build Notifications

**Set up Slack/Email notifications:**
1. Go to **App Settings → Notifications**
2. Add email or Slack webhook
3. Choose events:
   - Build started
   - Build succeeded
   - Build failed

### Manual Deployment

**Trigger manual deployment:**
```bash
# Using AWS CLI
aws amplify start-job \
  --app-id d1234abcd5678 \
  --branch-name main \
  --job-type RELEASE
```

---

## 📊 Monitoring & Analytics

### Access Logs

**View deployment logs:**
1. Go to **App → Branch → Build history**
2. Click on a deployment
3. View build logs in real-time

### Performance Monitoring

**Built-in metrics:**
- Build duration
- Deployment frequency
- Build success rate

**Amplify Console → Monitoring:**
- Request count
- Data transfer
- Error rates

### Integration with CloudWatch

Amplify logs are automatically sent to CloudWatch:
```bash
# View logs via CLI
aws logs tail /aws/amplify/d1234abcd5678/main --follow
```

---

## 🧪 Testing Deployments

### Preview Deployments for PRs

**Enable PR previews:**
1. Go to **App Settings → Previews**
2. Toggle **"Enable pull request previews"**
3. Every PR will get a unique URL:
   ```
   https://pr-123.d1234abcd5678.amplifyapp.com
   ```

**Use cases:**
- QA testing before merge
- Stakeholder review
- Visual regression testing

---

## 💰 Cost Optimization

### Amplify Pricing (US East 1)

**Build minutes:**
- Free tier: 1,000 minutes/month
- Additional: $0.01/minute

**Hosting:**
- Free tier: 15 GB storage + 15 GB data transfer
- Additional storage: $0.023/GB/month
- Additional transfer: $0.15/GB

**Estimated Monthly Costs:**
```
Production (main):     $5-15/month
Staging:               $3-8/month
Sandbox:               $2-5/month
Dev:                   $2-5/month
-----------------------------------
Total:                 $12-33/month
```

**Optimization tips:**
1. Use build caching (already configured)
2. Delete unused branches
3. Set up lifecycle policies for old builds
4. Use CloudFront edge locations wisely

---

## 🚨 Troubleshooting

### Build Failures

**Common issues:**

**1. Node version mismatch**
```yaml
# Solution: Specify in amplify.yml
env:
  variables:
    NODE_VERSION: '18'
```

**2. Missing environment variables**
```bash
# Check logs for: "NEXT_PUBLIC_API_URL is not defined"
# Solution: Add to Amplify Console → Environment variables
```

**3. Build timeout**
```bash
# Default timeout: 30 minutes
# Solution: Optimize build or contact AWS support
```

### Deployment Issues

**1. 404 on refresh**
```json
// Add rewrite rule in Amplify Console
{
  "source": "/<*>",
  "target": "/index.html",
  "status": "404-200"
}
```

**2. API calls failing (CORS)**
```bash
# Ensure backend API has CORS configured:
Access-Control-Allow-Origin: https://main.d123.amplifyapp.com
```

---

## 📚 Additional Resources

- [AWS Amplify Documentation](https://docs.aws.amazon.com/amplify/)
- [Next.js on Amplify](https://docs.aws.amazon.com/amplify/latest/userguide/deploy-nextjs-app.html)
- [Amplify CLI Reference](https://docs.amplify.aws/cli/)

---

## ✅ Deployment Checklist

### Pre-Deployment
- [ ] Verify `amplify.yml` is in repository root
- [ ] Test build locally: `cd frontend && npm run build`
- [ ] Update API URLs in environment variables
- [ ] Review security headers configuration
- [ ] Test on multiple branches (dev, staging, main)

### During Setup
- [ ] Connect GitHub repository to Amplify
- [ ] Set environment variables in Amplify Console
- [ ] Configure custom domain (if applicable)
- [ ] Enable PR previews
- [ ] Set up build notifications

### Post-Deployment
- [ ] Verify deployment at Amplify URL
- [ ] Test all pages and routes
- [ ] Check API connectivity
- [ ] Verify SSL certificate
- [ ] Set up monitoring and alerts
- [ ] Test on multiple devices/browsers

---

## 🆘 Support

**Need help?**
- AWS Support: [console.aws.amazon.com/support](https://console.aws.amazon.com/support)
- Amplify Discord: [discord.gg/amplify](https://discord.gg/amplify)
- GitHub Issues: [github.com/AI-Empower-HQ-360/AI-Film-Studio/issues](https://github.com/AI-Empower-HQ-360/AI-Film-Studio/issues)
