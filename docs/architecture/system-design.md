# System Design Document
## AI Film Studio Platform

**Document Version**: 1.0  
**Date**: 2025-12-27  
**Author**: AI-Empower-HQ-360  
**Status**: Approved

---

## 1. Executive Summary

The AI Film Studio platform is a cloud-native, microservices-based system designed to generate short films from text scripts using AI/ML models. The architecture prioritizes **scalability**, **reliability**, and **cost-efficiency** while maintaining a clean separation between the control plane (API) and execution plane (GPU workers).

---

## 2. Architecture Principles

### 2.1 Design Principles
1. **Separation of Concerns**: Frontend, backend, and workers are decoupled
2. **Scalability**: Horizontal scaling for all components
3. **Resilience**: Graceful degradation and automatic recovery
4. **Security**: Defense in depth with multiple security layers
5. **Observability**: Comprehensive logging, metrics, and tracing
6. **Cost Optimization**: Auto-scaling and resource right-sizing

### 2.2 Technology Choices
- **Cloud Provider**: AWS (mature, comprehensive services)
- **Container Orchestration**: ECS/EKS (managed, scalable)
- **Database**: PostgreSQL on RDS (ACID compliance, familiar)
- **Queue**: SQS (managed, reliable, cost-effective)
- **Storage**: S3 (durable, scalable, cheap)
- **CDN**: CloudFront (global, low-latency)

---

## 3. High-Level Architecture

┌─────────────────────────────────────────────────────────────────┐ │ User Layer │ │ ┌──────────┐ │ │ │ Browser │ ─── HTTPS ───> CloudFront CDN │ │ └──────────┘ │ │ └─────────────────────────────────────┼───────────────────────────┘ │ ┌─────────────────────────────────────┼───────────────────────────┐ │ Presentation Layer │ │ ▼ │ │ ┌────────────────────────┐ │ │ │ S3 Static Website │ │ │ │ (Next.js Frontend) │ │ │ └────────────────────────┘ │ └──────────────────────────────────────────────────────────────────┘ │ ┌─────────────────────────────────────┼───────────────────────────┐ │ API Gateway Layer │ │ ▼ │ │ ┌────────────────────────┐ │ │ │ Application Load │ │ │ │ Balancer (ALB) │ │ │ └────────────┬───────────┘ │ └─────────────────────────────────┼───────────────────────────────┘ │ ┌─────────────────────────────────┼───────────────────────────────┐ │ Application Layer │ │ ▼ │ │ ┌───────────────────────────────────┐ │ │ │ ECS/EKS Cluster │ │ │ │ ┌─────────────────────────┐ │ │ │ │ │ FastAPI Backend (3+) │ │ │ │ │ │ - Auth Service │ │ │ │ │ │ - Job Orchestrator │ │ │ │ │ │ - Project Manager │ │ │ │ │ └───────────┬─────────────┘ │ │ │ └──────────────┼───────────────────┘ │ └────────────────────────┼──────────────────────────────────────┘ │ ┌───────────────┼─────────────────┐ │ │ │ ▼ ▼ ▼ ┌────────────┐ ┌────────────┐ ┌────────────┐ │ RDS │ │ SQS │ │ S3 │ │ PostgreSQL │ │ Queue │ │ Bucket │ │ (Multi-AZ) │ │ │ │ (Assets) │ └────────────┘ └─────┬──────┘ └────────────┘ │ ┌─────────────────────┼───────────────────────────────────────────┐ │ │ Execution Layer │ │ ▼ │ │ ┌───────────────────────────────────┐ │ │ │ ECS/EKS GPU Worker Cluster │ │ │ │ ┌─────────────────────────┐ │ │ │ │ │ Worker Pods (g4dn/g5) │ │ │ │ │ │ - SQS Consumer │ │ │ │ │ │ - AI Pipeline │ │ │ │ │ │ - FFmpeg Compositor │ │ │ │ │ └───────────┬─────────────┘ │ │ │ └──────────────┼───────────────────┘ │ │ │ │ │ └─────────> S3 (Upload Results) │ └──────────────────────────────────────────────────────────────────┘

Code

---

## 4. Component Architecture

### 4.1 Frontend (Next.js)

**Technology**: Next.js 14, React, TypeScript, Tailwind CSS

**Deployment**:
- Build process generates static assets
- Deployed to S3 bucket (configured as static website)
- CloudFront distribution for global CDN
- Route 53 for custom domain

**Key Features**:
- Server-Side Rendering (SSR) for SEO
- Client-Side Rendering (CSR) for interactivity
- API routes for backend communication
- Real-time job status polling

**Pages**:
- Landing page (`/`)
- Login/Register (`/auth/login`, `/auth/register`)
- Dashboard (`/dashboard`)
- Project view (`/projects/:id`)
- Job view (`/jobs/:id`)
- Settings (`/settings`)
- Admin panel (`/admin`)

---

### 4.2 Backend API (FastAPI)

**Technology**: Python 3.11+, FastAPI, SQLAlchemy, Pydantic

**Deployment**:
- Docker container on ECS/EKS
- 3+ replicas for high availability
- Auto-scaling based on CPU/memory
- Health checks on `/health`

**Modules**:
1. **Auth Module** (`src/api/auth.py`)
   - User registration, login, JWT generation
   - Password hashing (bcrypt)
   - Token refresh

2. **Project Module** (`src/api/projects.py`)
   - CRUD operations for projects
   - List user projects with pagination

3. **Job Module** (`src/api/jobs.py`)
   - Submit script for generation
   - Query job status
   - Generate presigned download URLs

4. **Credit Module** (`src/api/credits.py`)
   - View credit balance
   - Purchase credits (future)

5. **Admin Module** (`src/api/admin.py`)
   - User management
   - System metrics
   - Content moderation

**Database ORM**:
- SQLAlchemy models
- Alembic migrations
- Connection pooling

**Queue Integration**:
- Publish jobs to SQS
- Use boto3 SDK

---

### 4.3 Worker Service (Python GPU)

**Technology**: Python 3.11+, PyTorch, Diffusers (SDXL), FFmpeg

**Deployment**:
- Docker container on ECS/EKS
- GPU instances: g4dn.xlarge (NVIDIA T4) or g5.xlarge (NVIDIA A10G)
- Auto-scaling based on SQS queue depth
- Min: 1 worker, Max: 20 workers

**Pipeline Stages**:

1. **Job Acquisition**
   - Poll SQS queue
   - Receive job message
   - Update job status → PROCESSING

2. **Script Analysis**
   - Parse script with NLP (spaCy)
   - Extract scenes, characters, actions
   - Generate scene graph

3. **Shot Generation**
   - Create AI prompts for each shot
   - Call SDXL model for image generation
   - Optional: Use video generation model (SVD, AnimateDiff)
   - Upload shots to S3

4. **Composition**
   - Use FFmpeg to:
     - Concatenate images/clips
     - Add transitions (fade, dissolve)
     - Apply filters (color grading)
     - Add background music (optional)
   - Render final MP4 (H.264, 1080p)
   - Upload to S3

5. **Completion**
   - Update job status → COMPLETED
   - Store output_url in database
   - Delete SQS message

**Error Handling**:
- Retry logic: 3 attempts
- Exponential backoff
- Log errors to CloudWatch
- Update job status → FAILED with error message

---

### 4.4 Data Layer

#### 4.4.1 RDS PostgreSQL

**Configuration**:
- Engine: PostgreSQL 15
- Instance: db.t3.medium (Dev), db.m5.large (Prod)
- Multi-AZ: Enabled (Prod)
- Automated backups: Daily, 7-day retention
- Encryption: AES-256

**Schema**:
```sql
-- Users
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    credits INTEGER DEFAULT 100,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Projects
CREATE TABLE projects (
    project_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Jobs
CREATE TABLE jobs (
    job_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(project_id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    script TEXT NOT NULL,
    style VARCHAR(50) DEFAULT 'cinematic',
    duration_target INTEGER DEFAULT 60,
    status VARCHAR(20) DEFAULT 'QUEUED',
    progress INTEGER DEFAULT 0,
    output_url TEXT,
    thumbnail_url TEXT,
    error_message TEXT,
    credits_used INTEGER DEFAULT 10,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- Indexes
CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_jobs_user_id ON jobs(user_id);
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_created_at ON jobs(created_at);
```

#### 4.4.2 Amazon S3
Buckets:

Frontend Bucket (ai-film-studio-frontend-{env})

Purpose: Host Next.js static assets
Versioning: Enabled
Public read access via CloudFront

Assets Bucket (ai-film-studio-assets-{env})

Purpose: Store scripts, images, video clips, final films
Versioning: Enabled
Encryption: AES-256 (SSE-S3)
Lifecycle: Delete objects > 30 days old
Path structure:
/scripts/{job_id}.txt
/shots/{job_id}/scene_{n}_shot_{m}.png
/films/{job_id}/final.mp4
/thumbnails/{job_id}/thumb.jpg

#### 4.4.3 Amazon SQS
Queue: ai-film-studio-jobs-{env}

Configuration:

Visibility timeout: 600 seconds (10 minutes)
Message retention: 14 days
Dead Letter Queue (DLQ): After 3 retries
Max message size: 256 KB
Message Format:

JSON
{
  "job_id": "uuid",
  "user_id": "uuid",
  "project_id": "uuid",
  "script": "text",
  "style": "cinematic",
  "duration_target": 60,
  "timestamp": "ISO8601"
}

## 5. Network Architecture
### 5.1 VPC Design

Code
VPC: 10.0.0.0/16 (ai-film-studio-vpc)

├── Public Subnets (Internet-facing)
│   ├── 10.0.1.0/24 (us-east-1a) - ALB, NAT Gateway
│   └── 10.0.2.0/24 (us-east-1b) - ALB, NAT Gateway
│
├── Private Subnets (Application Layer)
│   ├── 10.0.10.0/24 (us-east-1a) - Backend ECS/EKS
│   └── 10.0.11.0/24 (us-east-1b) - Backend ECS/EKS
│
├── Private Subnets (Worker Layer)
│   ├── 10.0.20.0/24 (us-east-1a) - GPU Workers
│   └── 10.0.21.0/24 (us-east-1b) - GPU Workers
│
└── Private Subnets (Data Layer)
    ├── 10.0.30.0/24 (us-east-1a) - RDS Primary
    └── 10.0.31.0/24 (us-east-1b) - RDS Standby

### 5.2 Security Groups
ALB Security Group (sg-alb)

Inbound: 443 (HTTPS) from 0.0.0.0/0
Outbound: All traffic

Backend Security Group (sg-backend)

Inbound: 8000 (FastAPI) from ALB SG
Outbound: 443 (HTTPS), 5432 (Postgres to RDS SG)

Worker Security Group (sg-worker)

Inbound: None
Outbound: 443 (HTTPS for S3, SQS), 5432 (Postgres to RDS SG)

RDS Security Group (sg-rds)

Inbound: 5432 from Backend SG, Worker SG
Outbound: None

---

## 6. Data Flow Diagrams
### 6.1 User Registration Flow

Code
User → CloudFront → ALB → Backend API
                              │
                              ├─> Validate input
                              ├─> Hash password
                              ├─> Insert into RDS
                              ├─> Assign 100 credits
                              └─> Return JWT token

### 6.2 Film Generation Flow

Code
1. User submits script via Frontend
   ↓
2. Backend validates script, checks credits
   ↓
3. Backend creates job record in RDS (status: QUEUED)
   ↓
4. Backend publishes job to SQS
   ↓
5. Backend returns job_id to user
   ↓
6. Worker polls SQS, receives job
   ↓
7. Worker updates job status → PROCESSING
   ↓
8. Worker executes AI pipeline:
   - Script analysis
   - Scene breakdown
   - Shot generation (SDXL)
   - Composition (FFmpeg)
   ↓
9. Worker uploads final MP4 to S3
   ↓
10. Worker updates job status → COMPLETED, stores output_url
   ↓
11. User polls /api/v1/jobs/{job_id}, receives output_url
   ↓
12. User downloads film via presigned S3 URL

---

## 7. Scaling Strategy
### 7.1 Backend Auto-Scaling
Metrics:

Target CPU: 70%
Target Memory: 75%
Scale-out: Add 1 instance if avg > threshold for 2 minutes
Scale-in: Remove 1 instance if avg < 50% for 10 minutes
Min: 2 instances
Max: 10 instances

### 7.2 Worker Auto-Scaling
Metrics:

SQS ApproximateNumberOfMessagesVisible
Target: 5 messages per worker
Scale-out: If queue depth > 5 * current workers
Scale-in: If queue depth < 2 * current workers (wait 10 min)
Min: 1 worker (Dev), 2 workers (Prod)
Max: 20 workers
Cost Optimization:

Use Spot instances for workers (60-70% cost savings)
Spot interruption handling: Gracefully finish current job, then terminate

---

## 8. Disaster Recovery
### 8.1 Backup Strategy
RDS:

Automated daily snapshots (7-day retention)
Point-in-time recovery enabled
Manual snapshots before major changes

S3:

Versioning enabled
Cross-region replication (optional for critical data)
Configuration:

Terraform state in S3 with versioning
Infrastructure as Code for rapid rebuild

### 8.2 Recovery Procedures
Scenario: RDS Failure

Automatic failover to Multi-AZ standby (< 2 minutes)
DNS update handled by RDS
Backend reconnects automatically

Scenario: Region Outage

Restore RDS from snapshot in alternate region
Sync S3 data from replica
Deploy infrastructure via Terraform
Update Route 53 to point to new region

---

## 9. Security Architecture
### 9.1 Defense in Depth
Layer 1: Edge (CloudFront + WAF)

DDoS protection
Geographic restrictions (optional)
Rate limiting

Layer 2: Network (VPC + Security Groups)

Subnet isolation
Security groups with least-privilege rules
No public IPs on backend/workers

Layer 3: Application (Backend API)

JWT authentication
Input validation (Pydantic)
SQL injection prevention (SQLAlchemy ORM)
CORS policy

Layer 4: Data (Encryption)

TLS in transit
AES-256 at rest
Secrets Manager for credentials

### 9.2 IAM Roles
Backend Role (ai-film-studio-backend-role)

Permissions: S3 read/write, SQS publish, RDS connect, Secrets Manager read

Worker Role (ai-film-studio-worker-role)

Permissions: SQS consume, S3 read/write, RDS connect

ECS Task Execution Role (ecs-task-execution-role)

Permissions: ECR pull, CloudWatch Logs write

---

## 10. Monitoring & Observability
### 10.1 CloudWatch Dashboards
API Dashboard:

Request count (by endpoint)
Latency (p50, p95, p99)
Error rate (4xx, 5xx)
Active connections

Worker Dashboard:

Queue depth
Active workers
Job processing time
Success/failure rate

Infrastructure Dashboard:

EC2 CPU, memory, disk
RDS connections, CPU, IOPS
S3 request rate

### 10.2 Alarms
Alarm	Threshold	Action
API error rate	> 5% for 5 min	SNS → Slack
Job failure rate	> 10% for 10 min	SNS → PagerDuty
RDS CPU	> 80% for 5 min	SNS → Slack
Queue depth	> 100 for 10 min	SNS → Slack
Disk usage	> 85%	SNS → Email

---

## 11. Cost Estimation
### 11.1 Monthly AWS Costs (Production)
Service	Configuration	Cost
EC2 (Backend)	3 × t3.medium	$90
EC2 (Workers)	5 × g4dn.xlarge (avg)	$1,200
RDS	db.m5.large Multi-AZ	$300
S3	1TB storage + requests	$30
CloudFront	1TB egress	$85
ALB	1 ALB	$25
SQS, CloudWatch, etc.	-	$70
Total	-	~$1,800/month

### 11.2 Cost Optimization Strategies
Use Spot instances for workers (save 60%)
Implement S3 lifecycle policies
Use CloudFront caching to reduce origin requests
Right-size instances based on metrics

---

## 12. Future Enhancements
Phase 2
Real-time collaboration features
Advanced video editing tools
Voice synthesis and audio generation
Custom AI model training by users

Phase 3
Multi-region deployment for global redundancy
Edge computing for faster processing (AWS Wavelength)
Mobile native applications (React Native)
Third-party integrations (YouTube, TikTok, social media)

---

## 13. Approval
Role	Name	Signature	Date
Chief Architect	AI-Empower-HQ-360	✅ Approved	2025-12-27
DevOps Lead	TBD	✅ Approved	2025-12-27
