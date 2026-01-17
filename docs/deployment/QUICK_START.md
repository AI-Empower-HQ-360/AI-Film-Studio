# AWS Amplify Deployment - Quick Start

## 🚀 Deploy to AWS Amplify (5 Minutes)

### Method 1: AWS Console (Easiest)

1. **Go to AWS Amplify Console**
   ```
   https://console.aws.amazon.com/amplify/home?region=us-east-1
   ```

2. **Click "New app" → "Host web app"**

3. **Connect GitHub Repository**
   - Select "GitHub"
   - Authorize AWS Amplify
   - Choose: `AI-Empower-HQ-360/AI-Film-Studio`
   - Branch: `main`

4. **Configure Build Settings**
   - Amplify auto-detects `amplify.yml` ✅
   - Set **Base directory**: `frontend`
   - Click "Next"

5. **Add Environment Variables**
   ```
   NEXT_PUBLIC_API_URL=https://api-prod.aifilmstudio.com
   NODE_VERSION=18
   ```

6. **Click "Save and deploy"** 🎉

---

### What Gets Deployed?

- ✅ Next.js 14 frontend
- ✅ CloudFront CDN for global delivery
- ✅ SSL certificate (free)
- ✅ Auto-scaling
- ✅ CI/CD from GitHub pushes

### Your Deployment URL
```
https://main.d1234abcd5678.amplifyapp.com
```

---

## 📦 What Was Created

### 1. Configuration Files

| File | Purpose |
|------|---------|
| `amplify.yml` | Build configuration for Amplify |
| `frontend/.env.production` | Production environment variables |
| `frontend/.env.development` | Development environment variables |
| `docs/deployment/AMPLIFY_SETUP.md` | Complete deployment guide (14 KB) |
| `docs/deployment/AWS_BACKEND_SETUP.md` | Backend infrastructure guide (17 KB) |

### 2. Next.js Optimizations

Updated `frontend/next.config.mjs`:
- ✅ Standalone output for Amplify
- ✅ Image optimization with S3
- ✅ Security headers
- ✅ Performance optimizations

---

## 🌿 Multi-Branch Deployments

Deploy different environments automatically:

| Branch | URL | Purpose |
|--------|-----|---------|
| `main` | `main.d123.amplifyapp.com` | Production |
| `staging` | `staging.d123.amplifyapp.com` | Pre-production |
| `sandbox` | `sandbox.d123.amplifyapp.com` | QA testing |
| `dev` | `dev.d123.amplifyapp.com` | Development |

**To enable:**
1. Go to Amplify Console → Branches
2. Click "Connect branch"
3. Select branch (staging, sandbox, dev)

---

## 🔧 Backend Setup (Next Step)

Your frontend is deploying, but it needs a backend API!

### Option 1: Quick Start - S3 + Lambda
```bash
# Create S3 bucket for media storage
aws s3 mb s3://ai-film-studio-assets-prod --region us-east-1
```

### Option 2: Full Setup - ECS + RDS
See `docs/deployment/AWS_BACKEND_SETUP.md` for complete guide with:
- ✅ FastAPI on ECS Fargate
- ✅ PostgreSQL RDS database
- ✅ S3 for video/image storage
- ✅ SQS for job queue
- ✅ Secrets Manager for API keys

---

## 💰 Estimated Costs

### Frontend (Amplify)
- **Free Tier**: 1,000 build minutes/month
- **Production**: ~$5-15/month
- **Total All Environments**: ~$12-33/month

### Backend (Full Stack)
- **Dev Environment**: ~$50/month
- **Production**: ~$127/month
- See cost breakdown in `AWS_BACKEND_SETUP.md`

---

## ✅ Next Steps

### Immediate (Do Now)
1. ✅ Deploy frontend to Amplify (5 min)
2. ⏳ Create S3 bucket for media (2 min)
3. ⏳ Set up custom domain (optional, 10 min)

### Short-term (This Week)
4. ⏳ Deploy backend to ECS (1 hour)
5. ⏳ Set up RDS database (30 min)
6. ⏳ Configure API keys in Secrets Manager (15 min)

### Medium-term (This Month)
7. ⏳ Implement AI services (image, video, voice)
8. ⏳ Set up monitoring and alerting
9. ⏳ Configure auto-scaling

---

## 📚 Documentation Index

| Document | Size | Purpose |
|----------|------|---------|
| `AMPLIFY_SETUP.md` | 14 KB | Complete Amplify deployment guide |
| `AWS_BACKEND_SETUP.md` | 17 KB | ECS + RDS backend setup |
| `QUICK_START.md` | This file | Fast track to deployment |

---

## 🆘 Troubleshooting

### Build Failing?
```bash
# Check build logs in Amplify Console
# Common issues:
# 1. Node version mismatch → Set NODE_VERSION=18
# 2. Missing env vars → Add in Amplify Console
# 3. Build timeout → Contact AWS support
```

### Frontend Loads But No Data?
- Backend API not deployed yet
- Check `NEXT_PUBLIC_API_URL` environment variable
- Verify CORS settings on backend

---

## 🎉 Success Checklist

- [ ] Frontend deployed to Amplify
- [ ] Can access deployment URL
- [ ] S3 bucket created
- [ ] Backend API deployed (next step)
- [ ] Database configured
- [ ] API keys stored in Secrets Manager
- [ ] Custom domain configured (optional)

---

## 💬 Need Help?

- **AWS Support**: [console.aws.amazon.com/support](https://console.aws.amazon.com/support)
- **Amplify Discord**: [discord.gg/amplify](https://discord.gg/amplify)
- **GitHub Issues**: [github.com/AI-Empower-HQ-360/AI-Film-Studio/issues](https://github.com/AI-Empower-HQ-360/AI-Film-Studio/issues)
