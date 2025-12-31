# 🎬 AI Film Studio — Environment Setup Master Checklist

**Complete setup guide for Dev, Sandbox, Staging, and Production environments**

---

## 📋 Table of Contents

- [Overview](#overview)
- [Environment Strategy](#environment-strategy)
- [1️⃣ Version Control Setup](#1️⃣-version-control-setup)
- [2️⃣ AWS Account Setup](#2️⃣-aws-account-setup)
- [3️⃣ Salesforce Setup](#3️⃣-salesforce-setup)
- [4️⃣ YouTube / Google Setup](#4️⃣-youtube--google-setup)
- [5️⃣ AI / ML Models & Tools](#5️⃣-ai--ml-models--tools)
- [6️⃣ Frontend / Backend Setup](#6️⃣-frontend--backend-setup)
- [7️⃣ Environment Files Configuration](#7️⃣-environment-files-configuration)
- [8️⃣ Optional Tools & Services](#8️⃣-optional-tools--services)
- [9️⃣ Environment Mapping Summary](#9️⃣-environment-mapping-summary)
- [Setup Checklist by Environment](#setup-checklist-by-environment)

---

## 📖 Overview

This document provides a comprehensive checklist for setting up all required accounts, credentials, and environment configurations for the AI Film Studio platform across Dev, Sandbox, Staging, and Production environments.

**Important Notes:**
- Complete each section sequentially
- Mark items as complete using checkboxes
- Store all credentials securely using AWS Secrets Manager
- Never commit sensitive data to version control

---

## 🌍 Environment Strategy

| Environment | Purpose | Infrastructure Scale | Data |
|-------------|---------|---------------------|------|
| **Dev** | Local development & unit testing | Minimal (local/small instances) | Sample/mock data |
| **Sandbox** | Integration testing & QA | Small AWS instances | Test data |
| **Staging** | Pre-production validation | Production-like setup | Anonymized prod data |
| **Production** | Live service | Full scale, HA, multi-AZ | Real user data |

---

## 1️⃣ Version Control Setup

### GitHub Repository Setup

- [ ] **Create GitHub Account/Organization**
  - Organization: `AI-Empower-HQ-360`
  - Repository: `AI-Film-Studio`

- [ ] **Repository Structure**
  - [ ] Create repository with appropriate visibility (Private/Public)
  - [ ] Initialize with README.md
  - [ ] Add LICENSE file (MIT recommended)
  - [ ] Add .gitignore for Python, Node.js, Terraform

- [ ] **Branch Strategy**
  - [ ] Create `main` branch (production-ready code)
  - [ ] Create `staging` branch (pre-production)
  - [ ] Create `sandbox` branch (QA/testing)
  - [ ] Create `dev` branch (active development)
  - [ ] Set up branch protection rules for `main` and `staging`

- [ ] **GitHub Copilot** (Optional)
  - [ ] Enable GitHub Copilot for AI-assisted development
  - [ ] Configure for team members

- [ ] **GitHub Actions**
  - [ ] Enable GitHub Actions for CI/CD
  - [ ] Set up secrets for AWS, Salesforce, YouTube credentials
  - [ ] Configure workflow permissions

- [ ] **Collaborators & Access**
  - [ ] Add team members with appropriate roles
  - [ ] Set up CODEOWNERS file
  - [ ] Configure required reviewers

---

## 2️⃣ AWS Account Setup

### Prerequisites

- [ ] **AWS Account Creation**
  - [ ] Create AWS account or use existing
  - [ ] Enable MFA for root account
  - [ ] Create IAM admin user for daily operations

- [ ] **AWS Organizations (Recommended for multi-environment)**
  - [ ] Create AWS Organization
  - [ ] Create separate accounts for Dev, Sandbox, Staging, Production
  - [ ] Set up consolidated billing

### IAM Setup

- [ ] **IAM Users & Roles**
  - [ ] Create IAM users for developers
  - [ ] Create service roles for EC2, ECS, Lambda
  - [ ] Set up cross-account roles if using AWS Organizations
  - [ ] Enable MFA for all IAM users

- [ ] **IAM Policies**
  - [ ] Create custom policies for least-privilege access
  - [ ] Document policy requirements

### AWS Services Configuration

#### Compute Resources

- [ ] **EC2 GPU Instances** (for AI processing)
  - **Dev Environment:**
    - [ ] Launch 1 small GPU instance (g4dn.xlarge or g5.xlarge)
    - [ ] Configure security groups
    - [ ] Set up SSH key pairs
  - **Sandbox Environment:**
    - [ ] Launch 1-2 GPU instances for testing
  - **Staging Environment:**
    - [ ] Launch 2 GPU instances (mirrors production)
  - **Production Environment:**
    - [ ] Launch auto-scaling group with 2+ GPU instances (g5.2xlarge or p3.2xlarge)
    - [ ] Configure spot instances for cost optimization
    - [ ] Set up monitoring and auto-recovery

- [ ] **ECS/EKS Setup** (Backend microservices)
  - **Dev Environment:**
    - [ ] Create ECS cluster with Fargate (2 vCPU, 4GB RAM)
    - OR
    - [ ] Create EKS cluster with 2 t3.medium nodes
  - **Sandbox Environment:**
    - [ ] Set up similar to Dev
  - **Staging Environment:**
    - [ ] Set up ECS/EKS cluster (production-like)
  - **Production Environment:**
    - [ ] Create ECS/EKS cluster with auto-scaling
    - [ ] Configure load balancer
    - [ ] Set up service mesh (optional)

#### Storage

- [ ] **S3 Buckets**
  - **Dev Environment:**
    - [ ] Create bucket: `ai-film-studio-dev-media`
    - [ ] Enable versioning
    - [ ] Configure lifecycle policies (delete after 30 days)
    - [ ] Set up CORS for web access
  - **Sandbox Environment:**
    - [ ] Create bucket: `ai-film-studio-sandbox-media`
    - [ ] Enable versioning
    - [ ] Configure lifecycle policies
  - **Staging Environment:**
    - [ ] Create bucket: `ai-film-studio-staging-media`
    - [ ] Enable versioning
    - [ ] Enable encryption (SSE-S3 or SSE-KMS)
  - **Production Environment:**
    - [ ] Create bucket: `ai-film-studio-prod-media`
    - [ ] Enable versioning
    - [ ] Enable encryption (SSE-KMS)
    - [ ] Enable access logging
    - [ ] Configure lifecycle policies for archival
    - [ ] Set up cross-region replication (optional)

- [ ] **S3 Bucket Organization**
  - [ ] Create folders: `/scripts`, `/images`, `/videos`, `/audio`, `/thumbnails`, `/subtitles`
  - [ ] Set up bucket policies for secure access

#### Content Delivery

- [ ] **CloudFront CDN**
  - **Dev Environment:** (Optional)
    - [ ] Skip or create basic distribution
  - **Sandbox Environment:** (Optional)
    - [ ] Create CloudFront distribution if testing CDN
  - **Staging Environment:**
    - [ ] Create CloudFront distribution
    - [ ] Configure origin (S3 bucket)
    - [ ] Set up caching behavior
    - [ ] Add custom domain (staging.aifilmstudio.com)
  - **Production Environment:**
    - [ ] Create CloudFront distribution
    - [ ] Configure multiple origins
    - [ ] Set up caching and compression
    - [ ] Enable field-level encryption
    - [ ] Add custom domain (www.aifilmstudio.com)
    - [ ] Configure SSL certificate (ACM)
    - [ ] Set up geo-restrictions if needed

#### Database

- [ ] **RDS (PostgreSQL/MySQL)**
  - **Dev Environment:**
    - [ ] Create RDS instance (db.t3.micro, single-AZ)
    - [ ] Database name: `ai_film_studio_dev`
    - [ ] Configure security group (allow from dev IPs)
    - [ ] Enable automated backups (1 day retention)
  - **Sandbox Environment:**
    - [ ] Create RDS instance (db.t3.small, single-AZ)
    - [ ] Database name: `ai_film_studio_sandbox`
    - [ ] Configure security group
  - **Staging Environment:**
    - [ ] Create RDS instance (db.r5.large, Multi-AZ)
    - [ ] Database name: `ai_film_studio_staging`
    - [ ] Enable automated backups (7 days)
    - [ ] Configure security group (VPC only)
  - **Production Environment:**
    - [ ] Create RDS instance (db.r5.xlarge or larger, Multi-AZ)
    - [ ] Database name: `ai_film_studio_prod`
    - [ ] Enable automated backups (30 days)
    - [ ] Set up read replicas
    - [ ] Enable encryption at rest
    - [ ] Configure enhanced monitoring
    - [ ] Set up CloudWatch alarms

- [ ] **Database Schema**
  - [ ] Create tables: `users`, `projects`, `ai_credits`, `jobs`, `videos`, `youtube_integrations`
  - [ ] Run migration scripts
  - [ ] Set up indexes for performance

#### Caching

- [ ] **ElastiCache (Redis)**
  - **Dev Environment:** (Optional)
    - [ ] Create single Redis node (cache.t3.micro) OR use local Redis
  - **Sandbox Environment:**
    - [ ] Create Redis cluster (cache.t3.small, 1 node)
  - **Staging Environment:**
    - [ ] Create Redis cluster (cache.r5.large, 2 nodes)
  - **Production Environment:**
    - [ ] Create Redis cluster (cache.r5.large or larger, 3+ nodes)
    - [ ] Enable cluster mode
    - [ ] Configure automatic failover
    - [ ] Set up CloudWatch alarms

#### Messaging & Queuing

- [ ] **SQS (Job Queue)**
  - **Dev Environment:**
    - [ ] Create standard queue: `ai-film-studio-dev-jobs`
  - **Sandbox Environment:**
    - [ ] Create standard queue: `ai-film-studio-sandbox-jobs`
  - **Staging Environment:**
    - [ ] Create standard queue: `ai-film-studio-staging-jobs`
    - [ ] Create DLQ (Dead Letter Queue)
  - **Production Environment:**
    - [ ] Create standard queue: `ai-film-studio-prod-jobs`
    - [ ] Create DLQ with appropriate retention
    - [ ] Set up CloudWatch alarms for queue depth
    - [ ] Configure message retention and visibility timeout

#### Secrets Management

- [ ] **AWS Secrets Manager / Parameter Store**
  - **All Environments:**
    - [ ] Store database credentials
    - [ ] Store API keys (Salesforce, YouTube, AI services)
    - [ ] Store JWT secrets
    - [ ] Store encryption keys
    - [ ] Store third-party service credentials
  - [ ] Set up automatic rotation for database credentials
  - [ ] Configure IAM policies for secret access

#### Monitoring & Logging

- [ ] **CloudWatch**
  - **All Environments:**
    - [ ] Create log groups for each service
    - [ ] Set up custom metrics
    - [ ] Configure alarms for critical metrics
  - **Production Environment:**
    - [ ] Set up detailed monitoring
    - [ ] Configure SNS topics for alerts
    - [ ] Set up CloudWatch Dashboards

- [ ] **Prometheus & Grafana** (Optional)
  - [ ] Deploy Prometheus for metrics collection
  - [ ] Deploy Grafana for visualization
  - [ ] Create dashboards for system health

- [ ] **AWS X-Ray** (Optional)
  - [ ] Enable X-Ray tracing for distributed services
  - [ ] Configure sampling rules

#### Networking

- [ ] **VPC Configuration**
  - **Each Environment:**
    - [ ] Create VPC with CIDR block (10.0.0.0/16 for dev, 10.1.0.0/16 for prod, etc.)
    - [ ] Create public subnets (for load balancers)
    - [ ] Create private subnets (for application servers)
    - [ ] Create database subnets (for RDS)
    - [ ] Set up Internet Gateway
    - [ ] Set up NAT Gateway (staging/prod)
    - [ ] Configure route tables
    - [ ] Set up security groups and NACLs

#### Infrastructure as Code

- [ ] **Terraform Setup**
  - [ ] Install Terraform (>= 1.5)
  - [ ] Create S3 bucket for Terraform state
  - [ ] Configure state locking with DynamoDB
  - [ ] Create `.tfvars` files:
    - [ ] `dev.tfvars`
    - [ ] `sandbox.tfvars`
    - [ ] `staging.tfvars`
    - [ ] `prod.tfvars`
  - [ ] Document Terraform modules and variables
  - [ ] Set up Terraform Cloud/Enterprise (optional)

---

## 3️⃣ Salesforce Setup

### Salesforce Account Creation

- [ ] **Developer Edition** (Free)
  - [ ] Sign up at: https://developer.salesforce.com/signup
  - [ ] Complete email verification
  - [ ] Set up security questions
  - [ ] Enable MFA

- [ ] **Salesforce Organizations**
  - **Dev/Sandbox:**
    - [ ] Use single free Developer Edition org
  - **Production:**
    - [ ] Upgrade to paid Salesforce org OR
    - [ ] Create separate Production org

### Custom Objects

- [ ] **Create Custom Objects**
  - [ ] `AI_Project__c`
    - Fields: Name, User__c, Status__c, Script__c, Video_URL__c, Created_Date__c
  - [ ] `AI_Credit__c`
    - Fields: User__c, Credits_Remaining__c, Credits_Used__c, Purchase_Date__c
  - [ ] `YouTube_Integration__c`
    - Fields: Project__c, YouTube_Video_ID__c, Upload_Status__c, Views__c

- [ ] **Set up relationships**
  - [ ] Link AI_Project__c to AI_Credit__c
  - [ ] Link YouTube_Integration__c to AI_Project__c

### Automation

- [ ] **Flows**
  - [ ] Create flow for credit deduction on project creation
  - [ ] Create flow for project status updates
  - [ ] Create flow for alert notifications
  - [ ] Test flows in Sandbox before deploying to Production

- [ ] **Apex Classes** (if needed)
  - [ ] Write Apex triggers for complex business logic
  - [ ] Create test classes (minimum 75% code coverage)

### Reports & Dashboards

- [ ] **Reports**
  - [ ] Projects by status
  - [ ] Credits usage by user
  - [ ] YouTube video metrics
  - [ ] Failed jobs report

- [ ] **Dashboards**
  - [ ] Executive dashboard (high-level metrics)
  - [ ] Operations dashboard (system health)
  - [ ] User activity dashboard

### API Setup

- [ ] **REST/SOAP API Access**
  - **Dev/Sandbox:**
    - [ ] Create Connected App in Salesforce
    - [ ] Note Consumer Key (Client ID)
    - [ ] Note Consumer Secret (Client Secret)
    - [ ] Set OAuth scopes (api, refresh_token)
    - [ ] Store credentials in AWS Secrets Manager
  - **Production:**
    - [ ] Create separate Connected App for production
    - [ ] Configure IP restrictions
    - [ ] Set up refresh token flow

- [ ] **Test API Connection**
  - [ ] Use Postman or curl to test authentication
  - [ ] Verify CRUD operations on custom objects

---

## 4️⃣ YouTube / Google Setup

### Google Account Setup

- [ ] **Google Account**
  - [ ] Create or use existing Google Account
  - [ ] Enable 2-factor authentication

- [ ] **YouTube Channel**
  - [ ] Create YouTube channel
  - [ ] Complete channel setup (name, description, branding)
  - [ ] Verify YouTube account (for videos >15 minutes)

### YouTube Data API

- [ ] **Google Cloud Project**
  - [ ] Go to: https://console.cloud.google.com
  - [ ] Create new project: `AI-Film-Studio`
  - [ ] Enable billing (required for API usage)

- [ ] **Enable YouTube Data API v3**
  - [ ] Navigate to APIs & Services → Library
  - [ ] Search for "YouTube Data API v3"
  - [ ] Enable the API

- [ ] **Create OAuth 2.0 Credentials**
  - [ ] Go to APIs & Services → Credentials
  - [ ] Create OAuth 2.0 Client ID
  - [ ] Application type: Web application
  - [ ] Authorized redirect URIs:
    - Dev: `http://localhost:3000/api/auth/youtube/callback`
    - Sandbox: `https://sandbox.aifilmstudio.com/api/auth/youtube/callback`
    - Staging: `https://staging.aifilmstudio.com/api/auth/youtube/callback`
    - Production: `https://www.aifilmstudio.com/api/auth/youtube/callback`
  - [ ] Note Client ID
  - [ ] Note Client Secret
  - [ ] Store in AWS Secrets Manager

- [ ] **API Quotas**
  - [ ] Review default quota (10,000 units/day)
  - [ ] Request quota increase if needed
  - [ ] Set up quota monitoring

### Optional: User-Provided Credentials

- [ ] **Allow User OAuth**
  - [ ] Implement OAuth flow for users to connect their YouTube accounts
  - [ ] Store user tokens securely (encrypted in database)
  - [ ] Implement token refresh logic

---

## 5️⃣ AI / ML Models & Tools

### Image Generation

- [ ] **Stable Diffusion**
  - [ ] Install Stable Diffusion XL (SDXL)
  - [ ] Download model weights (e.g., from Hugging Face)
  - [ ] Configure model cache directory
  - [ ] Test image generation locally

- [ ] **Alternative Models**
  - [ ] LTX-2 (if applicable)
  - [ ] Dream Machine API credentials
  - [ ] Runway ML API credentials (if using)

### Video Generation

- [ ] **Custom Video Models**
  - [ ] Identify and download pre-trained models
  - [ ] Set up model serving infrastructure

### Voice Synthesis (Text-to-Speech)

- [ ] **ElevenLabs** (Recommended)
  - [ ] Sign up: https://elevenlabs.io
  - [ ] Get API key
  - [ ] Store in AWS Secrets Manager
  - [ ] Test API calls

- [ ] **Alternative TTS**
  - [ ] Coqui TTS (open-source option)
  - [ ] Google Text-to-Speech API
  - [ ] AWS Polly

### Lip-sync / Animation

- [ ] **Wav2Lip**
  - [ ] Clone repository: https://github.com/Rudrabha/Wav2Lip
  - [ ] Download pre-trained model
  - [ ] Set up inference pipeline
  - [ ] Test on sample video

### Music / Audio

- [ ] **Music Generation**
  - [ ] Indian classical music models (if available)
  - [ ] Western music generation (e.g., MusicGen)
  - [ ] Slokas/Poems audio (pre-recorded or TTS)

### Podcast / Dialogue Mode

- [ ] **Multi-Character Dialogue**
  - [ ] Set up voice cloning for different characters
  - [ ] Test two-character conversation flow

### GPU Access

- [ ] **Development/Testing**
  - [ ] Local GPU (NVIDIA with CUDA) OR
  - [ ] Google Colab Pro subscription OR
  - [ ] AWS EC2 GPU instances (see AWS section)

- [ ] **Production**
  - [ ] AWS EC2 GPU instances with auto-scaling
  - [ ] Set up GPU monitoring and health checks

---

## 6️⃣ Frontend / Backend Setup

### Frontend (Next.js + React)

- [ ] **Technology Stack**
  - [ ] Next.js 14+
  - [ ] TypeScript
  - [ ] TailwindCSS or Material UI
  - [ ] React Query for data fetching
  - [ ] Axios for API calls

- [ ] **Environment Configuration**
  - **Dev:**
    - [ ] API endpoint: `http://localhost:8000`
  - **Sandbox:**
    - [ ] API endpoint: `https://api-sandbox.aifilmstudio.com`
  - **Staging:**
    - [ ] API endpoint: `https://api-staging.aifilmstudio.com`
  - **Production:**
    - [ ] API endpoint: `https://api.aifilmstudio.com`

- [ ] **Deployment**
  - [ ] Build for each environment
  - [ ] Deploy to S3 + CloudFront
  - [ ] Configure custom domains

### Backend (Node.js/NestJS or Python/FastAPI)

- [ ] **Technology Stack**
  - [ ] Python 3.11+ with FastAPI OR
  - [ ] Node.js 18+ with NestJS
  - [ ] PostgreSQL (via RDS)
  - [ ] Redis (via ElastiCache)
  - [ ] JWT for authentication

- [ ] **Microservices**
  - [ ] User Service (authentication, profile)
  - [ ] Project Service (CRUD operations)
  - [ ] Credit Service (purchase, deduction)
  - [ ] AI Job Service (queue management)
  - [ ] YouTube Service (video upload)
  - [ ] Admin Service (dashboard, reports)

- [ ] **Environment Configuration**
  - [ ] Connect to RDS (database URL per environment)
  - [ ] Connect to Redis (cache URL per environment)
  - [ ] Connect to S3 (bucket names per environment)
  - [ ] Connect to SQS (queue URLs per environment)

- [ ] **Deployment**
  - [ ] Build Docker images
  - [ ] Push to Amazon ECR
  - [ ] Deploy to ECS/EKS
  - [ ] Configure load balancer

### Async Job Processing

- [ ] **Redis / BullMQ**
  - [ ] Set up job queues (video generation, thumbnail creation, upload)
  - [ ] Configure separate queues per environment
  - [ ] Set up job monitoring dashboard

### Authentication & Authorization

- [ ] **JWT Implementation**
  - [ ] Generate JWT secrets for each environment
  - [ ] Implement login/register endpoints
  - [ ] Implement token refresh logic
  - [ ] Add middleware for protected routes

- [ ] **OAuth2** (Optional)
  - [ ] Set up OAuth providers (Google, GitHub)

---

## 7️⃣ Environment Files Configuration

### File Naming Convention

```
.env.dev
.env.sandbox
.env.staging
.env.prod
terraform.tfvars (per environment)
```

### Required Variables

Create environment files with the following variables:

#### Backend .env Files

```bash
# Environment
NODE_ENV=development|sandbox|staging|production
APP_ENV=dev|sandbox|staging|prod

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_BASE_URL=https://api.aifilmstudio.com

# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname
DATABASE_HOST=
DATABASE_PORT=5432
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=

# Redis
REDIS_URL=redis://host:6379
REDIS_HOST=
REDIS_PORT=6379
REDIS_PASSWORD=

# AWS
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
S3_BUCKET_NAME=ai-film-studio-[env]-media
SQS_QUEUE_URL=

# Salesforce
SALESFORCE_CLIENT_ID=
SALESFORCE_CLIENT_SECRET=
SALESFORCE_USERNAME=
SALESFORCE_PASSWORD=
SALESFORCE_SECURITY_TOKEN=
SALESFORCE_INSTANCE_URL=https://[instance].salesforce.com

# YouTube
YOUTUBE_API_KEY=
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=
YOUTUBE_REDIRECT_URI=

# JWT
JWT_SECRET=
JWT_EXPIRES_IN=7d
JWT_REFRESH_SECRET=
JWT_REFRESH_EXPIRES_IN=30d

# AI Services
ELEVENLABS_API_KEY=
RUNWAY_API_KEY=
DREAM_MACHINE_API_KEY=

# Feature Flags
ENABLE_PODCAST_MODE=true|false
ENABLE_SLOKAS_MODE=true|false
ENABLE_MULTI_LANGUAGE=true|false
ENABLE_INDIAN_MUSIC=true|false
ENABLE_WESTERN_MUSIC=true|false

# AI Model Configuration
MODEL_CACHE_DIR=/app/models
GPU_DEVICE_ID=0
STABLE_DIFFUSION_MODEL=stabilityai/stable-diffusion-xl-base-1.0

# Media Storage
TEMP_MEDIA_PATH=/tmp/media
UPLOAD_MAX_SIZE=100MB

# Logging
LOG_LEVEL=DEBUG|INFO|WARNING|ERROR
LOG_FORMAT=json

# Monitoring
SENTRY_DSN=
CLOUDWATCH_LOG_GROUP=
```

#### Frontend .env Files

```bash
# Environment
NEXT_PUBLIC_ENV=dev|sandbox|staging|prod

# API
NEXT_PUBLIC_API_BASE_URL=https://api.aifilmstudio.com

# Authentication
NEXT_PUBLIC_JWT_COOKIE_NAME=ai_film_studio_token

# Feature Flags
NEXT_PUBLIC_ENABLE_PODCAST=true|false
NEXT_PUBLIC_ENABLE_SLOKAS=true|false
NEXT_PUBLIC_ENABLE_MULTI_LANGUAGE=true|false

# Analytics (Optional)
NEXT_PUBLIC_GA_TRACKING_ID=
NEXT_PUBLIC_HOTJAR_ID=
```

#### Terraform .tfvars Files

```hcl
# terraform.dev.tfvars
environment = "dev"
aws_region = "us-east-1"

# VPC
vpc_cidr = "10.0.0.0/16"

# EC2
gpu_instance_type = "g4dn.xlarge"
gpu_instance_count = 1

# RDS
rds_instance_class = "db.t3.micro"
rds_allocated_storage = 20
rds_multi_az = false

# ElastiCache
redis_node_type = "cache.t3.micro"
redis_num_cache_nodes = 1

# ECS
ecs_desired_count = 1
ecs_cpu = 256
ecs_memory = 512

# Tags
tags = {
  Environment = "dev"
  Project     = "AI-Film-Studio"
  ManagedBy   = "Terraform"
}
```

### Environment File Checklist

- [ ] **Dev Environment**
  - [ ] Create `.env.dev`
  - [ ] Populate all variables with dev values
  - [ ] Test locally
  - [ ] Store secrets in AWS Secrets Manager

- [ ] **Sandbox Environment**
  - [ ] Create `.env.sandbox`
  - [ ] Populate all variables with sandbox values
  - [ ] Store secrets in AWS Secrets Manager

- [ ] **Staging Environment**
  - [ ] Create `.env.staging`
  - [ ] Populate all variables with staging values
  - [ ] Use production-like configuration
  - [ ] Store secrets in AWS Secrets Manager

- [ ] **Production Environment**
  - [ ] Create `.env.prod`
  - [ ] Populate all variables with production values
  - [ ] Use strong, unique secrets
  - [ ] Store secrets in AWS Secrets Manager
  - [ ] Enable encryption for sensitive data

---

## 8️⃣ Optional Tools & Services

### Containerization

- [ ] **Docker**
  - [ ] Install Docker Desktop
  - [ ] Create Dockerfile for backend
  - [ ] Create Dockerfile for AI worker
  - [ ] Create docker-compose.yml for local development

### Container Orchestration

- [ ] **Kubernetes (EKS)**
  - [ ] Create Kubernetes manifests (deployments, services, ingress)
  - [ ] Set up Helm charts for easier deployment
  - [ ] Configure kubectl access

- [ ] **ECS (Alternative to EKS)**
  - [ ] Create ECS task definitions
  - [ ] Create ECS services
  - [ ] Configure Application Load Balancer

### Infrastructure as Code

- [ ] **Terraform**
  - [ ] Create modular Terraform code
  - [ ] Set up remote state management
  - [ ] Create separate workspaces per environment
  - [ ] Document Terraform usage

### Monitoring & Observability

- [ ] **CloudWatch**
  - [ ] Set up custom metrics
  - [ ] Create CloudWatch dashboards
  - [ ] Configure alarms and SNS notifications

- [ ] **Prometheus + Grafana**
  - [ ] Deploy Prometheus for metrics scraping
  - [ ] Deploy Grafana for visualization
  - [ ] Create custom dashboards

- [ ] **Sentry** (Error Tracking)
  - [ ] Sign up for Sentry
  - [ ] Integrate Sentry SDK in backend/frontend
  - [ ] Configure error alerting

### CI/CD

- [ ] **GitHub Actions**
  - [ ] Create workflow for backend CI/CD
  - [ ] Create workflow for frontend CI/CD
  - [ ] Create workflow for AI worker CI/CD
  - [ ] Create workflow for Terraform deployments
  - [ ] Set up deployment approvals for staging/prod

- [ ] **AWS CodePipeline** (Alternative)
  - [ ] Create pipeline for each service
  - [ ] Configure build and deploy stages

### Cost Management

- [ ] **AWS Cost Explorer**
  - [ ] Enable Cost Explorer
  - [ ] Set up budgets and alerts
  - [ ] Tag all resources for cost tracking

- [ ] **Cost Optimization**
  - [ ] Use spot instances for non-critical workloads
  - [ ] Implement auto-scaling to minimize costs
  - [ ] Schedule dev/sandbox resources to shut down after hours

---

## 9️⃣ Environment Mapping Summary

| Service/Component | Dev | Sandbox | Staging | Production |
|-------------------|-----|---------|---------|------------|
| **AWS Account** | Shared/Dev | Shared/Dev | Separate | Separate |
| **EC2 GPU** | 1x g4dn.xlarge | 1x g4dn.xlarge | 2x g5.2xlarge | 3+ g5.2xlarge (auto-scale) |
| **RDS** | db.t3.micro | db.t3.small | db.r5.large (Multi-AZ) | db.r5.2xlarge (Multi-AZ) |
| **ElastiCache** | Local/Single | cache.t3.small | cache.r5.large | cache.r5.xlarge (cluster) |
| **S3 Bucket** | dev-media | sandbox-media | staging-media | prod-media |
| **CloudFront** | Optional | Optional | Enabled | Enabled |
| **ECS/EKS** | Fargate (small) | Fargate (small) | EC2 (medium) | EC2 (auto-scale) |
| **Salesforce** | Dev Org | Dev Org | Sandbox Org | Production Org |
| **YouTube** | Test Channel | Test Channel | Test Channel | Production Channel |
| **Domain** | localhost:3000 | sandbox.aifilmstudio.com | staging.aifilmstudio.com | www.aifilmstudio.com |
| **Monitoring** | Basic | Basic | Full | Full + Enhanced |
| **Backup** | Minimal | Minimal | Daily | Hourly + Cross-region |
| **SSL/TLS** | Self-signed | Let's Encrypt | ACM | ACM |

---

## 📝 Setup Checklist by Environment

### ✅ Development Environment Setup

1. **Version Control**
   - [ ] Clone repository
   - [ ] Create dev branch
   - [ ] Install Git hooks

2. **AWS Resources**
   - [ ] Create/use dev VPC
   - [ ] Launch 1 GPU instance
   - [ ] Create S3 bucket
   - [ ] Create RDS instance (small)
   - [ ] Create SQS queue
   - [ ] Configure IAM roles

3. **Local Development**
   - [ ] Install Docker
   - [ ] Set up local Redis (or use AWS)
   - [ ] Set up local PostgreSQL (or use RDS)
   - [ ] Install Python dependencies
   - [ ] Install Node.js dependencies

4. **Configuration**
   - [ ] Create `.env.dev`
   - [ ] Store secrets in AWS Secrets Manager
   - [ ] Test database connection
   - [ ] Test Redis connection
   - [ ] Test S3 upload/download

5. **Testing**
   - [ ] Run unit tests
   - [ ] Test API endpoints locally
   - [ ] Test AI model inference
   - [ ] Test video generation pipeline

### ✅ Sandbox Environment Setup

1. **AWS Resources**
   - [ ] Use same or separate AWS account
   - [ ] Create VPC (if separate)
   - [ ] Launch 1-2 GPU instances
   - [ ] Create S3 bucket
   - [ ] Create RDS instance
   - [ ] Create ElastiCache cluster
   - [ ] Create SQS queue

2. **Deployment**
   - [ ] Build and push Docker images to ECR
   - [ ] Deploy backend to ECS/EKS
   - [ ] Deploy frontend to S3
   - [ ] Configure load balancer

3. **Configuration**
   - [ ] Create `.env.sandbox`
   - [ ] Store secrets in AWS Secrets Manager
   - [ ] Configure DNS (sandbox.aifilmstudio.com)
   - [ ] Set up SSL certificate

4. **Integration Testing**
   - [ ] Test end-to-end workflows
   - [ ] Test Salesforce integration
   - [ ] Test YouTube upload
   - [ ] Perform load testing

### ✅ Staging Environment Setup

1. **AWS Resources**
   - [ ] Create/use separate AWS account (recommended)
   - [ ] Create production-like VPC
   - [ ] Launch 2+ GPU instances
   - [ ] Create S3 bucket with encryption
   - [ ] Create RDS Multi-AZ instance
   - [ ] Create ElastiCache cluster (2+ nodes)
   - [ ] Create SQS queues
   - [ ] Set up CloudFront

2. **Deployment**
   - [ ] Build and push Docker images
   - [ ] Deploy backend with auto-scaling
   - [ ] Deploy frontend to S3 + CloudFront
   - [ ] Configure load balancer with SSL

3. **Configuration**
   - [ ] Create `.env.staging`
   - [ ] Store all secrets securely
   - [ ] Configure DNS (staging.aifilmstudio.com)
   - [ ] Set up monitoring and alarms

4. **Pre-Production Testing**
   - [ ] UAT (User Acceptance Testing)
   - [ ] Performance testing
   - [ ] Security scanning
   - [ ] Disaster recovery testing

### ✅ Production Environment Setup

1. **AWS Resources**
   - [ ] Use separate production AWS account
   - [ ] Create production VPC (Multi-AZ)
   - [ ] Launch auto-scaling GPU instances
   - [ ] Create S3 buckets (with replication)
   - [ ] Create RDS Multi-AZ with read replicas
   - [ ] Create ElastiCache cluster (3+ nodes)
   - [ ] Create SQS queues with DLQ
   - [ ] Set up CloudFront with custom domain
   - [ ] Configure WAF (Web Application Firewall)

2. **Deployment**
   - [ ] Blue-green deployment setup
   - [ ] Deploy backend with full monitoring
   - [ ] Deploy frontend with CDN
   - [ ] Configure auto-scaling policies
   - [ ] Set up health checks

3. **Configuration**
   - [ ] Create `.env.prod`
   - [ ] Store all secrets in Secrets Manager
   - [ ] Configure DNS (www.aifilmstudio.com)
   - [ ] Set up SSL/TLS with ACM
   - [ ] Configure CORS and security headers

4. **Monitoring & Backup**
   - [ ] Enable CloudWatch enhanced monitoring
   - [ ] Set up critical alarms
   - [ ] Configure SNS for alerts
   - [ ] Set up automated backups
   - [ ] Test disaster recovery plan

5. **Go-Live**
   - [ ] Perform final smoke tests
   - [ ] Enable real user monitoring
   - [ ] Monitor system performance
   - [ ] Have rollback plan ready

---

## 🔒 Security Checklist

- [ ] **Never commit secrets to Git**
  - [ ] Add `.env*` to `.gitignore`
  - [ ] Use AWS Secrets Manager for all credentials

- [ ] **Enable MFA**
  - [ ] AWS root and IAM users
  - [ ] Salesforce accounts
  - [ ] Google/YouTube accounts

- [ ] **Network Security**
  - [ ] Use VPC with private subnets
  - [ ] Configure security groups (least privilege)
  - [ ] Enable VPC flow logs

- [ ] **Data Encryption**
  - [ ] Enable encryption at rest (S3, RDS, EBS)
  - [ ] Use TLS for data in transit
  - [ ] Use AWS KMS for key management

- [ ] **Access Control**
  - [ ] Implement IAM roles (not access keys)
  - [ ] Use least privilege principle
  - [ ] Regularly rotate credentials

- [ ] **Monitoring**
  - [ ] Enable AWS CloudTrail
  - [ ] Set up security monitoring
  - [ ] Configure intrusion detection

---

## 📞 Support & Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check security group rules
   - Verify database credentials
   - Ensure VPC connectivity

2. **S3 Access Denied**
   - Check IAM role permissions
   - Verify bucket policies
   - Check CORS configuration

3. **GPU Out of Memory**
   - Use smaller batch sizes
   - Optimize model loading
   - Consider larger instance types

4. **Salesforce API Limits**
   - Monitor API usage
   - Implement caching
   - Request limit increase if needed

### Resources

- AWS Documentation: https://docs.aws.amazon.com
- Terraform Registry: https://registry.terraform.io
- Salesforce Developer Docs: https://developer.salesforce.com
- YouTube API Docs: https://developers.google.com/youtube

---

## ✅ Final Checklist

Before going live:

- [ ] All environment files configured
- [ ] All AWS resources provisioned
- [ ] All third-party integrations tested
- [ ] CI/CD pipelines working
- [ ] Monitoring and alerting configured
- [ ] Backup and disaster recovery tested
- [ ] Security audit completed
- [ ] Documentation up to date
- [ ] Team trained on operations
- [ ] Go-live runbook prepared

---

**🎉 Congratulations! Your AI Film Studio environments are now set up and ready for development, testing, and production deployment.**

For questions or issues, please refer to the main [README.md](../README.md) or open an issue in the repository.
