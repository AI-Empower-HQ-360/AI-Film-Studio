# AWS CDK Deployment Strategy for AI Film Studio

## Overview

This document explains how AWS CDK infrastructure **complements** the primary GitHub Pages deployment for AI Film Studio.

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Pages (Primary)                    │
│                  Frontend Static Hosting                     │
│         Automated via GitHub Actions on push                 │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ API Calls
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              AWS CDK Infrastructure (Backend)                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  CloudFront CDN → ALB → ECS Fargate (Backend API)   │   │
│  │  ┌──────────────────────────────────────────────┐   │   │
│  │  │  All 8 Engines (FastAPI)                     │   │   │
│  │  │  - Character Engine                          │   │   │
│  │  │  - Writing Engine                            │   │   │
│  │  │  - Production Management                     │   │   │
│  │  │  - Post-Production Engine                    │   │   │
│  │  │  - Marketing Engine                          │   │   │
│  │  │  - Enterprise Platform                       │   │   │
│  │  └──────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  GPU Workers (EC2)                                   │   │
│  │  - Video Generation                                  │   │
│  │  - Voice Synthesis                                   │   │
│  │  - AI Processing                                     │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Supporting Services                                 │   │
│  │  - RDS PostgreSQL (Database)                        │   │
│  │  - S3 Buckets (Assets, Characters, Marketing)       │   │
│  │  - SQS Queues (Job Processing)                      │   │
│  │  - ECR (Container Registry)                         │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Deployment Strategy

### Primary: GitHub Pages (Frontend)
- **Automatic** deployment on push to `main`
- **No cost** for public repositories
- **Fast** deployment (< 1 minute)
- **CDN** included (GitHub's CDN)
- **HTTPS** included
- **Triggered by:** GitHub Actions workflow

### Secondary: AWS CDK (Backend + Workers)
- **On-demand** deployment via workflow or manual
- **Cost:** ~$40-75/month (dev) to ~$400-1100/month (production)
- **Full control** over infrastructure
- **Scalable** for high traffic
- **GPU support** for AI processing
- **Triggered by:** Manual workflow dispatch or on infrastructure changes

## When to Deploy AWS CDK

### Deploy AWS CDK When:
1. ✅ Backend API needs to be hosted
2. ✅ GPU workers are needed for AI processing
3. ✅ Database persistence is required
4. ✅ High traffic/scalability needed
5. ✅ Enterprise features needed (multi-tenant, billing)

### Keep GitHub Pages When:
1. ✅ Frontend-only deployment
2. ✅ Low cost requirement
3. ✅ Simple static site
4. ✅ Fast deployment needed
5. ✅ Development/testing phase

## Deployment Workflow

### 1. Frontend (GitHub Pages) - Automatic
```yaml
Push to main → GitHub Actions → Build Next.js → Deploy to GitHub Pages
```

### 2. Backend (AWS CDK) - On Demand
```yaml
Manual trigger → Build Docker images → Push to ECR → Deploy via CDK → Update ECS
```

## Cost Comparison

### GitHub Pages Only (Frontend)
- **Cost:** $0 (free for public repos)
- **Limitations:** Frontend only, no backend, no AI processing

### GitHub Pages + AWS CDK (Full Stack)
- **GitHub Pages:** $0
- **AWS Backend:** ~$40-1100/month depending on usage
- **Benefits:** Full functionality, scalable, production-ready

## Configuration

### Environment Variables

**Frontend (GitHub Pages):**
```env
NEXT_PUBLIC_API_URL=https://your-alb-url.us-east-1.elb.amazonaws.com
```

**Backend (AWS):**
```env
DATABASE_URL=postgresql://...
ASSETS_BUCKET=ai-film-studio-assets-{env}
JOB_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/...
```

## Recommended Setup

### Development
- ✅ Frontend: GitHub Pages
- ✅ Backend: Local development or minimal AWS (single instance)

### Staging
- ✅ Frontend: GitHub Pages
- ✅ Backend: AWS CDK (dev environment)

### Production
- ✅ Frontend: GitHub Pages
- ✅ Backend: AWS CDK (production environment)
- ✅ Workers: GPU instances for AI processing

## Deployment Commands

### Deploy Frontend (Automatic)
```bash
git push origin main
# GitHub Actions automatically deploys to GitHub Pages
```

### Deploy Backend (AWS CDK)
```bash
cd infrastructure/aws-cdk
./deploy.sh dev us-east-1
# Or via GitHub Actions workflow
```

### Deploy Both (Full Stack)
```bash
# 1. Push frontend (auto-deploys)
git push origin main

# 2. Deploy backend infrastructure
cd infrastructure/aws-cdk
./deploy.sh production us-east-1

# 3. Build and push images
./build-and-push.sh production us-east-1
```

## Integration

The frontend (GitHub Pages) communicates with the backend (AWS) via:
- **API Gateway** or **ALB** endpoint
- **CORS** configured for GitHub Pages domain
- **Environment variables** in Next.js pointing to AWS endpoints

## Benefits of This Architecture

1. **Cost-effective:** Frontend free on GitHub Pages
2. **Flexible:** Backend scales as needed
3. **Fast:** Frontend deploys in < 1 minute
4. **Scalable:** Backend auto-scales on AWS
5. **Best of both:** GitHub simplicity + AWS power

## Next Steps

1. Deploy AWS CDK infrastructure
2. Configure frontend to point to backend URL
3. Build and push Docker images
4. Test end-to-end flow
5. Monitor costs and optimize

---

**This architecture gives you the best of both worlds:**
- **Simple, free frontend** on GitHub Pages
- **Powerful, scalable backend** on AWS
