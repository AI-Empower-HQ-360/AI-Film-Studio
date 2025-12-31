# 🎬 AI Film Studio — End-to-End SDLC (AWS + DevOps + Cloud + AI)

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
- [Website Pages & Functionalities](#-website-pages--functionalities)
- [SDLC Phases](#sdlc-phases)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
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

## 🌐 Website Pages & Functionalities

**AI Film Studio** provides a comprehensive web application with 10 core pages designed to deliver a seamless user experience from script input to video distribution.

### **Core Pages (Phase-1 / MVP)**

1. **🏠 Landing / Home Page** — Marketing page with hero section, key features, demo videos, pricing teaser, testimonials, and call-to-action
2. **🔐 Sign Up / Login** — User authentication with email/password and OAuth (Google, YouTube), email verification, and password reset
3. **📊 Dashboard** — Central hub for project management with grid/list views, status tracking, credits balance, notifications, and analytics
4. **➕ New Project Page** — Create AI videos with script input, character upload, voice selection, music integration, duration settings, and credit calculation
5. **🎬 Project Detail / Video Page** — View project details, track processing status, download videos, regenerate, share, and upload to YouTube
6. **💳 Credits / Pricing Page** — Display subscription plans (Free, Creator, Pro, Enterprise), credit system, payment integration, and plan management
7. **📹 YouTube / Distribution Page** *(Phase-2)* — Manage YouTube uploads, playlists, thumbnails, scheduling, and analytics
8. **⚙️ Settings / Profile Page** — Account management, security settings, connected accounts, subscription management, billing, and notifications
9. **❓ Help / Docs / Tutorials** — Comprehensive documentation, video tutorials, FAQs, troubleshooting guides, and support contact
10. **🔧 Admin Panel** *(Phase-3)* — Platform management with user management, system monitoring, content moderation, analytics, and CRM integration

### **Additional Functionalities**

- **Multi-Language UI** *(Phase-2)* — Support for 8+ languages with full localization
- **AI Voice Customization** *(Phase-3)* — Custom voice cloning and personalization
- **Team Collaboration** *(Phase-3)* — Shared workspaces and collaborative editing
- **Marketplace** *(Phase-3)* — Buy/sell voices, music, and assets
- **Mobile Apps** *(Phase-3)* — Native iOS and Android applications
- **Advanced Analytics** *(Phase-2/3)* — Revenue, engagement, and content analytics dashboards

📂 **Full Documentation**: See [`docs/WEBSITE-PAGES-FUNCTIONALITIES.md`](./docs/WEBSITE-PAGES-FUNCTIONALITIES.md) for detailed specifications of all pages, features, and technical implementation notes.

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
- **Website pages and functionalities design**

📂 See: [`docs/architecture/`](./docs/architecture/), [`docs/WEBSITE-PAGES-FUNCTIONALITIES.md`](./docs/WEBSITE-PAGES-FUNCTIONALITIES.md)

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
├── docs/                          # Documentation
│   ├── requirements/              # BRD, FRD, NFR
│   ├── architecture/              # System design, diagrams
│   ├── WEBSITE-PAGES-FUNCTIONALITIES.md  # Website pages and features documentation
│   └── operations/                # Runbooks, incident response
├── infrastructure/                # Infrastructure as Code
│   ├── terraform/                 # Terraform modules
│   │   ├── environments/          # Dev, Test, Prod configs
│   │   └── modules/               # Reusable modules
│   └── kubernetes/                # K8s manifests and Helm charts
├── backend/                       # FastAPI backend
│   ├── src/                       # Source code
│   ├── tests/                     # Unit and integration tests
│   └── Dockerfile                 # Container image
├── worker/                        # GPU worker
│   ├── src/                       # AI pipeline code
│   ├── tests/                     # Worker tests
│   └── Dockerfile                 # Container image
├── frontend/                      # Next.js frontend
│   ├── src/                       # React components
│   └── package.json               # Dependencies
├── .github/                       # GitHub Actions workflows
│   └── workflows/                 # CI/CD pipelines
└── scripts/                       # Utility scripts
```

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