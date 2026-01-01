# 🌐 AI FILM STUDIO – CLOUD / INFRASTRUCTURE STACK

**Version:** 1.0  
**Last Updated:** 2025-12-31  
**Document Owner:** AI-Empower-HQ-360

---

## Overview

This document provides a detailed Cloud / Infrastructure setup for AI Film Studio, including all environments, services, and scalability considerations. The platform is built on AWS with a focus on scalability, reliability, and cost-effectiveness.

---

## 1️⃣ Cloud Provider

| Layer | Recommendation | Notes |
|-------|---------------|-------|
| **Provider** | AWS | Widely used, scalable, GPU instances, S3 storage, CloudFront CDN |
| **Optional Alternatives** | GCP / Azure | Can host AI workloads, optional for backup or multi-cloud strategy |

### Why AWS?

- **Mature AI/ML Services**: SageMaker, EC2 GPU instances (G4/G5), comprehensive AI toolkit
- **Global Infrastructure**: 30+ regions, 99+ availability zones for low latency
- **Cost Optimization**: Spot instances for GPU workloads, reserved instances, savings plans
- **Integration**: Native integration between services (ECS, S3, RDS, SQS, CloudFront)
- **Security**: Comprehensive security services (IAM, WAF, GuardDuty, KMS)

---

## 2️⃣ Compute

| Service | Recommendation | Notes |
|---------|---------------|-------|
| **AI Video / Voice Jobs** | EC2 GPU (G4/G5 instances) | Required for AI video generation, lip-sync, animation |
| **Backend Microservices** | EC2 / Lambda / ECS / Kubernetes | Node.js backend, async AI job workers |
| **Autoscaling** | AWS Auto Scaling / ECS Fargate | Scale compute automatically based on job queue load |

### Detailed Compute Configuration

#### Backend API Services

**Technology**: FastAPI (Python) or Node.js (Express/NestJS)

**Hosting Options**:

1. **Amazon ECS (Fargate)** - *Recommended for Production*
   - Serverless container orchestration
   - No server management required
   - Pay only for resources used
   - Configuration:
     ```yaml
     Task Definition:
       CPU: 1024 (1 vCPU)
       Memory: 2048 MB (2 GB)
       Desired Count: 2 (min) - 10 (max)
       Auto-scaling: Target CPU 70%
       Health Check: /health endpoint
     ```

2. **Amazon EKS (Kubernetes)** - *For Complex Microservices*
   - Full Kubernetes control
   - Better for multi-service architectures
   - Configuration:
     ```yaml
     Node Group:
       Instance Type: t3.medium
       Min Nodes: 2
       Max Nodes: 10
       Auto-scaling: Cluster Autoscaler
     ```

3. **AWS Lambda** - *For Event-Driven Functions*
   - Serverless functions
   - Perfect for webhooks, triggers
   - Configuration:
     ```yaml
     Runtime: Node.js 18 / Python 3.11
     Memory: 512 MB - 1024 MB
     Timeout: 30 seconds
     Concurrency: 100
     ```

#### GPU Workers for AI Processing

**Instance Types**:

| Instance | GPU | vCPUs | Memory | Storage | Use Case | Cost/Hour |
|----------|-----|-------|--------|---------|----------|-----------|
| g4dn.xlarge | 1x NVIDIA T4 (16GB) | 4 | 16 GB | 125 GB NVMe | Development, testing | $0.526 |
| g4dn.2xlarge | 1x NVIDIA T4 (16GB) | 8 | 32 GB | 225 GB NVMe | Production (standard) | $0.752 |
| g5.xlarge | 1x NVIDIA A10G (24GB) | 4 | 16 GB | 250 GB NVMe | High-quality generation | $1.006 |
| g5.2xlarge | 1x NVIDIA A10G (24GB) | 8 | 32 GB | 450 GB NVMe | Production (premium) | $1.212 |

**Deployment Strategy**:
```yaml
Orchestration: ECS or EKS with GPU support
AMI: AWS Deep Learning AMI (Ubuntu 22.04)
Auto-scaling:
  Metric: SQS Queue Depth
  Scale Up: Queue > 10 messages
  Scale Down: Queue < 2 messages
  Min Instances: 0 (dev), 1 (staging), 2 (prod)
  Max Instances: 5 (dev), 10 (staging), 20 (prod)

Spot Instance Strategy:
  Mix: 70% Spot, 30% On-Demand
  Savings: ~70% on GPU costs
  Interruption Handling: Graceful shutdown, job requeue
```

---

## 3️⃣ Storage & Media

| Service | Recommendation | Notes |
|---------|---------------|-------|
| **Media Storage** | AWS S3 + CloudFront CDN | Store images, videos, thumbnails, subtitles; global distribution |
| **Database Storage** | RDS (PostgreSQL / MySQL) | Users, projects, credits, subscriptions |
| **Cache / Queue** | Redis (ElastiCache) | Fast caching for credits, project status, job queues |
| **Backup** | S3 versioning + RDS snapshots | Disaster recovery & rollback |

### Amazon S3 Configuration

#### Bucket Structure

```yaml
Frontend Bucket:
  Name: ai-film-studio-frontend-{env}-{account_id}
  Purpose: Static website hosting (Next.js)
  Configuration:
    - Versioning: Enabled
    - Encryption: SSE-S3 (AES-256)
    - Public Access: Blocked (CloudFront OAC only)
    - CORS: Enabled for uploads
  Lifecycle:
    - Expire incomplete uploads: 7 days

Assets Bucket:
  Name: ai-film-studio-assets-{env}-{account_id}
  Purpose: User-generated content (images, videos, audio)
  Structure:
    /users/{user_id}/
      /projects/{project_id}/
        /raw/         # Original uploads
        /generated/   # AI-generated content
        /final/       # Rendered outputs
  Configuration:
    - Versioning: Enabled
    - Encryption: SSE-S3 (AES-256)
    - Intelligent-Tiering: Enabled
  Lifecycle:
    - Transition to IA: 90 days
    - Transition to Glacier IR: 180 days
    - Expire old versions: 30 days

Backup Bucket:
  Name: ai-film-studio-backups-{env}-{account_id}
  Region: us-west-2 (cross-region)
  Purpose: Disaster recovery
  Configuration:
    - Replication: From primary buckets
    - Retention: 90 days
```

### Amazon RDS (PostgreSQL)

```yaml
Development:
  Engine: PostgreSQL 15.4
  Instance: db.t3.micro (2 vCPU, 1 GB)
  Storage: 20 GB gp3, auto-scaling to 100 GB
  Multi-AZ: Yes (for consistency)
  Backups: 7 days retention
  Encryption: AES-256 (KMS)

Sandbox/QA:
  Engine: PostgreSQL 15.4
  Instance: db.t3.small (2 vCPU, 2 GB)
  Storage: 50 GB gp3, auto-scaling to 200 GB
  Multi-AZ: Yes
  Backups: 7 days retention
  Encryption: AES-256 (KMS)

Staging:
  Engine: PostgreSQL 15.4
  Instance: db.t3.medium (2 vCPU, 4 GB)
  Storage: 100 GB gp3, auto-scaling to 500 GB
  Multi-AZ: Yes
  Backups: 14 days retention
  Read Replicas: 1
  Encryption: AES-256 (KMS)

Production:
  Engine: PostgreSQL 15.4
  Instance: db.r6g.xlarge (4 vCPU, 32 GB)
  Storage: 500 GB gp3, 5000 IOPS, auto-scaling to 1 TB
  Multi-AZ: Yes
  Backups: 30 days retention
  Read Replicas: 2-3 (for scaling reads)
  Encryption: AES-256 (KMS)
  Performance Insights: Enabled
  Enhanced Monitoring: Enabled (60 second intervals)

Database Schema:
  Core Tables:
    - users (id, email, password_hash, subscription_tier, credits, created_at)
    - projects (id, user_id, name, description, status, settings, created_at)
    - jobs (id, project_id, type, status, parameters, result_url, error, created_at)
    - assets (id, project_id, type, s3_key, metadata, size, created_at)
    - subscriptions (id, user_id, plan, status, stripe_id, expires_at)
    - transactions (id, user_id, amount, type, status, created_at)
```

### Amazon ElastiCache (Redis)

```yaml
Development:
  Engine: Redis 7.0
  Node Type: cache.t3.micro (2 vCPU, 0.5 GB)
  Nodes: 1
  Encryption: In-transit and at-rest

Sandbox/QA:
  Engine: Redis 7.0
  Node Type: cache.t3.small (2 vCPU, 1.37 GB)
  Nodes: 1
  Encryption: In-transit and at-rest

Staging:
  Engine: Redis 7.0
  Node Type: cache.t3.medium (2 vCPU, 3.09 GB)
  Nodes: 2 (Multi-AZ)
  Encryption: In-transit and at-rest

Production:
  Engine: Redis 7.0
  Node Type: cache.r6g.large (2 vCPU, 13.07 GB)
  Nodes: 3 (Multi-AZ, 1 primary + 2 replicas)
  Cluster Mode: Enabled
  Encryption: In-transit and at-rest
  Automatic Failover: Enabled

Use Cases:
  - Session storage (TTL: 1 hour)
  - API response caching (TTL: 5 minutes)
  - Rate limiting counters (TTL: 1 minute)
  - Real-time job status (TTL: 24 hours)
  - User quota tracking
```

---

## 4️⃣ Networking & Security

| Layer | Recommendation | Notes |
|-------|---------------|-------|
| **Load Balancer** | AWS ELB / Application Load Balancer | Distribute requests across multiple backend instances |
| **Firewall** | Security Groups / NACLs | Control inbound/outbound traffic |
| **Domain & SSL** | Route 53 + ACM | Custom domain, HTTPS for all endpoints |
| **API Security** | Rate limiting, JWT, OAuth | Protect backend endpoints |

### VPC Architecture

```yaml
VPC Configuration:
  CIDR: 10.0.0.0/16
  Region: us-east-1 (primary)
  DNS Hostnames: Enabled
  DNS Resolution: Enabled

Subnet Structure:
  Public Subnets (Internet-facing):
    - us-east-1a: 10.0.1.0/24 (ALB, NAT Gateway, Bastion)
    - us-east-1b: 10.0.2.0/24 (ALB, NAT Gateway backup)
  
  Private App Subnets:
    - us-east-1a: 10.0.10.0/24 (ECS Backend, GPU Workers)
    - us-east-1b: 10.0.11.0/24 (ECS Backend, GPU Workers)
  
  Private Data Subnets:
    - us-east-1a: 10.0.20.0/24 (RDS, ElastiCache)
    - us-east-1b: 10.0.21.0/24 (RDS Standby, ElastiCache)

Network Components:
  - Internet Gateway: 1 (for public subnets)
  - NAT Gateway: 2 (one per AZ for high availability)
  - VPC Endpoints:
      - S3 (Gateway endpoint - free)
      - SQS (Interface endpoint)
      - ECR (Interface endpoint)
      - Secrets Manager (Interface endpoint)
      - CloudWatch Logs (Interface endpoint)
```

### Security Groups

```yaml
ALB Security Group:
  Inbound:
    - Port 443 (HTTPS): 0.0.0.0/0
    - Port 80 (HTTP): 0.0.0.0/0 → Redirect to 443
  Outbound:
    - All traffic to Backend Security Group

Backend ECS Security Group:
  Inbound:
    - Port 8000: From ALB Security Group
    - Port 8000: From Backend Security Group (service mesh)
  Outbound:
    - Port 443: To 0.0.0.0/0 (AWS APIs, external services)
    - Port 5432: To RDS Security Group
    - Port 6379: To Redis Security Group

GPU Workers Security Group:
  Inbound:
    - None (workers pull from SQS)
  Outbound:
    - Port 443: To 0.0.0.0/0 (AWS APIs, model downloads)
    - Port 5432: To RDS Security Group
    - S3: Via VPC Endpoint
    - SQS: Via VPC Endpoint

RDS Security Group:
  Inbound:
    - Port 5432: From Backend Security Group
    - Port 5432: From GPU Workers Security Group
  Outbound:
    - None (database doesn't initiate connections)

ElastiCache Security Group:
  Inbound:
    - Port 6379: From Backend Security Group
  Outbound:
    - None
```

### SSL/TLS & Domain Configuration

```yaml
Route 53:
  Hosted Zone: ai-film-studio.com
  Records:
    - api.ai-film-studio.com → ALB (A record, Alias)
    - www.ai-film-studio.com → CloudFront (A record, Alias)
    - ai-film-studio.com → CloudFront (A record, Alias)

AWS Certificate Manager (ACM):
  Certificates:
    - *.ai-film-studio.com (wildcard)
    - Validation: DNS validation
    - Renewal: Automatic
    - Used by: CloudFront, ALB

TLS Configuration:
  CloudFront:
    - Minimum TLS: 1.2
    - Supported: TLS 1.2, TLS 1.3
    - Cipher Suites: Modern (recommended)
    - HSTS: Enabled (max-age=31536000)
  
  Application Load Balancer:
    - Security Policy: ELBSecurityPolicy-TLS13-1-2-2021-06
    - HTTP → HTTPS: Redirect (301)
```

### AWS WAF (Web Application Firewall)

```yaml
Web ACL Configuration:
  Associated With: CloudFront, ALB
  
  Managed Rules:
    - AWS Managed Rules - Core Rule Set
    - AWS Managed Rules - Known Bad Inputs
    - AWS Managed Rules - SQL Injection
    - AWS Managed Rules - Amazon IP Reputation List
  
  Custom Rules:
    1. Rate Limiting:
       - 100 requests per 5 minutes per IP
       - Action: Block (return 429)
    
    2. Geo-Blocking (optional):
       - Block high-risk countries
       - Action: Block
    
    3. API Key Validation:
       - Require X-API-Key header for API routes
       - Action: Block if missing

  Logging:
    - Destination: S3 bucket or CloudWatch Logs
    - Retention: 90 days
```

---

## 5️⃣ Job Queue / AI Orchestration

| Layer | Recommendation | Notes |
|-------|---------------|-------|
| **Queue** | BullMQ / AWS SQS / RabbitMQ | Handle AI jobs asynchronously |
| **Worker Nodes** | Node.js / Python services | Process video/audio/music tasks |
| **GPU Scaling** | Dynamic EC2 instances | Spin up GPU nodes as per job demand |
| **Logging** | CloudWatch / ELK Stack | Monitor AI job performance, failures |

### Amazon SQS Configuration

```yaml
Main Processing Queue:
  Name: ai-film-studio-processing-queue-{env}
  Type: Standard
  Configuration:
    - Visibility Timeout: 300 seconds (5 minutes)
    - Message Retention: 345600 seconds (4 days)
    - Max Message Size: 262144 bytes (256 KB)
    - Receive Wait Time: 20 seconds (long polling)
    - Dead Letter Queue: Enabled (3 max receives)
  
  Message Format:
    {
      "job_id": "uuid",
      "user_id": "uuid",
      "project_id": "uuid",
      "type": "video_generation|image_generation|audio_generation",
      "parameters": {...},
      "priority": "low|normal|high",
      "created_at": "timestamp"
    }

Dead Letter Queue:
  Name: ai-film-studio-dlq-{env}
  Configuration:
    - Message Retention: 1209600 seconds (14 days)
    - Alarm: Trigger when message count > 5
  
  Purpose:
    - Capture failed jobs after 3 retry attempts
    - Manual investigation and reprocessing
    - Error pattern analysis

Priority Queues (Optional):
  High Priority Queue:
    - For premium users
    - Dedicated GPU workers
    - Faster processing
  
  Normal Priority Queue:
    - For standard users
    - Shared GPU workers
```

### Worker Architecture

```yaml
Worker Types:
  1. Image Generation Workers:
     - Model: Stable Diffusion XL
     - GPU: g4dn.xlarge (T4 16GB)
     - Concurrent Jobs: 1-2 per worker
     - Processing Time: 30-60 seconds per image
  
  2. Video Generation Workers:
     - Model: Stable Video Diffusion, AnimateDiff
     - GPU: g5.xlarge (A10G 24GB)
     - Concurrent Jobs: 1 per worker
     - Processing Time: 2-5 minutes per clip
  
  3. Audio Generation Workers:
     - Model: AudioCraft, MusicGen
     - GPU: g4dn.xlarge (T4 16GB)
     - Concurrent Jobs: 2-3 per worker
     - Processing Time: 20-40 seconds per track

Worker Lifecycle:
  1. Boot: 2-3 minutes (AMI load, Docker pull, model download)
  2. Warm-up: 30-60 seconds (model initialization)
  3. Processing: Variable (depends on job type)
  4. Idle: 5 minutes (before scale-down)
  5. Shutdown: 30 seconds (graceful job completion)

Scaling Logic:
  Scale Up:
    - Trigger: SQS queue depth > threshold
    - Action: Launch new GPU instances
    - Threshold: 10 messages (1 worker), 25 (2 workers), 50 (4 workers)
  
  Scale Down:
    - Trigger: Queue empty for 10 minutes
    - Action: Terminate idle workers (FIFO)
    - Protection: Keep minimum instances running

Error Handling:
  - Transient Errors: Retry up to 3 times
  - Permanent Errors: Send to DLQ, notify user
  - Spot Interruption: Gracefully finish job or requeue
  - Model Load Failure: Alert ops team, use backup worker
```

### BullMQ (Alternative to SQS)

```yaml
Use Case: If using Node.js and need more features

Configuration:
  Backend: Redis (ElastiCache)
  Features:
    - Job prioritization
    - Job scheduling (delayed jobs)
    - Job progress tracking
    - Job events and webhooks
    - Automatic retries with backoff
    - Rate limiting
  
  Queues:
    - image-generation-queue
    - video-generation-queue
    - audio-generation-queue
    - notification-queue

Advantages over SQS:
  - Real-time job progress updates
  - Better job prioritization
  - Scheduled/delayed jobs
  - Lower latency (Redis vs. HTTP polling)

Disadvantages:
  - Requires Redis cluster management
  - Less managed than SQS
  - Need to handle Redis failover
```

---

## 6️⃣ CI/CD & Infrastructure as Code

| Layer | Recommendation | Notes |
|-------|---------------|-------|
| **CI/CD** | GitHub Actions / Jenkins | Automate build, test, deploy |
| **IaC** | Terraform | Define AWS infrastructure (EC2, S3, RDS, Redis, Lambda) |
| **Containerization** | Docker | Package backend & AI microservices |
| **Orchestration** | ECS / Kubernetes | Manage containers and scaling |

### GitHub Actions Workflows

```yaml
1. Backend CI/CD (.github/workflows/backend-ci-cd.yml):
   Triggers:
     - Push to: main, develop
     - Pull Request: all branches
   
   Jobs:
     - Lint and format check (Ruff, Black, MyPy)
     - Run unit tests (pytest)
     - Run integration tests
     - Security scan (Snyk, Trivy)
     - Build Docker image
     - Push to Amazon ECR
     - Deploy to ECS (dev → staging → prod)
   
   Environments:
     - dev: Auto-deploy on merge to develop
     - staging: Auto-deploy on merge to main
     - production: Manual approval required

2. Worker CI/CD (.github/workflows/worker-ci-cd.yml):
   Similar to backend, but for GPU worker services
   
   Additional Steps:
     - Model validation (ensure models load correctly)
     - GPU smoke tests (if possible)
     - Docker image optimization (multi-stage builds)

3. Frontend CI/CD (.github/workflows/frontend-ci-cd.yml):
   Triggers:
     - Push to: main, develop
     - Pull Request: all branches
   
   Jobs:
     - Lint and format check (ESLint, Prettier)
     - Run unit tests (Jest)
     - Run E2E tests (Playwright)
     - Build Next.js static export
     - Upload to S3
     - Invalidate CloudFront cache
   
   Environments:
     - dev: Auto-deploy on merge to develop
     - staging: Auto-deploy on merge to main
     - production: Manual approval required

4. Infrastructure CI/CD (.github/workflows/terraform-deploy.yml):
   Triggers:
     - Push to: infrastructure/**/*.tf
     - Manual workflow dispatch
   
   Jobs:
     - Terraform fmt check
     - Terraform validate
     - Terraform plan (post as PR comment)
     - Terraform apply (manual approval for prod)
   
   State Management:
     - Backend: S3 + DynamoDB locking
     - State per environment: dev, staging, prod
```

### Terraform Structure

```
infrastructure/
├── terraform/
│   ├── environments/
│   │   ├── dev/
│   │   │   ├── main.tf                 # Main configuration
│   │   │   ├── variables.tf            # Environment-specific variables
│   │   │   ├── outputs.tf              # Outputs
│   │   │   └── terraform.tfvars        # Variable values
│   │   ├── sandbox/
│   │   │   └── ... (similar structure)
│   │   ├── staging/
│   │   │   └── ... (similar structure)
│   │   └── production/
│   │       └── ... (similar structure)
│   └── modules/
│       ├── vpc/                         # VPC module
│       ├── ecs/                         # ECS cluster module
│       ├── rds/                         # RDS database module
│       ├── s3/                          # S3 bucket module
│       ├── cloudfront/                  # CloudFront module
│       ├── alb/                         # Application Load Balancer
│       ├── sqs/                         # SQS queue module
│       ├── elasticache/                 # ElastiCache module
│       ├── security-groups/             # Security groups module
│       └── monitoring/                  # CloudWatch alarms module
└── kubernetes/                          # Optional K8s manifests
    ├── base/                            # Base configurations
    ├── overlays/                        # Environment-specific overlays
    │   ├── dev/
    │   ├── staging/
    │   └── production/
    └── helm-charts/                     # Helm charts (if using Helm)
```

### Docker Configuration

```yaml
Backend Dockerfile:
  Strategy: Multi-stage build
  Stages:
    1. Builder stage:
       - Install dependencies
       - Run tests
       - Build artifacts
    2. Runtime stage:
       - Minimal base image (python:3.11-slim)
       - Copy only necessary files
       - Non-root user
       - Health check
  
  Optimization:
    - Layer caching
    - .dockerignore
    - Minimize image size (<500MB)

Worker Dockerfile:
  Strategy: Multi-stage build with AI models
  Stages:
    1. Model download stage:
       - Download AI models
       - Cache models in layer
    2. Runtime stage:
       - CUDA-enabled base image
       - Copy models and code
       - GPU-optimized libraries
  
  Optimization:
    - Separate models into own layer
    - Use BuildKit for faster builds
    - Image size: 8-12 GB (with models)

Frontend Dockerfile:
  Strategy: Multi-stage build
  Stages:
    1. Builder stage:
       - Node.js build
       - Next.js static export
    2. Runtime stage:
       - Nginx for serving (optional)
       - Or upload to S3 (no runtime container)
```

---

## 7️⃣ Monitoring & Alerts

| Layer | Recommendation | Notes |
|-------|---------------|-------|
| **Logs** | CloudWatch / ELK Stack | Capture errors, AI processing logs |
| **Metrics** | Prometheus + Grafana | GPU/CPU usage, job queue length, response times |
| **Alerts** | CloudWatch Alarms | Notify on failed jobs, downtime, or high latency |

### CloudWatch Configuration

```yaml
Log Groups:
  - /ecs/ai-film-studio-backend-{env}
  - /ecs/ai-film-studio-workers-{env}
  - /aws/rds/ai-film-studio-postgres-{env}
  - /aws/lambda/{function-name}
  - /aws/elasticache/ai-film-studio-redis-{env}

Log Retention:
  - Development: 7 days
  - Staging: 14 days
  - Production: 30 days

Metrics:
  Standard Metrics:
    - ECS CPU/Memory utilization
    - RDS CPU, connections, IOPS
    - SQS queue depth, message age
    - ALB request count, latency, errors
    - ElastiCache CPU, memory, evictions
  
  Custom Metrics:
    - AI job processing time (by type)
    - User credit consumption rate
    - API endpoint response times
    - GPU utilization percentage
    - Model inference latency

Alarms:
  Critical (PagerDuty / SMS):
    - RDS CPU > 90% for 5 minutes
    - ECS service task failures > 3 in 5 minutes
    - ALB 5xx errors > 1% for 5 minutes
    - SQS DLQ message count > 10
    - GPU worker crashes > 3 per hour
  
  Warning (Email / Slack):
    - RDS connections > 80% of max
    - SQS queue depth > 100 messages
    - ECS memory utilization > 85%
    - CloudFront error rate > 5%
    - S3 bucket size growth > 100GB/day
  
  Info (Slack):
    - ECS deployment completed
    - Auto-scaling events
    - RDS maintenance windows
    - Certificate renewal

Dashboards:
  1. System Health Dashboard:
     - All service status
     - Error rates
     - Request/response metrics
     - Resource utilization
  
  2. AI Jobs Dashboard:
     - Queue depths
     - Processing times
     - Success/failure rates
     - GPU utilization
  
  3. Cost Dashboard:
     - Daily/monthly costs by service
     - GPU instance costs
     - S3 storage costs
     - Data transfer costs
```

### Prometheus + Grafana (Optional)

```yaml
Use Case: Advanced monitoring and custom dashboards

Deployment:
  - ECS Service or EC2 instance
  - Prometheus for metrics collection
  - Grafana for visualization

Metrics Collection:
  - ECS task metrics (via CloudWatch exporter)
  - Custom application metrics
  - GPU metrics (via NVIDIA DCGM)
  - Node exporter for system metrics

Grafana Dashboards:
  - Infrastructure overview
  - Application performance
  - AI model performance
  - Cost analysis
  - User behavior analytics

Advantages:
  - More flexible queries (PromQL)
  - Better visualization options
  - Open-source and customizable
  - Integrate with multiple data sources

Integration:
  - CloudWatch metrics → Prometheus
  - Application metrics → Prometheus
  - Grafana → Prometheus (data source)
  - Alerts → Slack, PagerDuty, Email
```

### ELK Stack (Elasticsearch, Logstash, Kibana)

```yaml
Use Case: Advanced log analysis and search

Deployment:
  - Amazon OpenSearch Service (managed Elasticsearch)
  - Or self-hosted on ECS/EKS

Configuration:
  Data Flow:
    CloudWatch Logs → Lambda → OpenSearch
    Or: Fluent Bit → OpenSearch (from ECS tasks)
  
  Index Strategy:
    - logs-backend-{env}-{YYYY.MM.DD}
    - logs-workers-{env}-{YYYY.MM.DD}
    - logs-api-{env}-{YYYY.MM.DD}
  
  Retention:
    - Hot nodes: 7 days (fast SSD)
    - Warm nodes: 30 days (slower storage)
    - Cold storage: 90 days (S3)

Kibana Dashboards:
  - Error log analysis
  - API request patterns
  - User behavior tracking
  - Security incident detection

Benefits:
  - Full-text search across logs
  - Complex log queries
  - Pattern detection
  - Security analysis
```

---

## 8️⃣ Environments Mapping

| Environment | Compute | Database | Storage | Notes |
|-------------|---------|----------|---------|-------|
| **Development** | Local / small EC2 | Local Postgres | Local / S3 dev bucket | Lightweight AI models |
| **Sandbox / QA** | EC2 small GPU | RDS sandbox | S3 sandbox bucket | Test AI jobs & workflows |
| **Staging** | EC2 full GPU | RDS staging | S3 staging bucket | Full-scale test, YouTube integration |
| **Production** | EC2 GPU cluster | RDS production | S3 + CloudFront | Scalable, secure, monitored |

### Detailed Environment Configurations

#### Development Environment

```yaml
Purpose: Rapid development and testing by engineers
Infrastructure:
  Compute:
    - Backend: 1 x ECS Fargate (1 vCPU, 2 GB)
    - Workers: 0-1 x g4dn.xlarge (spot instance, on-demand)
  
  Database:
    - RDS: db.t3.micro (2 vCPU, 1 GB)
    - Storage: 20 GB gp3
    - Multi-AZ: Yes
  
  Cache:
    - ElastiCache: cache.t3.micro (0.5 GB)
  
  Storage:
    - S3: ai-film-studio-assets-dev-{account_id}
    - CloudFront: Enabled
  
  Network:
    - VPC: 10.0.0.0/16
    - ALB: Yes
    - NAT Gateway: 1

Features:
  - Auto-scale to 0 for cost savings
  - Relaxed security rules (for debugging)
  - Short log retention (7 days)
  - No WAF (to reduce costs)

Access:
  - Bastion host for SSH access
  - VPN for database access (optional)
  - Public ALB for API testing

Cost: ~$240-335/month
```

#### Sandbox / QA Environment

```yaml
Purpose: Integration testing, QA team validation
Infrastructure:
  Compute:
    - Backend: 2 x ECS Fargate (1 vCPU, 2 GB)
    - Workers: 1-2 x g4dn.xlarge (spot instance)
  
  Database:
    - RDS: db.t3.small (2 vCPU, 2 GB)
    - Storage: 50 GB gp3
    - Multi-AZ: Yes
  
  Cache:
    - ElastiCache: cache.t3.small (1.37 GB)
  
  Storage:
    - S3: ai-film-studio-assets-sandbox-{account_id}
    - CloudFront: Enabled
  
  Network:
    - VPC: 10.1.0.0/16 (separate from dev)
    - ALB: Yes
    - NAT Gateway: 1

Features:
  - Separate VPC from dev
  - Production-like configuration
  - Test data seeding scripts
  - Automated testing integration

Access:
  - Restricted to QA team
  - No SSH access (use SSM Session Manager)
  - Private ALB (VPN access)

Cost: ~$450-600/month
```

#### Staging Environment

```yaml
Purpose: Pre-production validation, final testing before prod
Infrastructure:
  Compute:
    - Backend: 2-4 x ECS Fargate (1 vCPU, 2 GB)
    - Workers: 2-4 x g4dn.xlarge (70% spot, 30% on-demand)
  
  Database:
    - RDS: db.t3.medium (2 vCPU, 4 GB)
    - Storage: 100 GB gp3
    - Multi-AZ: Yes
    - Read Replica: 1
  
  Cache:
    - ElastiCache: cache.t3.medium (3.09 GB)
    - Nodes: 2 (Multi-AZ)
  
  Storage:
    - S3: ai-film-studio-assets-staging-{account_id}
    - CloudFront: Enabled with custom domain
  
  Network:
    - VPC: 10.2.0.0/16 (separate VPC)
    - ALB: Yes
    - NAT Gateway: 2 (Multi-AZ)
    - VPC Endpoints: Yes

Features:
  - Production-like configuration
  - Blue-green deployment testing
  - Load testing capabilities
  - Security scanning
  - WAF enabled

Access:
  - Restricted to engineering team
  - Public ALB with IP whitelist
  - SSM Session Manager for instances

Cost: ~$800-1,200/month
```

#### Production Environment

```yaml
Purpose: Live user traffic, maximum reliability
Infrastructure:
  Compute:
    - Backend: 4-10 x ECS Fargate (1 vCPU, 2 GB)
    - Workers: 2-20 x g4dn.xlarge (70% spot, 30% on-demand)
    - Auto-scaling: Aggressive (based on queue depth)
  
  Database:
    - RDS: db.r6g.xlarge (4 vCPU, 32 GB)
    - Storage: 500 GB gp3, 5000 IOPS
    - Multi-AZ: Yes
    - Read Replicas: 2-3
    - Performance Insights: Enabled
  
  Cache:
    - ElastiCache: cache.r6g.large (13.07 GB)
    - Nodes: 3 (1 primary + 2 replicas, Multi-AZ)
    - Cluster Mode: Enabled
  
  Storage:
    - S3: ai-film-studio-assets-prod-{account_id}
    - S3 DR: ai-film-studio-assets-dr-usw2 (cross-region replication)
    - CloudFront: Enabled with custom domain and SSL
  
  Network:
    - VPC: 10.3.0.0/16 (dedicated VPC)
    - ALB: Yes
    - NAT Gateway: 2 (Multi-AZ for HA)
    - VPC Endpoints: Yes (S3, SQS, ECR, Secrets Manager, CloudWatch)

Features:
  - Multi-AZ deployment for all components
  - Blue-green deployments
  - Automatic rollback on health check failures
  - Enhanced monitoring (1-minute intervals)
  - WAF with advanced rules
  - GuardDuty for threat detection
  - Config for compliance auditing
  - Cross-region backups
  - 99.9% uptime SLA

Access:
  - No direct SSH access
  - SSM Session Manager only (audited)
  - Bastion host in private subnet (optional)
  - Public ALB with rate limiting

Security:
  - All data encrypted at rest and in transit
  - MFA for admin access
  - IAM roles with least privilege
  - Regular security audits
  - Automated patching
  - DDoS protection (AWS Shield Standard)

Cost: ~$2,600-4,000/month (depending on usage)
```

---

## 9️⃣ Deployment Strategy

### Blue-Green Deployment

```yaml
Implementation:
  - Used for: Backend API, GPU Workers
  - Tool: AWS CodeDeploy, ECS
  
  Process:
    1. Deploy new version to "green" environment
    2. Run smoke tests on green
    3. Gradually shift traffic: 10% → 50% → 100%
    4. Monitor error rates and latency
    5. Rollback if issues detected
    6. Terminate old "blue" environment

Benefits:
  - Zero-downtime deployments
  - Easy rollback
  - Gradual traffic shifting
  - Production validation before full rollout
```

### Canary Deployment

```yaml
Implementation:
  - Used for: High-risk changes
  - Tool: AWS App Mesh, ALB target groups
  
  Process:
    1. Deploy new version to 5% of users
    2. Monitor metrics for 15 minutes
    3. Increase to 25% if successful
    4. Increase to 50% if successful
    5. Increase to 100% if successful
    6. Automatic rollback if error rate increases

Benefits:
  - Minimize blast radius
  - Real user validation
  - Data-driven rollout decisions
```

---

## 🔟 Disaster Recovery

### RTO and RPO

```yaml
Recovery Time Objective (RTO): 1 hour
Recovery Point Objective (RPO): 15 minutes

Tier Classification:
  - Tier 1 (Critical): Database, Auth Service
    RTO: 30 minutes, RPO: 5 minutes
  - Tier 2 (Important): API Backend, GPU Workers
    RTO: 1 hour, RPO: 15 minutes
  - Tier 3 (Normal): Frontend (cached), Monitoring
    RTO: 2 hours, RPO: 1 hour
```

### Backup Strategy

```yaml
RDS Backups:
  - Automated daily backups
  - Retention: 30 days (prod), 7 days (dev/staging)
  - Point-in-time recovery: Yes (5-minute intervals)
  - Cross-region snapshots: us-west-2 (weekly)

S3 Backups:
  - Versioning: Enabled on all buckets
  - Cross-region replication: us-west-2
  - Lifecycle policies: Transition to Glacier after 90 days
  - MFA Delete: Enabled for production

Configuration Backups:
  - Terraform state: Versioned in S3
  - Git repository: All IaC and application code
  - Secrets: AWS Secrets Manager with versioning
```

### Failover Procedures

```yaml
Database Failover:
  - Automatic Multi-AZ failover (60-120 seconds)
  - No manual intervention required
  - DNS automatically updates

Region Failover (us-east-1 → us-west-2):
  1. Declare disaster (5 minutes)
  2. Promote RDS read replica in us-west-2 (15 minutes)
  3. Deploy ECS services via Terraform (20 minutes)
  4. Update Route 53 to us-west-2 ALB (2 minutes)
  5. Update CloudFront origin to us-west-2 S3 (5 minutes)
  6. Verify functionality (10 minutes)
  
  Total RTO: ~60 minutes
  Data Loss: <15 minutes (RPO)
```

---

## 🔹 Summary

### Complete Infrastructure Stack

```yaml
Compute:
  - Backend: ECS Fargate / EKS Kubernetes
  - Workers: EC2 GPU (G4/G5 instances)
  - Auto-scaling: Based on CPU, memory, and queue depth

Storage:
  - Media: S3 + CloudFront CDN
  - Database: RDS PostgreSQL (Multi-AZ)
  - Cache: ElastiCache Redis
  - Backups: S3 versioning, RDS snapshots, cross-region replication

Networking & Security:
  - Load Balancer: Application Load Balancer
  - Firewall: Security Groups, NACLs, AWS WAF
  - SSL/TLS: Route 53 + ACM
  - VPC: Multi-AZ with public/private subnets

AI Jobs:
  - Queue: Amazon SQS (or BullMQ with Redis)
  - Orchestration: Queue-based processing
  - Scaling: Auto-scaling GPU nodes based on queue depth
  - Monitoring: CloudWatch, custom metrics

CI/CD & IaC:
  - CI/CD: GitHub Actions
  - IaC: Terraform
  - Containers: Docker
  - Registry: Amazon ECR
  - Orchestration: ECS / EKS

Monitoring:
  - Logs: CloudWatch Logs, ELK Stack (optional)
  - Metrics: CloudWatch Metrics, Prometheus (optional)
  - Visualization: CloudWatch Dashboards, Grafana (optional)
  - Alerts: CloudWatch Alarms, SNS, PagerDuty

Environments:
  - Development: Lightweight, cost-optimized
  - Sandbox/QA: Production-like for testing
  - Staging: Full-scale validation
  - Production: Multi-AZ, HA, scalable

Cost:
  - Development: ~$335/month
  - Sandbox/QA: ~$550/month
  - Staging: ~$1,000/month
  - Production: ~$2,600/month (1,000 users)
```

This cloud infrastructure supports all AI Film Studio workflows, from script → video generation → YouTube upload → dashboard preview, and ensures **scalability**, **security**, and **high availability**.

---

## 📚 Additional Resources

### Related Documents
- [System Design Document](./system-design.md)
- [Requirements Document](../requirements/)
- [Security Guidelines](./security-guidelines.md) *(to be created)*
- [Deployment Runbooks](../operations/runbooks/) *(to be created)*

### External References
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Terraform AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [ECS Best Practices](https://docs.aws.amazon.com/AmazonECS/latest/bestpracticesguide/)
- [AWS GPU Instances Guide](https://aws.amazon.com/ec2/instance-types/g4/)

---

**Document Version**: 1.0  
**Last Updated**: 2025-12-31  
**Next Review**: 2026-03-31  
**Owner**: AI-Empower-HQ-360 DevOps Team

---

**End of Document**
