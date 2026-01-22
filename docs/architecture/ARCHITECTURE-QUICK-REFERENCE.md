# AI Film Studio - Architecture Quick Reference

**Version:** 1.0  
**Last Updated:** 2025-12-31

---

## 🎯 One-Page Architecture Overview

### Full Tech Stack at a Glance

| Layer | Component | Technology | Key Details |
|-------|-----------|------------|-------------|
| **🌐 Frontend** | Framework | React + Next.js 14 | SSR, fast page loads, SEO-friendly |
| | Styling | TailwindCSS + Material UI | Component library, responsive design |
| | State | Redux / Zustand | Global state management |
| | Video | Video.js / HTML5 Player | Video preview and playback |
| | Forms | React Hook Form + Dropzone | File uploads, form validation |
| | i18n | i18next | Multi-language support |
| **⚙️ Backend** | Framework | Node.js + Express / NestJS | Microservices-ready architecture |
| | API | REST + GraphQL (optional) | RESTful endpoints + GraphQL queries |
| | Database | PostgreSQL / MySQL | Relational DB, Multi-AZ |
| | Cache | Redis | Session storage, job status |
| | Storage | AWS S3 | Media files, generated content |
| | Auth | JWT + OAuth 2.0 | Google, YouTube authentication |
| | Services | Microservices | Projects, Users, Credits, YouTube, AI Jobs |
| **🤖 AI/ML** | Video Gen | SD-V, Gen-2, CogVideo, LTX-2 | AI video generation models |
| | Voice | ElevenLabs, Coqui TTS, OpenAI | Multi-age & gender voice synthesis |
| | Lip-sync | Wav2Lip, First Order Motion | Animation & synchronization |
| | Music | Jukebox, TTS, MIDI | Indian & Western music, Slokas |
| | Models | HuggingFace, RunwayML | Pre-trained model hub |
| **☁️ Cloud** | Provider | AWS | Primary cloud platform |
| | Compute | EC2 GPU (G4/G5), Lambda | NVIDIA GPUs for AI workloads |
| | Containers | Docker + ECS / Kubernetes | Orchestration & scaling |
| | IaC | Terraform | Infrastructure provisioning |
| | CDN | CloudFront | Global content delivery |
| **💾 Storage** | Metadata | PostgreSQL / MySQL | Users, projects, credits, jobs |
| | Media | AWS S3 | Images, videos, final outputs |
| | Cache | Redis | Processing queue, status cache |
| | Logs | CloudWatch / ELK Stack | Application & AI logs |
| **🔧 DevOps** | CI/CD | GitHub Actions / Jenkins | Automated deployments |
| | Containers | Docker | Multi-stage builds |
| | Orchestration | Kubernetes / ECS | Service management |
| | Monitoring | Prometheus + Grafana | Metrics & dashboards |
| | Logging | CloudWatch / ELK | Centralized logging |
| | IaC | Terraform | Infrastructure as Code |
| **🔌 Integrations** | YouTube | YouTube Data API v3 | OAuth upload, playlists |
| | CRM | Salesforce API | Customer management |
| | Payments | Stripe / PayPal | Credits & subscriptions |
| | i18n | i18next | Multi-language UI |

---

## 🏗️ System Architecture Layers

### Layer 1: Client & CDN
```
[Web Browser] → [CloudFront CDN] → [AWS WAF Security]
     ↓
[Next.js Static Site on S3]
```

### Layer 2: API & Backend Services
```
[Application Load Balancer]
     ↓
[Backend Microservices (Node.js/NestJS)]
     ├── User Service (Auth, JWT, OAuth)
     ├── Project Service (CRUD)
     ├── Credits Service (Billing)
     ├── YouTube Service (Upload)
     └── AI Jobs Service (Orchestration)
```

### Layer 3: Message Queue & Cache
```
[SQS Queue] ← Backend Services
     ↓
[Redis Cache] (Session, Status, Rate Limiting)
```

### Layer 4: AI/ML Processing
```
[GPU Workers (EC2/EKS with NVIDIA GPUs)]
     ├── Stable Diffusion Video (Video Gen)
     ├── ElevenLabs / Coqui TTS (Voice)
     ├── Wav2Lip (Lip-sync)
     ├── OpenAI Jukebox (Music)
     └── HuggingFace Models (Pre-trained)
```

### Layer 5: Data & Storage
```
[PostgreSQL/MySQL] (Metadata, Users, Projects)
[Redis] (Cache, Sessions, Queue Status)
[S3] (Images, Videos, Final Outputs)
[CloudWatch/ELK] (Logs & Metrics)
```

### Layer 6: External Integrations
```
[YouTube API v3] (Video Upload)
[Salesforce API] (CRM)
[Stripe/PayPal] (Payments)
[OpenAI API] (AI Models)
```

---

## 📊 Request Flow Summary

### Typical User Journey
1. **User Access** → CloudFront CDN → React/Next.js App
2. **API Request** → ALB → Backend Service (JWT Auth)
3. **Create Project** → PostgreSQL → SQS Queue
4. **Job Processing** → GPU Worker picks from SQS
5. **AI Generation** → Load models → Generate content
6. **Store Results** → Upload to S3 → Update PostgreSQL
7. **Notify User** → Redis cache → WebSocket/Polling
8. **Deliver Content** → CloudFront → User downloads video
9. **(Optional) YouTube** → OAuth → Upload to channel

---

## 🔒 Security Architecture

### Defense in Depth
1. **Edge**: AWS WAF, DDoS protection, Rate limiting
2. **Network**: VPC isolation, Security Groups, NACLs
3. **Application**: JWT authentication, OAuth 2.0, Input validation
4. **Data**: Encryption at rest (KMS), Encryption in transit (TLS 1.2+)
5. **Monitoring**: CloudWatch alarms, GuardDuty, AWS Config

---

## 📈 Scaling Strategy

### Auto-scaling Configuration
- **Frontend**: CloudFront global edge caching (automatic)
- **Backend**: ECS auto-scaling (CPU/Memory based, 2-50 tasks)
- **GPU Workers**: Queue-based scaling (SQS depth, 0-20 instances, 70% Spot)
- **Database**: Read replicas + vertical scaling (Multi-AZ)
- **Cache**: Redis cluster mode (horizontal scaling)

---

## 💰 Cost Estimates

### Development Environment
- **Monthly Cost**: ~$335
- **Usage**: 1-2 developers, light GPU usage (40 hrs/month)
- **Configuration**: Small instances, single AZ

### Production Environment
- **Monthly Cost**: ~$2,600
- **Usage**: 1,000+ active users, moderate GPU usage
- **Configuration**: Multi-AZ, auto-scaling, HA setup
- **Optimization**: 70% spot instances, Reserved Instances for databases

### Cost per User
- At 1,000 users: $2.60/user/month
- At 10,000 users: $1.20/user/month
- Target subscription: $15/user/month (85-91% margin)

---

## 🚀 Deployment Environments

| Environment | Purpose | Infrastructure | Scaling |
|-------------|---------|----------------|---------|
| **Dev** | Development & testing | Small instances, Single AZ | Minimal |
| **Test/QA** | Integration testing | Prod-like, scaled down | Moderate |
| **Staging** | Pre-production validation | Production mirror | Full |
| **Production** | Live user traffic | Multi-AZ, auto-scaling, HA | Full |

---

## 📦 Microservices Breakdown

### Backend Services (Node.js/NestJS)
1. **User Service**: Registration, authentication, profiles
2. **Project Service**: CRUD operations for film projects
3. **Credits Service**: Payment processing, subscription management
4. **YouTube Service**: OAuth, video upload, playlist management
5. **AI Jobs Service**: Job queue, status tracking, orchestration

---

## 🤖 AI Models Used

### Video Generation
- Stable Diffusion Video (SD-V)
- Gen-2 (RunwayML)
- CogVideo (Open source)
- LTX-2 / Dream Machine

### Voice Synthesis
- ElevenLabs (Premium, multi-language)
- Coqui TTS (Open source)
- OpenAI TTS (API-based)

### Animation & Lip-sync
- Wav2Lip (Lip synchronization)
- First Order Motion Model (Face animation)
- Custom pipelines (AI baby, podcast style)

### Music & Audio
- OpenAI Jukebox
- MIDI-based generation
- TTS for Slokas & Poems

### Model Hosting
- HuggingFace (Open source models)
- RunwayML (Fast MVP deployment)

---

## 🛠️ DevOps Pipeline

### CI/CD Flow
```
[GitHub Push]
     ↓
[GitHub Actions / Jenkins]
     ↓
[Build & Test] → [Docker Build]
     ↓
[Push to ECR]
     ↓
[Deploy to ECS/EKS]
     ↓
[Health Checks]
     ↓
[Production Live]
```

### Infrastructure Management
- **Terraform**: Provision AWS resources
- **Docker**: Containerize all services
- **Kubernetes/ECS**: Orchestrate containers
- **Prometheus + Grafana**: Monitor metrics
- **CloudWatch**: AWS native monitoring

---

## 📡 Monitoring & Observability

### Metrics Collection
- **Prometheus**: Custom metrics, time-series DB
- **CloudWatch**: AWS native metrics, alarms
- **Grafana**: Dashboards, visualizations

### Logging
- **CloudWatch Logs**: Centralized log storage
- **ELK Stack**: Elasticsearch, Logstash, Kibana
- **Structured JSON**: Consistent log format

### Alerting
- **Critical**: PagerDuty (5xx errors, RDS failures)
- **Warning**: Email (High CPU, queue depth)
- **Info**: Slack (Deployments, scaling events)

---

## 🔗 External API Integrations

### YouTube Data API v3
- OAuth 2.0 authentication
- Video upload
- Playlist management
- Thumbnail generation
- Automated publishing

### Salesforce CRM
- Customer data sync
- Lead management
- DevOps Center integration
- Analytics & reporting

### Payment Gateways
- Stripe: Primary payment processor
- PayPal: Alternative payment method
- Subscription management
- Credit purchasing
- Invoicing automation

### AI Model APIs
- OpenAI: GPT, DALL-E, TTS, Whisper
- Anthropic: Claude (optional)
- ElevenLabs: Premium voice synthesis
- Third-party model providers

---

## 🌍 Network Architecture

### VPC Configuration
```
VPC: 10.0.0.0/16
├── Public Subnets (2 AZs)
│   ├── Application Load Balancer
│   └── NAT Gateway
├── Private App Subnets (2 AZs)
│   ├── Backend ECS/EKS
│   └── GPU Workers (EC2)
└── Private Data Subnets (2 AZs)
    ├── RDS PostgreSQL (Multi-AZ)
    └── ElastiCache Redis
```

### Security Groups
- **ALB**: Port 443 (HTTPS), 80 (HTTP redirect)
- **Backend**: Port 8000 (from ALB only)
- **GPU Workers**: No inbound (pulls from SQS)
- **RDS**: Port 5432 (from Backend & Workers only)
- **Redis**: Port 6379 (from Backend only)

---

## 📖 Additional Documentation

- [Comprehensive Architecture Diagram](./comprehensive-architecture-diagram.md) - Full detailed diagrams
- [System Design Document](./system-design.md) - In-depth technical specifications
- [Requirements Documents](../requirements/) - BRD, FRD, NFR

---

## ✅ Implementation Checklist

### Phase 1: Infrastructure Setup
- [ ] Set up AWS account and VPC
- [ ] Provision RDS PostgreSQL
- [ ] Set up S3 buckets
- [ ] Configure CloudFront CDN
- [ ] Set up Redis ElastiCache
- [ ] Configure SQS queues

### Phase 2: Backend Development
- [ ] Implement User Service
- [ ] Implement Project Service
- [ ] Implement Credits Service
- [ ] Implement YouTube Service
- [ ] Implement AI Jobs Service
- [ ] Set up JWT authentication
- [ ] Integrate OAuth 2.0

### Phase 3: AI/ML Integration
- [ ] Set up GPU instances
- [ ] Deploy Stable Diffusion models
- [ ] Integrate voice synthesis (ElevenLabs/TTS)
- [ ] Implement Wav2Lip pipeline
- [ ] Add music generation
- [ ] Test all AI pipelines

### Phase 4: Frontend Development
- [ ] Set up Next.js project
- [ ] Implement UI components
- [ ] Add state management (Redux/Zustand)
- [ ] Integrate API calls
- [ ] Add video player
- [ ] Implement file upload
- [ ] Add i18n support

### Phase 5: External Integrations
- [ ] Integrate YouTube API
- [ ] Integrate Salesforce CRM
- [ ] Integrate Stripe payments
- [ ] Test OAuth flows
- [ ] Verify API limits

### Phase 6: DevOps & Deployment
- [ ] Set up GitHub Actions
- [ ] Configure Docker builds
- [ ] Deploy to ECS/Kubernetes
- [ ] Set up Terraform
- [ ] Configure monitoring (Prometheus/Grafana)
- [ ] Set up CloudWatch alarms
- [ ] Test auto-scaling

### Phase 7: Testing & QA
- [ ] Unit tests (backend)
- [ ] Integration tests
- [ ] E2E tests (frontend)
- [ ] Load testing
- [ ] Security testing
- [ ] Penetration testing
- [ ] Performance optimization

### Phase 8: Production Launch
- [ ] Deploy to production
- [ ] Monitor metrics
- [ ] Set up on-call rotation
- [ ] Document runbooks
- [ ] Train support team
- [ ] Launch marketing

---

**Status**: Blueprint Ready for Implementation  
**Maintained By**: AI-Empower-HQ-360 Architecture Team  
**Last Updated**: 2025-12-31
