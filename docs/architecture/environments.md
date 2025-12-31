# AI Film Studio – Complete Environment Setup

**Version:** 1.0  
**Last Updated:** 2025-12-31  
**Document Owner:** AI-Empower-HQ-360

---

## Table of Contents

1. [Overview](#overview)
2. [Environments Summary](#environments-summary)
3. [Environment Details](#environment-details)
4. [Environment Services Mapping](#environment-services-mapping)
5. [Environment Interactions](#environment-interactions)
6. [Configuration Management](#configuration-management)
7. [Access & Security](#access--security)
8. [Deployment Process](#deployment-process)

---

## Overview

This document provides a complete environment setup plan for AI Film Studio, including all environments, their purpose, storage, compute resources, and interactions. This ensures the development team can run, test, and deploy the platform safely and efficiently.

### Environment Strategy

AI Film Studio uses a **four-tier environment strategy** to ensure safe development, thorough testing, and reliable production deployment:

1. **Development (Dev)** — Local and sandbox development
2. **Testing / QA (Sandbox)** — Integrated testing and validation
3. **Staging / Pre-Production** — Final pre-deployment validation
4. **Production (Prod)** — Live platform for end users

---

## Environments Summary

| Environment | Purpose | Key Characteristics | Hosting |
|-------------|---------|---------------------|---------|
| **Development (Dev)** | Local development and feature coding | • Rapid iteration<br/>• Local or minimal cloud resources<br/>• Isolated testing<br/>• No real user data | • Local DB<br/>• Local Docker<br/>• AWS dev sandbox (optional)<br/>• S3 dev bucket |
| **Testing / QA (Sandbox)** | Feature testing, user simulation, AI workflow validation | • Mimics production<br/>• Isolated from prod<br/>• Anonymized data<br/>• Full AI pipeline testing | • PostgreSQL RDS (small)<br/>• S3 sandbox bucket<br/>• GPU EC2 (t4 small)<br/>• Redis sandbox |
| **Staging / Pre-Prod** | Pre-deployment environment for final QA | • Production mirror<br/>• Full integration<br/>• Performance testing<br/>• Final validation | • Same architecture as prod<br/>• EC2 GPU<br/>• RDS multi-AZ<br/>• S3 + CloudFront<br/>• Full API endpoints |
| **Production (Prod)** | Live platform for users | • Highly available<br/>• Scalable<br/>• Secure<br/>• Monitored 24/7<br/>• Real user data | • EC2 GPU cluster<br/>• RDS multi-AZ<br/>• S3 + CloudFront CDN<br/>• Load balancer<br/>• Full monitoring |

---

## Environment Details

### 1️⃣ Development Environment

**Purpose:** Local development, feature coding, unit testing, and rapid prototyping.

#### Infrastructure

```yaml
Frontend:
  Technology: React + Next.js
  Hosting: localhost:3000
  Hot Reload: Enabled
  Build Tool: Webpack / Vite
  Environment Variables: .env.local

Backend:
  Technology: FastAPI + Python 3.11
  Hosting: localhost:5000 or localhost:8000
  Server: Uvicorn with auto-reload
  Environment Variables: .env.dev

Database:
  Type: PostgreSQL 15
  Hosting: 
    - Option 1: Local instance (Docker)
    - Option 2: AWS RDS db.t3.micro (free tier)
  Connection: localhost:5432
  Schema: Development schema with test data
  Migrations: Alembic

File Storage:
  Option 1: Local filesystem (./data/uploads)
  Option 2: AWS S3 dev bucket (ai-film-studio-dev-{account})
  Access: Local path or S3 presigned URLs

AI Models:
  Approach: 
    - Lightweight models for testing
    - Mock responses for rapid development
    - Small GPU instance (g4dn.xlarge) for full testing
  Model Cache: Local directory (./models)
  GPU: Optional, CUDA enabled for local testing

Cache / Queue:
  Redis: 
    - Docker container (localhost:6379)
    - Or ElastiCache dev instance
  SQS: 
    - LocalStack for local development
    - Or AWS SQS dev queue

Container Management:
  Docker: Version 24+
  Docker Compose: Multi-service orchestration
  Services: Backend, Worker, Redis, PostgreSQL
```

#### Development Workflow

```yaml
Setup Steps:
  1. Clone repository
  2. Install dependencies (npm, pip)
  3. Copy .env.example to .env.dev
  4. Start Docker services (docker-compose up)
  5. Run database migrations
  6. Start backend server
  7. Start frontend dev server
  8. Access: http://localhost:3000

Daily Workflow:
  - Code changes auto-reload
  - Unit tests run locally
  - Commit to feature branch
  - Push to GitHub for CI checks
  - Create PR for code review

Resource Usage:
  - CPU: 4 cores recommended
  - RAM: 8GB minimum, 16GB recommended
  - Storage: 50GB for models and data
  - GPU: Optional, for AI testing
```

---

### 2️⃣ Testing / QA (Sandbox) Environment

**Purpose:** Safe testing environment for QA engineers and developers to validate features, simulate user actions, and test AI workflows without affecting production.

#### Infrastructure

```yaml
Frontend:
  Hosting: AWS S3 + CloudFront
  URL: https://sandbox.ai-filmstudio.com
  Deployment: Automated via GitHub Actions
  Build: Next.js static export
  CDN: CloudFront distribution (minimal config)

Backend:
  Hosting: AWS ECS Fargate
  Instance: 1-2 tasks (1 vCPU, 2GB RAM)
  Load Balancer: Application Load Balancer
  URL: https://api-sandbox.ai-filmstudio.com
  Container: Docker image from ECR
  Scaling: Manual or minimal auto-scaling

Database:
  Type: Amazon RDS PostgreSQL 15
  Instance: db.t3.medium (2 vCPU, 4GB RAM)
  Storage: 100GB gp3 SSD
  Multi-AZ: No (cost saving)
  Backups: Daily, 7-day retention
  Data: Anonymized test data, refreshed weekly

File Storage:
  Bucket: ai-film-studio-sandbox-{region}
  Region: us-east-1
  Storage Class: S3 Standard
  Lifecycle: Delete objects > 30 days
  Access: IAM roles, presigned URLs
  Size: Up to 100GB

AI Models & GPU:
  Instance Type: g4dn.xlarge (NVIDIA T4, 16GB)
  Count: 1 instance (on-demand)
  Scaling: Manual start/stop to save costs
  Models: Same versions as production
  Model Storage: S3 model cache bucket
  Usage: On-demand for testing, scaled to 0 when idle

Cache & Queue:
  Redis: ElastiCache (cache.t3.micro)
  SQS: Dedicated sandbox queue
  Usage: Session storage, API caching, job queue

Networking:
  VPC: Dedicated sandbox VPC or shared dev VPC
  Subnets: Public (ALB) + Private (ECS, RDS)
  Security Groups: Restricted access
  NAT Gateway: Single NAT for cost optimization
```

#### Testing Workflow

```yaml
Deployment Process:
  1. Merge feature branch to 'develop'
  2. GitHub Actions triggers sandbox deployment
  3. Docker image built and pushed to ECR
  4. ECS service updated with new image
  5. Database migrations run automatically
  6. Smoke tests execute
  7. QA team notified

Testing Activities:
  - Feature validation
  - Integration testing
  - API endpoint testing (Postman/Swagger)
  - AI pipeline testing (text → video generation)
  - User workflow simulation
  - Performance testing (limited)

Tools & Access:
  - Swagger UI: https://api-sandbox.ai-filmstudio.com/docs
  - Postman collections for API testing
  - Test user accounts with various roles
  - Monitoring: CloudWatch logs and basic metrics

Data Management:
  - Anonymized production data snapshot (optional)
  - Synthetic test data
  - Data refresh: Weekly or on-demand
  - No PII or sensitive data
```

---

### 3️⃣ Staging / Pre-Production Environment

**Purpose:** Final QA and validation before production deployment. This environment mirrors production architecture and is used for end-to-end testing, performance validation, and deployment rehearsal.

#### Infrastructure

```yaml
Frontend:
  Hosting: AWS S3 + CloudFront
  URL: https://staging.ai-filmstudio.com
  Deployment: Blue-green deployment strategy
  Build: Production-optimized build
  CDN: CloudFront with full caching rules
  SSL: ACM certificate (*.ai-filmstudio.com)

Backend:
  Hosting: AWS ECS Fargate or EKS
  Instance: 2-4 tasks (1 vCPU, 2GB RAM each)
  Load Balancer: Application Load Balancer
  URL: https://api-staging.ai-filmstudio.com
  Auto-scaling: Enabled (min: 2, max: 8)
  Health Checks: /health endpoint (30s interval)

Database:
  Type: Amazon RDS PostgreSQL 15
  Instance: db.r6g.large (2 vCPU, 16GB RAM)
  Storage: 500GB gp3 SSD, 3000 IOPS
  Multi-AZ: Yes (high availability)
  Backups: Daily automated, 14-day retention
  Snapshots: Before each deployment
  Data: Production-like schema with test data

File Storage:
  Bucket: ai-film-studio-staging-{region}
  Region: us-east-1
  Storage Class: S3 Standard
  Versioning: Enabled
  Encryption: SSE-S3 (AES-256)
  Lifecycle: Transition to IA after 30 days
  CDN: CloudFront distribution

AI Models & GPU:
  Instance Type: g4dn.xlarge or g4dn.2xlarge
  Count: 1-3 instances (auto-scaled)
  Scaling: Based on SQS queue depth
  Strategy: 50% on-demand, 50% spot
  Models: Production versions
  Model Storage: Shared S3 model repository

Cache & Queue:
  Redis: 
    - ElastiCache (cache.r6g.large)
    - Multi-AZ replication
  SQS: 
    - Dedicated staging queue
    - Dead-letter queue enabled

Networking:
  VPC: Dedicated staging VPC
  CIDR: 10.1.0.0/16
  Subnets: 
    - Public (2 AZs): ALB, NAT Gateway
    - Private App (2 AZs): ECS, GPU workers
    - Private Data (2 AZs): RDS, ElastiCache
  Security Groups: Production-equivalent rules
  VPC Endpoints: S3, SQS, ECR, Secrets Manager

Monitoring:
  CloudWatch: Logs, metrics, alarms
  Log Retention: 30 days
  Alarms: CPU, memory, error rates
  Dashboards: Custom CloudWatch dashboards
```

#### Staging Workflow

```yaml
Deployment Process:
  1. All tests pass in sandbox environment
  2. Create release candidate tag
  3. Deploy to staging via GitHub Actions
  4. Run database migration (with rollback plan)
  5. Execute automated test suite
  6. Perform manual QA checklist
  7. Load testing (optional)
  8. Obtain approval for production deployment

Validation Activities:
  - End-to-end workflow testing
  - Full AI pipeline validation
  - Payment integration testing (test mode)
  - YouTube upload simulation
  - Email notification testing
  - Performance benchmarking
  - Security scanning
  - Disaster recovery testing

Approval Gates:
  - All automated tests pass
  - Manual QA sign-off
  - Performance metrics acceptable
  - No critical bugs
  - Security scan clean
  - Product owner approval

Rollback Plan:
  - Database snapshot before migration
  - Previous ECS task definition preserved
  - Blue-green deployment allows instant rollback
  - S3 versioning for frontend assets
```

---

### 4️⃣ Production Environment

**Purpose:** Live platform serving real users with high availability, security, scalability, and 24/7 monitoring.

#### Infrastructure

```yaml
Frontend:
  Hosting: AWS S3 + CloudFront CDN
  URL: https://www.ai-filmstudio.com
  Deployment: Blue-green with gradual rollout
  Build: Fully optimized production build
  CDN: 
    - Global edge locations (225+)
    - Custom caching rules
    - Gzip + Brotli compression
    - Origin Shield enabled
  SSL: ACM certificate with auto-renewal
  WAF: AWS WAF for DDoS protection

Backend:
  Hosting: AWS ECS Fargate or Amazon EKS
  Instance: 4-10 tasks (1 vCPU, 2GB RAM each)
  Load Balancer: 
    - Application Load Balancer (multi-AZ)
    - SSL termination
    - Health checks: 30s interval
  URL: https://api.ai-filmstudio.com
  Auto-scaling: 
    - Min: 4 tasks
    - Max: 50 tasks
    - Metrics: CPU 70%, Memory 80%
  Container: 
    - Multi-stage Docker build
    - Scanned for vulnerabilities
    - Optimized for performance

Database:
  Type: Amazon RDS PostgreSQL 15
  Instance: db.r6g.xlarge (4 vCPU, 32GB RAM)
  Storage: 500GB gp3 SSD, 5000 IOPS
  Multi-AZ: Yes (automatic failover)
  Read Replicas: 1-2 (for read scaling)
  Backups: 
    - Automated daily backups
    - 30-day retention
    - Point-in-time recovery (5 min intervals)
    - Cross-region backup (us-west-2)
  Encryption: 
    - At rest: KMS encryption
    - In transit: TLS 1.2+
  Connection Pooling: PgBouncer or SQLAlchemy pool

File Storage:
  Primary Bucket: ai-film-studio-prod-{region}
  Region: us-east-1
  Storage Classes:
    - S3 Standard: Recent content
    - S3 Intelligent-Tiering: Auto-optimization
  Versioning: Enabled
  Encryption: SSE-S3 (AES-256)
  Lifecycle Policies:
    - Standard → IA: 30 days
    - IA → Glacier: 90 days
  Replication: 
    - Cross-region to us-west-2
    - For disaster recovery
  CDN: CloudFront for fast global delivery
  Access: 
    - IAM roles (least privilege)
    - Presigned URLs for uploads
    - Bucket policies enforced

AI Models & GPU:
  Instance Type: g4dn.xlarge or g4dn.2xlarge
  Count: 3-20 instances (auto-scaled)
  Scaling: 
    - Metric: SQS queue depth
    - Scale up: Queue > 10 messages
    - Scale down: Queue < 2 messages
    - Warm-up time: 300 seconds
  Strategy: 
    - 30% on-demand (stable baseline)
    - 70% spot instances (cost optimization)
  Spot Handling: 
    - Graceful shutdown on interruption
    - Job requeue to SQS
  Models: 
    - Stable Diffusion XL
    - Custom LoRA models
    - Video generation models
  Model Storage: S3 with CloudFront

Cache & Queue:
  Redis: 
    - ElastiCache (cache.r6g.large)
    - Cluster mode enabled
    - Multi-AZ: 2 replicas
    - Encryption: In-transit and at-rest
  SQS: 
    - Production job queue
    - Visibility timeout: 300s
    - Dead-letter queue: 3 retries
    - Message retention: 14 days

Networking:
  VPC: Dedicated production VPC
  CIDR: 10.0.0.0/16
  Subnets: 
    - Public (2 AZs): 10.0.1.0/24, 10.0.2.0/24
    - Private App (2 AZs): 10.0.10.0/24, 10.0.11.0/24
    - Private Data (2 AZs): 10.0.20.0/24, 10.0.21.0/24
  Availability Zones: us-east-1a, us-east-1b
  NAT Gateways: 2 (one per AZ for HA)
  VPC Endpoints: 
    - S3 (gateway endpoint)
    - SQS, Secrets Manager, ECR (interface endpoints)
  Security Groups: 
    - Defense in depth
    - Least privilege access
    - Separate SGs per service tier

Monitoring & Logging:
  CloudWatch:
    - Logs: Centralized logging
    - Metrics: System and custom metrics
    - Alarms: Critical and warning alerts
    - Dashboards: Real-time visibility
  Log Retention: 90 days
  Metrics Retention: 15 months
  Distributed Tracing: AWS X-Ray (optional)
  Alerting: 
    - PagerDuty for critical alerts
    - Email for warnings
    - Slack for info notifications

Security:
  WAF: 
    - Rate limiting (100 req/5min per IP)
    - SQL injection protection
    - XSS protection
    - Geo-blocking (optional)
  Secrets: AWS Secrets Manager
  Encryption: 
    - At rest: All storage encrypted
    - In transit: TLS 1.2+ everywhere
  IAM: 
    - Least privilege policies
    - Role-based access control
    - MFA for admin access
  Compliance: 
    - AWS GuardDuty enabled
    - AWS Config rules
    - Regular security audits
```

#### Production Operations

```yaml
Deployment Process:
  1. Staging validation complete
  2. Create production release tag
  3. Schedule deployment window
  4. Create database backup snapshot
  5. Deploy using blue-green strategy:
     - Deploy to "green" environment
     - Run smoke tests
     - Gradually shift traffic (10%, 25%, 50%, 100%)
     - Monitor metrics during rollout
     - Instant rollback if issues detected
  6. Monitor for 1 hour post-deployment
  7. Document deployment in runbook

Monitoring & Alerts:
  Critical Alerts (PagerDuty, immediate):
    - API error rate > 1%
    - Database CPU > 90%
    - ECS task failures
    - GPU worker crashes
    - Payment processing failures
  
  Warning Alerts (Email, 15 min):
    - API latency > 2 seconds
    - SQS queue depth > 100
    - Memory utilization > 85%
    - Disk space < 20%
  
  Info Alerts (Slack):
    - Deployment events
    - Auto-scaling events
    - Daily metrics summary

Maintenance Windows:
  Scheduled: Sunday 2:00-4:00 AM UTC
  Frequency: Monthly
  Activities:
    - Database maintenance
    - OS patching
    - Certificate renewals
    - Performance optimization

Incident Response:
  Severity 1 (Critical):
    - Response: Immediate (24/7)
    - Escalation: 15 minutes
    - Communication: Status page, email
  
  Severity 2 (High):
    - Response: 1 hour
    - Escalation: 2 hours
    - Communication: Slack, email
  
  Severity 3 (Medium):
    - Response: Next business day
    - Communication: Internal only

Backup & Recovery:
  RTO (Recovery Time Objective): 1 hour
  RPO (Recovery Point Objective): 15 minutes
  
  Recovery Procedures:
    - Database: Multi-AZ failover (auto)
    - Application: Blue-green rollback (5 min)
    - Region failure: DR in us-west-2 (1 hour)

Cost Management:
  Monthly Budget: $2,600
  Alerts: 80%, 90%, 100% of budget
  Optimization:
    - Spot instances for GPU workers
    - S3 Intelligent-Tiering
    - Reserved Instances (RDS, ElastiCache)
    - CloudFront caching optimization
  
  Cost per User: $1.20-2.60/user/month
  Target Margin: 85-91% at $15/user subscription
```

---

## Environment Services Mapping

### Comprehensive Service Matrix

| Service | Development | Testing/QA (Sandbox) | Staging | Production |
|---------|-------------|---------------------|---------|------------|
| **Frontend** | Localhost:3000<br/>Webpack dev server | AWS S3 + CloudFront<br/>sandbox.ai-filmstudio.com | AWS S3 + CloudFront<br/>staging.ai-filmstudio.com | AWS S3 + CloudFront<br/>www.ai-filmstudio.com<br/>Global CDN |
| **Backend API** | Localhost:5000<br/>Uvicorn auto-reload | ECS Fargate<br/>1-2 tasks<br/>1 vCPU, 2GB RAM | ECS Fargate<br/>2-4 tasks<br/>Auto-scaling | ECS Fargate<br/>4-50 tasks<br/>Full auto-scaling<br/>Multi-AZ |
| **Database** | Local PostgreSQL<br/>Docker container<br/>or db.t3.micro | RDS PostgreSQL<br/>db.t3.medium<br/>2 vCPU, 4GB<br/>Single-AZ | RDS PostgreSQL<br/>db.r6g.large<br/>2 vCPU, 16GB<br/>Multi-AZ | RDS PostgreSQL<br/>db.r6g.xlarge<br/>4 vCPU, 32GB<br/>Multi-AZ + Read Replicas |
| **AI Models / GPU** | Local small models<br/>Mock responses<br/>Optional: g4dn.xlarge | g4dn.xlarge (T4)<br/>1 instance<br/>On-demand<br/>Manual scaling | g4dn.xlarge<br/>1-3 instances<br/>Auto-scaled<br/>50% spot | g4dn.xlarge/2xlarge<br/>3-20 instances<br/>Auto-scaled<br/>70% spot, 30% on-demand |
| **Storage** | Local filesystem<br/>./data/uploads<br/>or S3 dev bucket | S3 sandbox bucket<br/>~100GB<br/>30-day lifecycle | S3 staging bucket<br/>~500GB<br/>Versioning enabled<br/>IA after 30 days | S3 production<br/>Multi-TB<br/>Intelligent-Tiering<br/>Cross-region replication |
| **Cache** | Local Redis<br/>Docker container<br/>localhost:6379 | ElastiCache<br/>cache.t3.micro<br/>Single node | ElastiCache<br/>cache.r6g.large<br/>Multi-AZ | ElastiCache<br/>cache.r6g.large<br/>Cluster mode<br/>Multi-AZ replicas |
| **Queue** | LocalStack SQS<br/>or AWS SQS dev | SQS sandbox queue<br/>Standard queue | SQS staging queue<br/>DLQ enabled | SQS production<br/>DLQ enabled<br/>CloudWatch alarms |
| **CDN** | None<br/>Direct access | CloudFront<br/>Basic caching | CloudFront<br/>Full caching rules | CloudFront<br/>Global distribution<br/>Origin Shield<br/>WAF enabled |
| **Load Balancer** | None<br/>Direct connection | ALB<br/>Single AZ acceptable | ALB<br/>Multi-AZ | ALB<br/>Multi-AZ<br/>SSL termination<br/>WAF integration |
| **CI/CD** | GitHub Actions<br/>Local builds | GitHub Actions<br/>Auto-deploy on merge | GitHub Actions<br/>Manual approval | GitHub Actions<br/>Blue-green deploy<br/>Manual approval |
| **Monitoring** | Console logs<br/>Basic debugging | CloudWatch<br/>Basic logs & metrics | CloudWatch<br/>Logs, metrics, alarms<br/>Dashboards | CloudWatch<br/>Prometheus + Grafana<br/>X-Ray tracing<br/>PagerDuty alerts |
| **Security** | Local dev only<br/>No authentication<br/>(or basic) | HTTPS<br/>JWT auth<br/>IAM roles | HTTPS<br/>JWT auth<br/>IAM roles<br/>Security groups | HTTPS<br/>JWT auth<br/>WAF<br/>GuardDuty<br/>Secrets Manager<br/>KMS encryption |
| **Backup** | None<br/>Git only | Daily RDS backup<br/>7-day retention | Daily RDS backup<br/>14-day retention<br/>S3 versioning | Daily RDS backup<br/>30-day retention<br/>Cross-region backup<br/>S3 versioning + replication |
| **Networking** | Localhost | Sandbox VPC<br/>or shared dev VPC<br/>Single NAT | Dedicated VPC<br/>10.1.0.0/16<br/>2 AZs<br/>NAT per AZ | Dedicated VPC<br/>10.0.0.0/16<br/>2 AZs<br/>VPC endpoints<br/>Multi-AZ NAT |

### Cost Comparison

| Environment | Monthly Cost | Key Cost Drivers |
|-------------|--------------|------------------|
| Development | $0-100 | Optional cloud resources, mostly local |
| Testing/QA | $335 | Small RDS, 1 GPU instance (40 hrs/month), minimal compute |
| Staging | $800-1,200 | Production-like setup, scaled down |
| Production | $2,600 | Full HA, auto-scaling, monitoring, multiple GPU workers |

---

## Environment Interactions

### Code & Deployment Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                       Developer Laptop                           │
│  • Feature branch development                                    │
│  • Local testing                                                 │
│  • Unit tests                                                    │
└────────────────────────┬────────────────────────────────────────┘
                         │ git push
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                         GitHub                                   │
│  • Source control                                                │
│  • Pull request review                                           │
│  • CI checks (linting, tests)                                    │
└────────────────────────┬────────────────────────────────────────┘
                         │ merge to develop
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│               Development Environment (Local)                    │
│  • Fast iteration                                                │
│  • Immediate feedback                                            │
│  • Isolated testing                                              │
└────────────────────────┬────────────────────────────────────────┘
                         │ push via GitHub Actions
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│            Testing/QA Environment (Sandbox)                      │
│  • Automated deployment                                          │
│  • Integration testing                                           │
│  • QA validation                                                 │
│  • Bug fixes                                                     │
└────────────────────────┬────────────────────────────────────────┘
                         │ merge tested code to main
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│           Staging / Pre-Production Environment                   │
│  • Manual deployment trigger                                     │
│  • Final QA and validation                                       │
│  • Performance testing                                           │
│  • Deployment rehearsal                                          │
│  • Product owner approval                                        │
└────────────────────────┬────────────────────────────────────────┘
                         │ manual or automated deploy
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│               Production Environment                             │
│  • Blue-green deployment                                         │
│  • Gradual traffic shift                                         │
│  • Real-time monitoring                                          │
│  • Rollback capability                                           │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow Strategy

```
┌────────────────────────────────────────────────────────────────┐
│                    Development Data                             │
│  • Synthetic test data                                          │
│  • Minimal dataset                                              │
│  • No PII/sensitive data                                        │
│  • Anonymized samples                                           │
└────────────────────────┬───────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────┐
│                   Testing/QA Data                               │
│  • Anonymized production data (optional)                        │
│  • Larger test dataset                                          │
│  • Realistic user scenarios                                     │
│  • Data refresh: Weekly                                         │
└────────────────────────┬───────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────┐
│                    Staging Data                                 │
│  • Mirror production schema                                     │
│  • Realistic data volume                                        │
│  • Test data only (no real users)                               │
│  • Same data structure as prod                                  │
└────────────────────────┬───────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────┐
│                   Production Data                               │
│  • Real user data                                               │
│  • Encrypted at rest and in transit                             │
│  • Regular backups                                              │
│  • GDPR/compliance requirements                                 │
└────────────────────────────────────────────────────────────────┘
```

### AI Processing Flow Across Environments

```
┌───────────────────────────────────────────────────────────────┐
│                      Development                               │
│  • Lightweight models or mocks                                 │
│  • Fast response for testing                                   │
│  • Optional local GPU                                          │
└────────────────────────┬──────────────────────────────────────┘
                         │
                         ▼
┌───────────────────────────────────────────────────────────────┐
│                     Testing/QA                                 │
│  • Small GPU instance (g4dn.xlarge)                            │
│  • Same model versions as production                           │
│  • Scaled down for cost                                        │
│  • Manual start/stop                                           │
└────────────────────────┬──────────────────────────────────────┘
                         │
                         ▼
┌───────────────────────────────────────────────────────────────┐
│                      Staging                                   │
│  • Full GPU instances                                          │
│  • Same configuration as production                            │
│  • Performance testing                                         │
│  • 1-3 workers                                                 │
└────────────────────────┬──────────────────────────────────────┘
                         │
                         ▼
┌───────────────────────────────────────────────────────────────┐
│                     Production                                 │
│  • Full GPU cluster (3-20 workers)                             │
│  • Auto-scaled based on demand                                 │
│  • Mixed spot/on-demand                                        │
│  • High availability                                           │
└───────────────────────────────────────────────────────────────┘
```

---

## Configuration Management

### Environment Variables

Each environment uses different configuration files:

#### Development (.env.dev or .env.local)

```bash
# Application
NODE_ENV=development
API_URL=http://localhost:5000
NEXT_PUBLIC_API_URL=http://localhost:5000

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/aifilm_dev
DB_HOST=localhost
DB_PORT=5432
DB_NAME=aifilm_dev

# Redis
REDIS_URL=redis://localhost:6379
REDIS_HOST=localhost
REDIS_PORT=6379

# AWS (optional for dev)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_dev_key
AWS_SECRET_ACCESS_KEY=your_dev_secret
S3_BUCKET=ai-film-studio-dev

# AI Models
MODEL_CACHE_DIR=./models
USE_MOCK_AI=true
OPENAI_API_KEY=sk-test-xxx

# Logging
LOG_LEVEL=DEBUG
```

#### Testing/QA (.env.sandbox)

```bash
# Application
NODE_ENV=sandbox
API_URL=https://api-sandbox.ai-filmstudio.com
NEXT_PUBLIC_API_URL=https://api-sandbox.ai-filmstudio.com

# Database
DATABASE_URL=postgresql://user:password@sandbox-db.xxx.rds.amazonaws.com:5432/aifilm_sandbox
DB_HOST=sandbox-db.xxx.rds.amazonaws.com
DB_PORT=5432
DB_NAME=aifilm_sandbox

# Redis
REDIS_URL=redis://sandbox-redis.xxx.cache.amazonaws.com:6379

# AWS
AWS_REGION=us-east-1
S3_BUCKET=ai-film-studio-sandbox-us-east-1
SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/xxx/aifilm-sandbox-jobs

# AI Models
MODEL_CACHE_DIR=/models
USE_MOCK_AI=false
MODEL_S3_BUCKET=ai-film-studio-models-shared

# Secrets (from AWS Secrets Manager)
JWT_SECRET={{resolve:secretsmanager:aifilm/sandbox/jwt-secret}}
OPENAI_API_KEY={{resolve:secretsmanager:aifilm/sandbox/openai-key}}

# Logging
LOG_LEVEL=INFO
```

#### Staging (.env.staging)

```bash
# Application
NODE_ENV=staging
API_URL=https://api-staging.ai-filmstudio.com
NEXT_PUBLIC_API_URL=https://api-staging.ai-filmstudio.com

# Database
DATABASE_URL={{resolve:secretsmanager:aifilm/staging/database-url}}
DB_HOST=staging-db.xxx.rds.amazonaws.com
DB_PORT=5432
DB_NAME=aifilm_staging

# Redis
REDIS_URL=redis://staging-redis.xxx.cache.amazonaws.com:6379

# AWS
AWS_REGION=us-east-1
S3_BUCKET=ai-film-studio-staging-us-east-1
SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/xxx/aifilm-staging-jobs

# AI Models
MODEL_CACHE_DIR=/models
MODEL_S3_BUCKET=ai-film-studio-models-shared

# Secrets (from AWS Secrets Manager)
JWT_SECRET={{resolve:secretsmanager:aifilm/staging/jwt-secret}}
OPENAI_API_KEY={{resolve:secretsmanager:aifilm/staging/openai-key}}
STRIPE_SECRET_KEY={{resolve:secretsmanager:aifilm/staging/stripe-key}}

# Logging
LOG_LEVEL=INFO
```

#### Production (.env.production)

```bash
# Application
NODE_ENV=production
API_URL=https://api.ai-filmstudio.com
NEXT_PUBLIC_API_URL=https://api.ai-filmstudio.com

# Database (from Secrets Manager)
DATABASE_URL={{resolve:secretsmanager:aifilm/prod/database-url}}
DB_HOST=prod-db.xxx.rds.amazonaws.com
DB_PORT=5432
DB_NAME=aifilm_production

# Redis
REDIS_URL={{resolve:secretsmanager:aifilm/prod/redis-url}}

# AWS
AWS_REGION=us-east-1
S3_BUCKET=ai-film-studio-prod-us-east-1
SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/xxx/aifilm-prod-jobs

# AI Models
MODEL_CACHE_DIR=/models
MODEL_S3_BUCKET=ai-film-studio-models-prod

# Secrets (all from AWS Secrets Manager)
JWT_SECRET={{resolve:secretsmanager:aifilm/prod/jwt-secret}}
OPENAI_API_KEY={{resolve:secretsmanager:aifilm/prod/openai-key}}
STRIPE_SECRET_KEY={{resolve:secretsmanager:aifilm/prod/stripe-key}}
DATABASE_PASSWORD={{resolve:secretsmanager:aifilm/prod/db-password}}

# Monitoring
SENTRY_DSN={{resolve:secretsmanager:aifilm/prod/sentry-dsn}}
DATADOG_API_KEY={{resolve:secretsmanager:aifilm/prod/datadog-key}}

# Logging
LOG_LEVEL=INFO
```

### Terraform Variable Files

#### dev.tfvars

```hcl
environment = "dev"
region      = "us-east-1"

# VPC
vpc_cidr = "10.2.0.0/16"

# ECS
ecs_task_count     = 1
ecs_task_cpu       = "1024"
ecs_task_memory    = "2048"
enable_autoscaling = false

# RDS
db_instance_class  = "db.t3.medium"
db_allocated_storage = 100
db_multi_az        = false

# ElastiCache
redis_node_type = "cache.t3.micro"
redis_num_nodes = 1

# GPU Workers
gpu_instance_type = "g4dn.xlarge"
gpu_min_size      = 0
gpu_max_size      = 2
gpu_desired_size  = 0

# Tags
tags = {
  Environment = "dev"
  Project     = "AI-Film-Studio"
  ManagedBy   = "Terraform"
}
```

#### sandbox.tfvars

```hcl
environment = "sandbox"
region      = "us-east-1"

vpc_cidr = "10.3.0.0/16"

ecs_task_count     = 2
ecs_task_cpu       = "1024"
ecs_task_memory    = "2048"
enable_autoscaling = true
autoscaling_min    = 1
autoscaling_max    = 4

db_instance_class    = "db.t3.medium"
db_allocated_storage = 100
db_multi_az          = false

redis_node_type = "cache.t3.micro"
redis_num_nodes = 1

gpu_instance_type = "g4dn.xlarge"
gpu_min_size      = 0
gpu_max_size      = 3
gpu_desired_size  = 1

tags = {
  Environment = "sandbox"
  Project     = "AI-Film-Studio"
  ManagedBy   = "Terraform"
}
```

#### staging.tfvars

```hcl
environment = "staging"
region      = "us-east-1"

vpc_cidr = "10.1.0.0/16"

ecs_task_count     = 2
ecs_task_cpu       = "1024"
ecs_task_memory    = "2048"
enable_autoscaling = true
autoscaling_min    = 2
autoscaling_max    = 8

db_instance_class    = "db.r6g.large"
db_allocated_storage = 500
db_multi_az          = true

redis_node_type = "cache.r6g.large"
redis_num_nodes = 2

gpu_instance_type = "g4dn.xlarge"
gpu_min_size      = 1
gpu_max_size      = 3
gpu_desired_size  = 1

enable_cloudfront = true
enable_waf        = true

tags = {
  Environment = "staging"
  Project     = "AI-Film-Studio"
  ManagedBy   = "Terraform"
}
```

#### production.tfvars

```hcl
environment = "production"
region      = "us-east-1"

vpc_cidr = "10.0.0.0/16"

ecs_task_count     = 4
ecs_task_cpu       = "1024"
ecs_task_memory    = "2048"
enable_autoscaling = true
autoscaling_min    = 4
autoscaling_max    = 50

db_instance_class      = "db.r6g.xlarge"
db_allocated_storage   = 500
db_multi_az            = true
db_backup_retention    = 30
enable_read_replica    = true
read_replica_count     = 2

redis_node_type     = "cache.r6g.large"
redis_num_nodes     = 3
redis_cluster_mode  = true

gpu_instance_type    = "g4dn.xlarge"
gpu_min_size         = 3
gpu_max_size         = 20
gpu_desired_size     = 3
gpu_spot_percentage  = 70

enable_cloudfront        = true
enable_waf               = true
enable_guardduty         = true
enable_xray              = true
enable_cross_region_backup = true

tags = {
  Environment = "production"
  Project     = "AI-Film-Studio"
  ManagedBy   = "Terraform"
  CostCenter  = "Engineering"
  Compliance  = "GDPR-ready"
}
```

---

## Access & Security

### Environment Access Control

| Environment | Access Method | Authentication | Authorization |
|-------------|---------------|----------------|---------------|
| **Development** | Local machine | None (local dev) | Full access |
| **Testing/QA** | VPN or IP whitelist | AWS IAM + SSO | Developers, QA team |
| **Staging** | VPN or IP whitelist | AWS IAM + SSO + MFA | Developers, QA, DevOps |
| **Production** | Bastion host only | AWS IAM + SSO + MFA | DevOps team only |

### Security Best Practices

```yaml
Development:
  - Use local credentials only
  - No production credentials
  - Git-ignore .env files
  - Use test API keys

Testing/QA:
  - IAM roles for service access
  - No direct database access
  - SSH via Systems Manager
  - Rotate credentials monthly

Staging:
  - IAM roles with MFA
  - Database access via bastion
  - All secrets in Secrets Manager
  - Security group IP whitelisting
  - Audit logging enabled

Production:
  - Least privilege IAM policies
  - No SSH access (use Systems Manager)
  - All secrets in Secrets Manager
  - Secrets rotation (30-90 days)
  - Database access audit logging
  - WAF and GuardDuty enabled
  - VPC Flow Logs enabled
  - CloudTrail for all API calls
```

---

## Deployment Process

### CI/CD Pipeline per Environment

#### Development → Testing/QA

```yaml
Trigger: Push to 'develop' branch

Steps:
  1. Run linters (ESLint, Black, Ruff)
  2. Run unit tests
  3. Build Docker images
  4. Push images to ECR (sandbox tag)
  5. Deploy to sandbox ECS
  6. Run database migrations
  7. Execute smoke tests
  8. Notify team in Slack

Approval: None (automatic)
Rollback: Automatic on failed smoke tests
```

#### Testing/QA → Staging

```yaml
Trigger: Merge to 'main' branch or manual trigger

Steps:
  1. All tests must pass
  2. Security scan (Snyk, Trivy)
  3. Build optimized Docker images
  4. Push images to ECR (staging tag)
  5. Create database backup snapshot
  6. Deploy to staging ECS (blue-green)
  7. Run database migrations (with rollback plan)
  8. Execute full test suite
  9. Run performance tests
 10. Generate deployment report

Approval: Required (tech lead or senior dev)
Rollback: Manual, blue-green instant switch
```

#### Staging → Production

```yaml
Trigger: Manual deployment after staging validation

Steps:
  1. Staging validation complete
  2. Create production release tag
  3. Notify team of deployment window
  4. Create production database backup
  5. Build production Docker images
  6. Push images to ECR (production tag)
  7. Deploy to production (blue-green):
     a. Deploy to "green" environment
     b. Run smoke tests on green
     c. Shift 10% traffic to green
     d. Monitor for 10 minutes
     e. Shift 25% traffic
     f. Monitor for 10 minutes
     g. Shift 50% traffic
     h. Monitor for 10 minutes
     i. Shift 100% traffic
  8. Run database migrations (zero-downtime)
  9. Monitor CloudWatch for 1 hour
 10. Update documentation
 11. Notify stakeholders

Approval: Required (product owner + DevOps lead)
Rollback: Instant via blue-green switch (< 5 minutes)
```

---

## Summary

This comprehensive environment setup ensures:

✅ **Safe Development** — Local and isolated development without affecting other environments  
✅ **Thorough Testing** — Dedicated QA environment for validating all features including AI workflows  
✅ **Reliable Staging** — Production mirror for final validation and deployment rehearsal  
✅ **Scalable Production** — Highly available, auto-scaled infrastructure serving real users  
✅ **Clear Separation** — Each environment has distinct purpose, configuration, and access controls  
✅ **Cost Optimization** — Right-sized resources per environment with production-level monitoring  
✅ **Security** — Progressive security hardening from dev to production  
✅ **Seamless Deployment** — Automated CI/CD pipeline with safety gates and rollback capability  

---

## Diagram Overview

For a visual representation of the environment interactions, see [environment-diagram.md](./environment-diagram.md).

---

## Document Revision History

| Version | Date       | Author                 | Changes                                    |
|---------|------------|------------------------|--------------------------------------------|
| 1.0     | 2025-12-31 | AI-Empower-HQ-360      | Initial complete environment setup document |

---

**End of Document**
