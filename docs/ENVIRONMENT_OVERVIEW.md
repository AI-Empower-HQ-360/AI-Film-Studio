# AI Film Studio - Environment Overview (Visual Summary)

This document provides a quick visual overview of the AI Film Studio environment setup.

---

## 🎯 Four-Tier Environment Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                     DEVELOPMENT ENVIRONMENT                      │
│  Purpose: Local coding and rapid prototyping                    │
│  Location: Developer laptop (localhost)                         │
│  Cost: $0-100/month                                             │
│                                                                  │
│  Components:                                                     │
│  ├── Frontend: Next.js (localhost:3000)                         │
│  ├── Backend: FastAPI (localhost:5000)                          │
│  ├── Database: PostgreSQL (Docker)                              │
│  ├── Cache: Redis (Docker)                                      │
│  └── AI: Mock responses or small models                         │
│                                                                  │
│  Features: Hot reload, fast iteration, no cloud costs           │
└─────────────────────────────────────────────────────────────────┘
                              ⬇
                      git push to develop
                              ⬇
┌─────────────────────────────────────────────────────────────────┐
│                   TESTING/QA ENVIRONMENT (Sandbox)               │
│  Purpose: Integration testing and QA validation                 │
│  Location: AWS Cloud (sandbox.ai-filmstudio.com)               │
│  Cost: ~$335/month                                              │
│                                                                  │
│  Components:                                                     │
│  ├── Frontend: S3 + CloudFront                                  │
│  ├── Backend: ECS Fargate (1-2 tasks)                           │
│  ├── Database: RDS db.t3.medium (single-AZ)                     │
│  ├── Cache: ElastiCache cache.t3.micro                          │
│  ├── AI: 1x g4dn.xlarge GPU worker                              │
│  └── Storage: S3 sandbox bucket (~100GB)                        │
│                                                                  │
│  Features: Auto-deploy, anonymized data, full AI pipeline       │
└─────────────────────────────────────────────────────────────────┘
                              ⬇
                     merge to main (approved)
                              ⬇
┌─────────────────────────────────────────────────────────────────┐
│                    STAGING ENVIRONMENT (Pre-Prod)                │
│  Purpose: Final validation before production                    │
│  Location: AWS Cloud (staging.ai-filmstudio.com)               │
│  Cost: ~$800-1,200/month                                        │
│                                                                  │
│  Components:                                                     │
│  ├── Frontend: S3 + CloudFront (full caching)                   │
│  ├── Backend: ECS Fargate (2-4 tasks, auto-scaled)              │
│  ├── Database: RDS db.r6g.large (Multi-AZ)                      │
│  ├── Cache: ElastiCache cache.r6g.large (Multi-AZ)              │
│  ├── AI: 1-3x g4dn.xlarge GPU workers (auto-scaled)             │
│  └── Storage: S3 staging bucket (~500GB, versioned)             │
│                                                                  │
│  Features: Production mirror, performance testing, VPC endpoints │
└─────────────────────────────────────────────────────────────────┘
                              ⬇
                    manual deploy (approved)
                              ⬇
┌─────────────────────────────────────────────────────────────────┐
│                     PRODUCTION ENVIRONMENT                       │
│  Purpose: Live platform serving real users                      │
│  Location: AWS Cloud (www.ai-filmstudio.com)                   │
│  Cost: ~$2,600/month                                            │
│                                                                  │
│  Components:                                                     │
│  ├── Frontend: S3 + CloudFront CDN (global, WAF enabled)        │
│  ├── Backend: ECS Fargate (4-50 tasks, auto-scaled)             │
│  ├── Database: RDS db.r6g.xlarge (Multi-AZ + 2 read replicas)   │
│  ├── Cache: ElastiCache cluster (Multi-AZ, 3 nodes)             │
│  ├── AI: 3-20x g4dn.xlarge GPU cluster (70% spot, auto-scaled)  │
│  └── Storage: S3 prod (multi-TB, Intelligent-Tiering, DR)       │
│                                                                  │
│  Features: HA, auto-scaling, monitoring, WAF, backups, DR       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Environment Comparison Matrix

| Aspect | Dev | Testing/QA | Staging | Production |
|--------|-----|-----------|---------|------------|
| **Purpose** | Coding | QA Testing | Final Validation | Live Users |
| **Access** | Local | Team | VPN Required | Public |
| **Cost/Month** | $0-100 | ~$335 | ~$1,000 | ~$2,600 |
| **Frontend** | localhost:3000 | S3 + CF Basic | S3 + CF Full | S3 + CF Global |
| **Backend Tasks** | 1 (local) | 1-2 | 2-4 | 4-50 |
| **Database** | Local Docker | db.t3.medium | db.r6g.large | db.r6g.xlarge |
| **GPU Workers** | Optional/Mock | 1 | 1-3 | 3-20 |
| **Auto-scaling** | ❌ | Limited | ✅ | ✅ Full |
| **Multi-AZ** | ❌ | ❌ | ✅ | ✅ |
| **Read Replicas** | ❌ | ❌ | ❌ | ✅ (2) |
| **Backups** | ❌ | 7 days | 14 days | 30 days + DR |
| **Monitoring** | Console logs | CloudWatch | CW + Alarms | Full Stack |
| **SSL/HTTPS** | ❌ | ✅ | ✅ | ✅ + WAF |
| **CDN** | ❌ | Basic | Full | Global |
| **Deployment** | Local | Auto | Manual | Manual + Approval |

---

## 🔄 Data Flow Visualization

### Code Deployment Flow

```
Developer
    │
    ├─── Write Code
    │
    ├─── Test Locally (Development)
    │
    ├─── Push to GitHub
    │
    ├─── CI Checks (Lint, Test, Build)
    │
    ├─── Create Pull Request
    │
    ├─── Code Review
    │
    ├─── Merge to 'develop'
    │
    ▼
Testing/QA Environment (Sandbox)
    │
    ├─── Auto Deploy
    │
    ├─── Integration Tests
    │
    ├─── QA Validation
    │
    ├─── Bug Fixes (if needed)
    │
    ├─── Merge to 'main'
    │
    ▼
Staging Environment
    │
    ├─── Manual Deploy Trigger
    │
    ├─── Full Test Suite
    │
    ├─── Performance Tests
    │
    ├─── Security Scan
    │
    ├─── Product Owner Approval
    │
    ▼
Production Environment
    │
    ├─── Manual Deploy (Blue-Green)
    │
    ├─── 10% Traffic → Monitor 10 min
    │
    ├─── 50% Traffic → Monitor 10 min
    │
    ├─── 100% Traffic → Complete
    │
    └─── Monitor for 1 hour
```

### User Request Flow (Production)

```
User
    │
    ├─── Request: Generate AI Video
    │
    ▼
CloudFront CDN (Edge)
    │
    ├─── Route API Call
    │
    ▼
Application Load Balancer
    │
    ├─── Distribute Traffic
    │
    ▼
ECS Backend (4-50 tasks)
    │
    ├─── Validate JWT Token
    │
    ├─── Check User Credits (RDS)
    │
    ├─── Create Job Record (RDS)
    │
    ├─── Enqueue Job (SQS)
    │
    ├─── Return Job ID
    │
    ▼
SQS Queue
    │
    ├─── Job Message
    │
    ▼
GPU Worker (3-20 instances)
    │
    ├─── Poll Queue
    │
    ├─── Load AI Model
    │
    ├─── Generate Video (30-90s)
    │
    ├─── Upload to S3
    │
    ├─── Update Job Status (RDS)
    │
    ├─── Publish Event (Redis)
    │
    └─── Delete SQS Message
    │
    ▼
User
    │
    ├─── Poll Job Status
    │
    ├─── Receive S3 URL
    │
    └─── Download Video (via CloudFront)
```

---

## 🛠️ Technology Stack by Environment

### Development
```
Frontend:   Next.js + React (localhost)
Backend:    FastAPI + Python 3.11 (localhost)
Database:   PostgreSQL 15 (Docker)
Cache:      Redis 7 (Docker)
AI:         Mock or lightweight models
Storage:    Local filesystem
Tools:      Docker Compose, hot reload
```

### Testing/QA
```
Frontend:   Next.js on S3 + CloudFront
Backend:    ECS Fargate (1-2 tasks)
Database:   RDS PostgreSQL db.t3.medium
Cache:      ElastiCache cache.t3.micro
AI:         g4dn.xlarge (1 instance)
Storage:    S3 sandbox bucket
Tools:      GitHub Actions, CloudWatch
```

### Staging
```
Frontend:   Next.js on S3 + CloudFront (full caching)
Backend:    ECS Fargate (2-4 tasks, auto-scaled)
Database:   RDS PostgreSQL db.r6g.large (Multi-AZ)
Cache:      ElastiCache cache.r6g.large (Multi-AZ)
AI:         g4dn.xlarge (1-3 instances, auto-scaled)
Storage:    S3 staging bucket (versioned)
Tools:      GitHub Actions, CloudWatch, Alarms
```

### Production
```
Frontend:   Next.js on S3 + CloudFront CDN (global)
Backend:    ECS Fargate (4-50 tasks, auto-scaled)
Database:   RDS PostgreSQL db.r6g.xlarge (Multi-AZ + 2 replicas)
Cache:      ElastiCache cluster (Multi-AZ, 3 nodes)
AI:         g4dn.xlarge cluster (3-20 instances, 70% spot)
Storage:    S3 production (Intelligent-Tiering, DR backup)
Tools:      GitHub Actions, CloudWatch, Prometheus, Grafana, X-Ray, PagerDuty
Security:   WAF, GuardDuty, Secrets Manager, KMS
```

---

## 💰 Cost Breakdown

```
Development:     $0-100/month
  └─ Mostly local, optional AWS sandbox

Testing/QA:      ~$335/month
  ├─ RDS db.t3.medium:        $72
  ├─ GPU Worker (40 hrs):     $21
  ├─ ECS Fargate:             $30
  ├─ ElastiCache:             $12
  ├─ Load Balancer:           $16
  ├─ NAT Gateway:             $37
  ├─ S3 + CloudFront:         $6
  └─ Other services:          $20

Staging:         ~$800-1,200/month
  ├─ RDS db.r6g.large:        $267
  ├─ GPU Workers (1-3):       $380
  ├─ ECS Fargate:             $60
  ├─ ElastiCache:             $99
  ├─ Load Balancer:           $33
  ├─ NAT Gateways:            $74
  ├─ S3 + CloudFront:         $25
  └─ Monitoring & other:      $50

Production:      ~$2,600/month
  ├─ RDS + Replicas:          $856
  ├─ GPU Workers (3-20):      $691
  ├─ ECS Fargate:             $120
  ├─ ElastiCache:             $199
  ├─ Load Balancer:           $33
  ├─ NAT Gateways:            $118
  ├─ S3 + CloudFront:         $297
  ├─ Backups & DR:            $60
  ├─ Monitoring:              $57
  └─ Security & other:        $170
```

---

## 🔐 Security Progression

```
Development
  └─ Basic security
  └─ Local credentials
  └─ No encryption

      ⬇

Testing/QA
  └─ HTTPS only
  └─ IAM roles
  └─ Security groups
  └─ Basic monitoring

      ⬇

Staging
  └─ IAM + MFA
  └─ Encryption at rest
  └─ VPC endpoints
  └─ CloudWatch alarms
  └─ Secrets Manager

      ⬇

Production
  └─ IAM + MFA + RBAC
  └─ Full encryption (rest + transit)
  └─ WAF + GuardDuty
  └─ 24/7 monitoring
  └─ Secrets rotation
  └─ Audit logging
  └─ Incident response
  └─ DR plan
```

---

## 📚 Documentation Links

- **[Complete Environment Setup](./docs/architecture/environments.md)** — Comprehensive 42KB guide
- **[Environment Diagrams](./docs/architecture/environment-diagram.md)** — Visual architecture (21KB)
- **[Quick Start Guide](./ENVIRONMENT_SETUP.md)** — Fast setup instructions (8KB)
- **[System Design](./docs/architecture/system-design.md)** — Overall architecture (38KB)

---

## 🚀 Quick Setup Commands

### Development (5 minutes)
```bash
cp .env.dev.example .env.dev
docker-compose up -d
cd backend && pip install -r requirements.txt
uvicorn src.main:app --reload &
cd ../frontend && npm install && npm run dev
```

### Testing/QA (Auto-deployed)
```bash
# Access: https://sandbox.ai-filmstudio.com
# Deployed automatically on merge to 'develop'
```

### Staging (Requires approval)
```bash
# Access: https://staging.ai-filmstudio.com
# Deploy via GitHub Actions after approval
```

### Production (Manual deployment)
```bash
# Access: https://www.ai-filmstudio.com
# Blue-green deployment with gradual rollout
```

---

**For detailed setup instructions, see [ENVIRONMENT_SETUP.md](./ENVIRONMENT_SETUP.md)**
