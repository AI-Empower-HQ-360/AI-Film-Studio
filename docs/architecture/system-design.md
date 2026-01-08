# System Design Document
## AI Film Studio

**Document Version:** 1.0  
**Date:** 2025-12-27  
**Author:** AI-Empower-HQ-360  
**Status:** Approved

---

## 1. Architecture Overview

### 1.1 High-Level Architecture

The AI Film Studio follows a **microservices architecture** with clear separation between:
- **Control Plane** (Backend API): Orchestration, state management, user management
- **Execution Plane** (GPU Workers): AI-powered film generation
- **Data Plane** (Storage): S3 for assets, RDS for metadata
- **Presentation Plane** (Frontend): User interface

┌─────────────┐ │ Users │ └──────┬──────┘ │ ▼ ┌─────────────────────────────────────────────┐ │ CloudFront (CDN) │ │ - S3 Frontend Hosting │ │ - Global Edge Caching │ └──────┬──────────────────────────────────────┘ │ ▼ ┌─────────────────────────────────────────────┐ │ Application Load Balancer (ALB) │ │ - TLS Termination │ │ - Health Checks │ └──────┬──────────────────────────────────────┘ │ ├─────────────────┬──────────────────┐ ▼ ▼ ▼ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │ Backend API │ │ Backend API │ │ Backend API │ │ (ECS/EKS) │ │ (ECS/EKS) │ │ (ECS/EKS) │ │ FastAPI │ │ FastAPI │ │ FastAPI │ └──────┬───────┘ └──────┬───────┘ └──────┬───────┘ │ │ │ └─────────────────┴──────────────────┘ │ ┌─────────────────┼─────────────────┐ ▼ ▼ ▼ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │ RDS Postgres │ │ SQS Queue │ │ S3 Buckets │ │ (Multi-AZ) │ │ + DLQ │ │ - Frontend │ │ │ │ │ │ - Assets │ └──────────────┘ └──────┬───────┘ └──────────────┘ │ ▼ ┌──────────────┐ │ GPU Workers │ │ (EC2/EKS) │ │ - AI Pipeline│ │ - FFmpeg │ └──────────────┘

Code

---

## 2. Component Design

### 2.1 Frontend (Next.js)

**Purpose**: User interface for project management and film generation

**Technology**:
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- React Query for data fetching

**Key Pages**:
- `/` - Landing page
- `/login` - Authentication
- `/dashboard` - Project overview
- `/projects/[id]` - Project detail and film generation
- `/projects/[id]/jobs/[jobId]` - Job progress tracking
- `/admin` - Admin dashboard

**Hosting**:
- S3 bucket with static website hosting
- CloudFront for CDN and HTTPS

**Authentication**:
- JWT tokens stored in httpOnly cookies
- API client with automatic token refresh

---

### 2.2 Backend API (FastAPI)

**Purpose**: Control plane for orchestration, auth, and state management

**Technology**:
- Python 3.11+
- FastAPI framework
- SQLAlchemy ORM
- Alembic for migrations
- Pydantic for validation

**Modules**:

#### Auth Module (`/api/v1/auth`)
- User registration and login
- JWT token generation
- Password reset workflow
- OAuth integration (Google, GitHub)

#### Projects Module (`/api/v1/projects`)
- CRUD operations for projects
- Script storage and retrieval
- Project status management

#### Jobs Module (`/api/v1/jobs`)
- Job creation and submission to SQS
- Job status tracking
- Progress updates from workers
- Signed URL generation for downloads

#### Credits Module (`/api/v1/credits`)
- Credit balance queries
- Credit deduction logic
- Purchase integration with Stripe
- Credit history

#### Admin Module (`/api/v1/admin`)
- User management
- System health dashboards
- Content moderation queues

**Database Schema**:
- Users table
- Projects table
- Jobs table
- CreditTransactions table
- Sessions table

**Hosting**:
- ECS Fargate or EKS
- Auto-scaling based on CPU/memory
- Behind Application Load Balancer

---

### 2.3 GPU Worker (Python + AI Models)

**Purpose**: Execution plane for AI-powered film generation

**Technology**:
- Python 3.11+
- PyTorch for AI models
- Stable Diffusion XL (SDXL)
- FFmpeg for video composition
- Boto3 for AWS integration

**Pipeline Stages**:

#### Stage 1: Script Analysis
- Parse user script
- Extract scenes and shots
- Generate scene graph
- Determine pacing and transitions

#### Stage 2: Prompt Engineering
- Convert scene descriptions to image prompts
- Apply style modifiers (cinematic, anime, etc.)
- Negative prompts for quality control

#### Stage 3: Image Generation
- Use SDXL to generate keyframes
- Batch processing for efficiency
- Upscaling (optional)

#### Stage 4: Video Generation (Optional)
- Animate between keyframes
- Use motion models for smooth transitions

#### Stage 5: Composition
- Assemble images/videos into timeline
- Add transitions (fade, dissolve)
- Render final MP4 with FFmpeg

#### Stage 6: Post-Processing
- Add watermark (free tier)
- Encode to H.264
- Upload to S3
- Update job status in backend

**Hosting**:
- GPU EC2 instances (g4dn.xlarge or g5.xlarge)
- EKS with GPU node groups (alternative)
- Spot instances for cost savings (70% discount)
- Auto-scaling based on SQS queue depth

**Queue Integration**:
- Poll SQS for job messages
- Visibility timeout: 15 minutes
- Dead Letter Queue (DLQ) for failed jobs
- Max 3 retry attempts

---

### 2.4 Database (RDS Postgres)

**Purpose**: Persistent storage for metadata

**Configuration**:
- PostgreSQL 15
- Multi-AZ deployment (prod)
- Instance type: db.t3.medium (dev), db.r6g.xlarge (prod)
- Storage: 100GB SSD, auto-scaling enabled
- Automated backups: Daily, 7-day retention
- Connection pooling via PgBouncer

**Schema Highlights**:

```sql
-- Users table
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    tier VARCHAR(50) DEFAULT 'free',
    credits INTEGER DEFAULT 3,
    credit_reset_date DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login_at TIMESTAMP
);

-- Projects table
CREATE TABLE projects (
    project_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    script TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'draft',
    thumbnail_url TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Jobs table
CREATE TABLE jobs (
    job_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(project_id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'queued',
    progress INTEGER DEFAULT 0,
    current_step VARCHAR(100),
    output_url TEXT,
    error_message TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Credit Transactions table
CREATE TABLE credit_transactions (
    transaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    amount INTEGER NOT NULL,
    balance_after INTEGER NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

2.5 Storage (S3)
Buckets:

Frontend Bucket
Name: ai-film-studio-frontend-{env}
Purpose: Host static Next.js site
Public read access
Versioning enabled
CloudFront origin
Assets Bucket
Name: ai-film-studio-assets-{env}
Purpose: Store scripts, images, videos, final films
Private access (signed URLs only)
Versioning enabled
Lifecycle rules: Delete objects >90 days old
Server-side encryption (SSE-S3)
Directory Structure:

Code
assets/
├── projects/
│   └── {projectId}/
│       └── script.txt
├── jobs/
│   └── {jobId}/
│       ├── scenes/
│       │   ├── scene_001.png
│       │   └── scene_002.png
│       ├── intermediate/
│       │   └── timeline.json
│       └── output/
│           └── final.mp4
2.6 Message Queue (SQS)
Queue Configuration:

Main Queue: ai-film-studio-jobs-{env}
Dead Letter Queue: ai-film-studio-jobs-dlq-{env}
Message retention: 14 days
Visibility timeout: 15 minutes (time for worker to process)
Max receive count: 3 (after 3 failures, send to DLQ)
Message Format:

JSON
{
  "jobId": "uuid",
  "projectId": "uuid",
  "userId": "uuid",
  "script": "Once upon a time...",
  "style": "cinematic",
  "priority": "normal"
}
3. Network Architecture
3.1 VPC Design
CIDR Block: 10.0.0.0/16

Subnets:

| Subnet Type | CIDR | Availability Zone | Purpose | |-------------|------|-------------------|---------|| | Public A | 10.0.1.0/24 | us-east-1a | ALB, NAT Gateway | | Public B | 10.0.2.0/24 | us-east-1b | ALB, NAT Gateway | | Private A | 10.0.10.0/24 | us-east-1a | Backend, Workers | | Private B | 10.0.11.0/24 | us-east-1b | Backend, Workers | | Data A | 10.0.20.0/24 | us-east-1a | RDS | | Data B | 10.0.21.0/24 | us-east-1b | RDS (Multi-AZ) |

3.2 Security Groups
ALB Security Group
Inbound: 443 (HTTPS) from 0.0.0.0/0
Outbound: All to backend SG
Backend Security Group
Inbound: 8000 from ALB SG
Outbound: 5432 to RDS SG, 443 to internet (for S3/SQS)
Worker Security Group
Inbound: None
Outbound: 5432 to RDS SG, 443 to internet
RDS Security Group
Inbound: 5432 from backend SG and worker SG
Outbound: None
4. Scaling Strategy
4.1 Backend Auto-Scaling
Triggers:

Scale out: CPU >70% for 2 minutes
Scale in: CPU <30% for 5 minutes
Min instances: 2 (prod), 1 (dev)
Max instances: 10 (prod), 3 (dev)
4.2 Worker Auto-Scaling
Triggers:

Scale out: SQS queue depth >10 messages
Scale in: SQS queue depth <3 messages
Min instances: 0 (dev), 1 (prod)
Max instances: 20 (prod), 5 (dev)
Use Spot Instances (70% cost savings)
Spot Instance Strategy:

Mix of g4dn.xlarge and g5.xlarge
On-Demand fallback if Spot unavailable
3-minute grace period before termination
5. Monitoring & Observability
5.1 Metrics to Track
Application Metrics:

API request rate, latency, errors
Job queue depth
Job processing time
Job success/failure rate
Credit consumption rate
Infrastructure Metrics:

EC2 CPU, memory, GPU utilization
RDS connections, query performance
S3 storage size, request count
SQS message age
5.2 CloudWatch Dashboards
Dashboard 1: API Health

Request count (last 1 hour)
Error rate (%)
p50, p95, p99 latency
Active connections
Dashboard 2: Job Processing

Queue depth
Jobs in progress
Average processing time
Failure rate
Dashboard 3: Infrastructure

EC2 instance count
GPU utilization
RDS CPU/memory
S3 storage growth
5.3 Alarms
Alarm	Threshold	Action
API Error Rate	>5%	SNS notification
Job Failure Rate	>10%	SNS notification
RDS CPU	>80%	Scale up instance
SQS DLQ Messages	>10	SNS notification
S3 Storage	>1TB	Cost review
6. Security Architecture
6.1 Authentication Flow
Code
User → Frontend → ALB → Backend API → RDS
  1. User enters credentials
  2. Frontend sends POST /auth/login
  3. Backend validates against RDS
  4. Backend generates JWT (24hr expiration)
  5. Frontend stores token in httpOnly cookie
  6. Future requests include token in Authorization header
6.2 IAM Roles
Backend ECS Task Role
S3: PutObject, GetObject on assets bucket
SQS: SendMessage on jobs queue
RDS: Connect via IAM auth (optional)
Secrets Manager: GetSecretValue
Worker ECS Task Role
S3: PutObject, GetObject on assets bucket
SQS: ReceiveMessage, DeleteMessage on jobs queue
RDS: Connect via IAM auth (optional)
6.3 Encryption
In Transit: TLS 1.2+ for all API calls
At Rest:
S3: SSE-S3 encryption
RDS: Encryption at rest enabled
Secrets Manager: Automatic encryption
7. Disaster Recovery
7.1 Backup Strategy
RDS Backups:

Automated daily snapshots (7-day retention)
Manual snapshots before major changes
Point-in-time recovery enabled
S3 Versioning:

Enabled on all buckets
Lifecycle policy to delete old versions after 30 days
Infrastructure:

Terraform state stored in S3 with versioning
Can recreate entire environment in 30 minutes
7.2 Recovery Objectives
RTO (Recovery Time Objective): 4 hours
RPO (Recovery Point Objective): 1 hour
8. Cost Optimization
8.1 Cost Breakdown (Monthly Estimates)
Service	Dev	Prod	Optimization Strategy
EC2 (Workers)	$200	$1,500	Spot instances (70% off)
ECS/EKS	$50	$300	Right-size containers
RDS	$50	$500	Reserved instances
S3	$20	$200	Lifecycle policies
CloudFront	$10	$100	Cache optimization
SQS	$5	$50	Batch processing
Total	$335	$2,650	
8.2 Cost Controls
AWS Budget alerts at 80% and 100%
Auto-scaling to prevent idle resources
Delete S3 objects >90 days old
Use Spot for non-critical workloads
9. Deployment Strategy
9.1 Blue-Green Deployment
Process:

Deploy new version to "green" environment
Run smoke tests
Gradually shift 10% traffic to green
Monitor error rates for 10 minutes
If stable, shift 100% to green
Keep blue environment for 24 hours (rollback buffer)
Decommission blue
9.2 Rollback Plan
DNS switch back to blue (30 seconds)
ECS/EKS task rollback (2 minutes)
Database migration rollback (if needed)
10. Future Enhancements
Multi-region deployment for global latency reduction
GraphQL API for flexible data fetching
WebSockets for real-time job progress
Mobile apps (iOS, Android)
Custom AI model training for enterprise customers
Kubernetes Operators for advanced orchestration
Document Control

Next Review Date: 2026-01-27
Change History: Version 1.0 - Initial release
