v# 🎬 AI Film Studio — End-to-End SDLC (AWS + DevOps + Cloud + AI)

**A production-ready case study demonstrating enterprise-grade cloud architecture, DevOps practices, and AI-powered film generation**

[![AWS](https://img.shields.io/badge/AWS-Cloud-orange?logo=amazon-aws)](https://aws.amazon.com)
[![Terraform](https://img.shields.io/badge/IaC-Terraform-623CE4?logo=terraform)](https://terraform.io)
[![Kubernetes](https://img.shields.io/badge/Orchestration-Kubernetes-326CE5?logo=kubernetes)](https://kubernetes.io)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js-000000?logo=next.js)](https://nextjs.org)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [SDLC Phases](#sdlc-phases)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Documentation](#documentation)
- [Getting Started](#getting-started)
- [Environments](#environments)
- [CI/CD Pipeline](#cicd-pipeline)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**AI Film Studio** is a cloud-native platform that transforms text scripts into cinematic short films (30-90 seconds) using AI-powered image/video generation and intelligent composition.

### **Key Features**

✅ **End-to-End Automation** — Script → Scene Graph → Shot Generation → Video Composition  
✅ **Scalable Cloud Architecture** — AWS-based infrastructure supporting 10,000+ users  
✅ **GPU-Accelerated AI** — SDXL, custom models for high-quality visual generation  
✅ **DevOps Best Practices** — IaC, CI/CD, multi-environment deployments  
✅ **Production-Ready** — Monitoring, alerting, auto-scaling, security hardening  

### **Target Users**

- Content creators and marketers
- Indie filmmakers and studios
- Educational institutions
- Corporate training departments

---

## 🏗️ Architecture

### **High-Level System Design**

```mermaid
graph TB
    User[User Browser] -->|HTTPS| CF[CloudFront CDN]
    CF --> S3F[S3 Frontend]
    User -->|API Calls| ALB[Application Load Balancer]
    ALB --> ECS[ECS/EKS Backend]
    ECS --> RDS[(RDS Postgres)]
    ECS --> SQS[SQS Job Queue]
    ECS --> S3A[S3 Assets]
    SQS --> Worker[GPU Workers]
    Worker --> S3A
    Worker --> RDS
```

### **Component Breakdown**

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Next.js on S3 + CloudFront | User interface, video preview |
| **Backend API** | FastAPI on ECS/EKS | Job orchestration, auth, credits |
| **Worker Plane** | Python + GPU EC2/EKS | AI generation, video composition |
| **Database** | RDS Postgres (Multi-AZ) | Users, projects, jobs, metadata |
| **Storage** | S3 (versioned, encrypted) | Scripts, images, videos, final MP4s |
| **Queue** | SQS | Asynchronous job processing |
| **CDN** | CloudFront | Global content delivery |

---

## 📊 SDLC Phases

This project follows a complete **Software Development Life Cycle (SDLC)** with DevOps integration:

### **1️⃣ Requirements Phase**
- Business Requirements Document (BRD)
- Functional Requirements Document (FRD)
- Non-Functional Requirements (NFR)
- Cost estimation and timeline

📂 See: [`docs/requirements/`](./docs/requirements/)

### **2️⃣ Design Phase**
- System architecture design
- Cloud service selection
- Network and security design
- Environment strategy

📂 See: [`docs/architecture/`](./docs/architecture/)

### **3️⃣ Development Phase**
- Application development (Backend, Worker, Frontend)
- Infrastructure as Code (Terraform)
- Kubernetes manifests
- Unit testing

📂 See: [`backend/`](./backend/), [`worker/`](./worker/), [`frontend/`](./frontend/), [`infrastructure/`](./infrastructure/)

### **4️⃣ Testing Phase**
- Unit, integration, and security testing
- Performance and load testing
- Resilience testing

📂 See: Test directories in each component

### **5️⃣ Deployment Phase**
- CI/CD pipelines (GitHub Actions)
- Blue-green and canary deployments
- Rollback strategies

📂 See: [`.github/workflows/`](./.github/workflows/)

### **6️⃣ Operations & Maintenance**
- Monitoring and alerting (CloudWatch)
- Incident management
- Cost optimization
- Security patching

📂 See: [`docs/operations/`](./docs/operations/)

---

## 🛠️ Technology Stack

### **Cloud & Infrastructure**
- **AWS**: VPC, EC2, ECS/EKS, RDS, S3, SQS, CloudFront, IAM
- **Terraform**: Infrastructure as Code
- **Kubernetes**: Container orchestration (EKS)
- **Docker**: Containerization

### **Backend**
- **Python 3.11+**
- **FastAPI**: High-performance API framework
- **SQLAlchemy**: ORM for database interactions
- **Alembic**: Database migrations
- **Pydantic**: Data validation
- **JWT**: Authentication

### **Worker (AI Pipeline)**
- **Stable Diffusion XL (SDXL)**: Image generation
- **Custom AI models**: Video generation
- **FFmpeg**: Video composition and encoding
- **Celery/SQS**: Task queue processing

### **Frontend**
- **Next.js 14**: React framework
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Styling
- **Axios**: API client
- **React Query**: Data fetching

### **DevOps**
- **GitHub Actions**: CI/CD
- **Docker**: Multi-stage builds
- **Amazon ECR**: Container registry
- **Terraform Cloud**: State management (optional)

### **Monitoring & Observability**
- **CloudWatch**: Logs, metrics, alarms
- **Prometheus + Grafana**: Advanced monitoring (optional)
- **X-Ray**: Distributed tracing (optional)

---

## 📁 Project Structure

```
ai-film-studio/
├── frontend/                      # React + Next.js web application
│   ├── public/                    # Static assets
│   ├── src/                       # Source code
│   │   ├── components/            # React components
│   │   ├── pages/                 # Next.js pages
│   │   ├── hooks/                 # Custom hooks
│   │   ├── services/              # API calls
│   │   └── styles/                # CSS/Tailwind
│   └── README.md
├── backend/                       # FastAPI microservices
│   ├── services/                  # Microservices
│   │   ├── user-service/          # Auth & user management
│   │   ├── project-service/       # Project CRUD
│   │   ├── credit-service/        # Billing & subscriptions
│   │   ├── ai-job-service/        # Job queue management
│   │   ├── youtube-service/       # YouTube integration
│   │   └── admin-service/         # Admin panel
│   ├── common/                    # Shared utilities
│   ├── queue/                     # Job queue definitions
│   └── README.md
├── ai/                            # AI/ML models & pipelines
│   ├── script-analysis/           # NLP & scene analysis
│   ├── image-generation/          # SDXL image generation
│   ├── voice-synthesis/           # TTS & voice cloning
│   ├── lip-sync-animation/        # Facial animation
│   ├── music-poems/               # Music & sloka generation
│   ├── subtitles/                 # Multi-language subtitles
│   └── README.md
├── cloud-infra/                   # Infrastructure as Code
│   ├── terraform/                 # Terraform configs
│   ├── k8s/                       # Kubernetes manifests
│   ├── monitoring/                # CloudWatch, Prometheus
│   └── README.md
├── salesforce/                    # Salesforce integration
│   ├── objects/                   # Custom objects
│   ├── flows/                     # Automation flows
│   ├── apex/                      # Apex classes
│   └── README.md
├── media/                         # Temporary storage
│   ├── images/                    # User uploads
│   ├── videos/                    # Generated videos
│   └── subtitles/                 # Subtitle files
├── docs/                          # Comprehensive documentation
│   ├── architecture/              # Architecture diagrams
│   │   ├── complete-visual-architecture.md  # ⭐ NEW
│   │   ├── frontend-tech-stack.md           # ⭐ NEW
│   │   ├── complete-tech-stack.md           # ⭐ NEW
│   │   ├── file-structure.md                # ⭐ NEW
│   │   └── system-design.md
│   ├── requirements/              # FRD, NFR
│   └── README.md                  # Documentation index
├── scripts/                       # Utility scripts
├── tests/                         # Integration tests
└── .github/                       # CI/CD workflows
```

📖 **[View Complete File Structure Documentation](docs/architecture/file-structure.md)**

---

## 📚 Documentation

Comprehensive documentation is available to help you understand, deploy, and maintain AI Film Studio.

### 📖 Quick Links

#### Architecture & Design
- **[Complete Visual Architecture](docs/architecture/complete-visual-architecture.md)** ⭐
  - Comprehensive diagram combining Frontend + Backend + AI + Cloud + Storage + Environments
  - All interactions and workflows visualized
  - Data flow scenarios
  
- **[Frontend Tech Stack](docs/architecture/frontend-tech-stack.md)** ⭐
  - React 18+ + Next.js 14 stack
  - TailwindCSS, Material UI, Framer Motion
  - Redux, React Query, i18next
  - Complete package.json and setup guide

- **[Complete Tech Stack](docs/architecture/complete-tech-stack.md)** ⭐
  - 100+ technologies documented
  - Frontend, Backend, AI/ML, Cloud, CI/CD
  - Version requirements and decision matrix
  
- **[File Structure Documentation](docs/architecture/file-structure.md)** ⭐
  - Complete directory tree
  - Configuration files
  - Best practices and conventions

- **[System Design](docs/architecture/system-design.md)**
  - High-level architecture
  - Component specifications
  - Network architecture
  - Security and scaling strategies
  - Cost breakdown

#### Requirements
- **[Functional Requirements (FRD)](docs/requirements/FRD.md)**
  - User roles and capabilities
  - Feature specifications
  - Acceptance criteria

- **[Non-Functional Requirements (NFR)](docs/requirements/NFR.md)**
  - Performance, scalability, security
  - Reliability and usability

#### Component Documentation
- **[Frontend README](frontend/README.md)** - React/Next.js setup and architecture
- **[Backend README](backend/README.md)** - FastAPI microservices documentation
- **[AI/ML README](ai/README.md)** - AI models and processing pipelines
- **[Cloud Infrastructure README](cloud-infra/README.md)** - Terraform and Kubernetes
- **[Salesforce README](salesforce/README.md)** - CRM integration

#### Full Documentation Index
📚 **[View Complete Documentation Index](docs/README.md)**

---

## 🚀 Getting Started

### **Prerequisites**

- AWS Account with appropriate permissions
- Terraform >= 1.5
- Docker Desktop
- Node.js >= 18
- Python >= 3.11
- kubectl (for EKS)
- GitHub account for CI/CD

### **Local Development Setup**

#### **1. Clone the repository**
```bash
git clone https://github.com/AI-Empower-HQ-360/AI-Film-Studio.git
cd AI-Film-Studio
```

#### **2. Set up backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Configure your environment variables
uvicorn src.main:app --reload
```

#### **3. Set up worker**
```bash
cd worker
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

#### **4. Set up frontend**
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

### **Infrastructure Deployment**

#### **1. Initialize Terraform**
```bash
cd infrastructure/terraform/environments/dev
terraform init
```

#### **2. Plan infrastructure**
```bash
terraform plan -out=tfplan
```

#### **3. Apply infrastructure**
```bash
terraform apply tfplan
```

---

## 🌍 Environments

| Environment | Purpose | Infrastructure |
|-------------|---------|---------------|
| **Dev** | Rapid development and testing | Small instances, single AZ |
| **Test/QA** | Integration and performance testing | Mirrors prod, scaled down |
| **Staging** | Pre-production validation | Prod-like, blue-green ready |
| **Production** | Live user traffic | Multi-AZ, auto-scaling, HA |

---

## 🔄 CI/CD Pipeline

### **Workflow Overview**

1. **Code Push** → Trigger GitHub Actions
2. **Build & Test** → Run unit and integration tests
3. **Docker Build** → Create container images → Push to ECR
4. **Deploy to Dev** → Automatic deployment
5. **Deploy to Test** → Manual approval
6. **Deploy to Prod** → Blue-green deployment with manual approval

### **Pipeline Files**
- `.github/workflows/backend-ci-cd.yml` — Backend deployment
- `.github/workflows/worker-ci-cd.yml` — Worker deployment
- `.github/workflows/frontend-ci-cd.yml` — Frontend deployment
- `.github/workflows/terraform-deploy.yml` — Infrastructure deployment

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---

## 📞 Contact

**Author**: AI-Empower-HQ-360  
**Repository**: [AI-Film-Studio](https://github.com/AI-Empower-HQ-360/AI-Film-Studio)

---

**⭐ If you find this project useful, please star the repository!**
