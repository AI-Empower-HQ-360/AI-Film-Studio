# AI Film Studio – Visual Architecture Diagram (Ready-to-Use)

**Version:** 1.0  
**Last Updated:** December 31, 2025  
**Document Owner:** AI-Empower-HQ-360

---

## Purpose

This document provides a visual, ready-to-paste architecture diagram for presentations, documentation, and technical discussions. The diagram uses ASCII art with clear layer separation and can be easily copied into any text-based medium or used as a reference for creating visual diagrams in tools like Figma, Canva, or PowerPoint.

---

## Master Visual Diagram

```
════════════════════════════════════════════════════════════════════════════════
                        AI FILM STUDIO – SYSTEM ARCHITECTURE
════════════════════════════════════════════════════════════════════════════════

┌──────────────────────────────────────────────────────────────────────────────┐
│                           👤 USER LAYER (Blue #2196F3)                       │
├──────────────────────────────────────────────────────────────────────────────┤
│  Inputs:                                                                      │
│  • Script Text (1-5 minutes)                                                 │
│  • Images (optional reference images)                                        │
│  • Voice Preferences (age, gender, accent)                                   │
│  • Music/Slokas Selection (Indian & Western)                                 │
│  • Duration (1-5 minutes)                                                    │
│  • YouTube Credentials (OAuth 2.0)                                           │
│                                                                              │
│  Interactions:                                                               │
│  • Web Forms, Dropdowns, File Upload                                         │
│  • Multi-language Interface (EN, HI, ES, FR, etc.)                          │
│  • Real-time Progress Tracking                                              │
└──────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                       💻 FRONTEND LAYER (Light Blue #64B5F6)                 │
├──────────────────────────────────────────────────────────────────────────────┤
│  Technology Stack:                                                            │
│  • React 18 + Next.js 14 (Server-Side Rendering)                            │
│  • TypeScript 5.x (Type safety)                                             │
│  • TailwindCSS / Material UI (Responsive design)                            │
│  • Zustand / Redux (State management)                                       │
│                                                                              │
│  Features:                                                                   │
│  • Video Preview Player                                                      │
│  • Input Validation & Error Handling                                         │
│  • API Client with Retry Logic                                              │
│  • WebSocket for Real-time Updates                                          │
│  • Progressive Web App (PWA)                                                │
│                                                                              │
│  Hosting:                                                                    │
│  • AWS S3 Static Website                                                     │
│  • CloudFront CDN (Global delivery)                                          │
│  • Route53 DNS                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                   ⚙️  BACKEND / MICROSERVICES (Green #4CAF50)                │
├──────────────────────────────────────────────────────────────────────────────┤
│  Technology Stack:                                                            │
│  • Node.js 18+ / Python 3.11+                                               │
│  • NestJS / FastAPI (API frameworks)                                         │
│  • Microservices Architecture                                                │
│  • RESTful APIs + GraphQL (optional)                                         │
│                                                                              │
│  Microservices:                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │
│  │  Auth Service   │  │ Project Service │  │  Credit Service │            │
│  │  - JWT tokens   │  │ - CRUD ops      │  │ - Deduction     │            │
│  │  - OAuth2       │  │ - Status mgmt   │  │ - Balance check │            │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘            │
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │
│  │  AI Job Service │  │YouTube Service  │  │  Admin Service  │            │
│  │  - Job queue    │  │ - Upload        │  │ - Moderation    │            │
│  │  - Monitoring   │  │ - Playlists     │  │ - Analytics     │            │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘            │
│                                                                              │
│  Infrastructure:                                                             │
│  • Async Job Queue: Redis / BullMQ / AWS SQS                                │
│  • Authentication: JWT with refresh tokens                                   │
│  • Rate Limiting: Redis-based                                                │
│  • Load Balancer: AWS Application Load Balancer                             │
│  • Container Platform: ECS Fargate / EKS                                     │
└──────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│               🗄️  DATABASE / STORAGE LAYER (Yellow #FFEB3B)                  │
├──────────────────────────────────────────────────────────────────────────────┤
│  Relational Database:                                                         │
│  • PostgreSQL 15+ / MySQL 8+ (Primary)                                      │
│  • Multi-AZ Deployment (High Availability)                                   │
│  • Automated Backups (7-day retention)                                       │
│  • Read Replicas (for scaling)                                              │
│                                                                              │
│  Tables:                                                                     │
│  • users, projects, ai_jobs, credits, subscriptions, assets                 │
│                                                                              │
│  Cache Layer:                                                                │
│  • Redis 7+ / AWS ElastiCache                                               │
│  • Session storage, API response cache                                       │
│  • Job queue management                                                      │
│  • Real-time job status                                                      │
│                                                                              │
│  Object Storage:                                                             │
│  • AWS S3 (Versioned, Encrypted)                                            │
│  • Media Files: Scripts, images, videos, audio, thumbnails                  │
│  • Lifecycle Policies: Auto-archival after 90 days                          │
│  • Cross-region Replication (Disaster recovery)                             │
│                                                                              │
│  CDN:                                                                        │
│  • AWS CloudFront (225+ edge locations)                                      │
│  • Global content delivery                                                   │
│  • Cache hit ratio: >90%                                                     │
└──────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                      🤖 AI / ML LAYER (Orange #FF9800)                       │
├──────────────────────────────────────────────────────────────────────────────┤
│  Script Analysis & Story Understanding:                                       │
│  • GPT-4 / Claude 3 / LLaMA 2                                               │
│  • Scene breakdown, character extraction                                     │
│  • Mood & emotion analysis                                                   │
│  • Cultural context detection                                                │
│                                                                              │
│  Image Generation (Characters & Backgrounds):                                │
│  • Stable Diffusion XL (1024x1024)                                          │
│  • ControlNet (pose guidance)                                                │
│  • Custom LoRA models (film production)                                      │
│  • Culture-aware prompts (Indian vs Western)                                 │
│  • Resolution: Upscaled to 1920x1080                                        │
│                                                                              │
│  Voice Synthesis (Multi-Age/Gender/Mature):                                 │
│  • ElevenLabs API / Coqui TTS / Azure Speech                                │
│  • 50+ pre-built voices                                                      │
│  • Age options: Child, Young Adult, Mature, Elderly                         │
│  • Gender options: Male, Female, Non-binary                                  │
│  • Emotion control: Happy, Sad, Excited, Calm                               │
│  • Accent variations: American, British, Indian, etc.                        │
│                                                                              │
│  Lip-Sync / Facial Animation:                                               │
│  • Wav2Lip / Rhubarb Lip Sync                                               │
│  • Facial expression matching                                                │
│  • Head movement synchronization                                             │
│  • Natural eye blinks and micro-expressions                                  │
│                                                                              │
│  Music, Slokas & Poems (Indian & Western):                                  │
│  • MusicGen / AudioCraft (AI music generation)                              │
│  • Royalty-free music library (10,000+ tracks)                              │
│  • Indian classical: Ragas, devotional music                                │
│  • Western: Cinematic, ambient, orchestral                                   │
│  • Slokas & poems: Context-aware selection                                   │
│                                                                              │
│  Podcast / Dialogue Mode (Multi-Character):                                 │
│  • Two-character conversation videos                                         │
│  • Automatic turn-taking in dialogue                                         │
│  • Split-screen or alternating views                                         │
│  • Natural conversation pacing                                               │
│                                                                              │
│  Subtitle Generation (Multi-Language):                                       │
│  • Whisper AI / Google Cloud Speech-to-Text                                 │
│  • 20+ languages: EN, HI, ES, FR, DE, ZH, JA, etc.                         │
│  • Accurate timing & positioning                                             │
│  • SRT/VTT export formats                                                    │
│                                                                              │
│  Video Rendering & Composition:                                              │
│  • FFmpeg (industry-standard)                                                │
│  • MoviePy (Python library)                                                  │
│  • Resolution: 1920x1080 (1080p HD)                                         │
│  • Format: MP4 (H.264 codec)                                                │
│  • Frame rate: 24 fps (cinematic)                                           │
└──────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│              ☁️  CLOUD / INFRASTRUCTURE LAYER (Purple #9C27B0)               │
├──────────────────────────────────────────────────────────────────────────────┤
│  Compute (AI Processing & Rendering):                                        │
│  • AWS EC2 GPU Instances (g4dn.xlarge)                                      │
│    - GPU: NVIDIA T4 (16GB VRAM)                                             │
│    - vCPUs: 4, Memory: 16GB                                                  │
│    - Auto-scaling: 0-20 instances                                            │
│    - Spot instances (70% cost savings)                                       │
│                                                                              │
│  Backend Orchestration:                                                      │
│  • Amazon ECS (Elastic Container Service) with Fargate                       │
│  • Amazon EKS (Elastic Kubernetes Service)                                   │
│  • Docker containers (multi-stage builds)                                    │
│  • Auto-scaling based on CPU/Memory                                          │
│                                                                              │
│  Infrastructure as Code (IaC):                                               │
│  • Terraform 1.6+ (AWS resource provisioning)                               │
│  • AWS CDK (alternative)                                                     │
│  • Version-controlled configurations                                         │
│  • Multi-environment support (Dev, Staging, Prod)                           │
│                                                                              │
│  Database Hosting:                                                           │
│  • Amazon RDS (PostgreSQL/MySQL)                                             │
│  • Multi-AZ deployment (high availability)                                   │
│  • Automated backups & point-in-time recovery                               │
│  • Read replicas for scaling                                                 │
│                                                                              │
│  Object Storage:                                                             │
│  • AWS S3 (Simple Storage Service)                                           │
│  • Versioning, encryption (AES-256)                                          │
│  • Lifecycle policies (auto-archival)                                        │
│  • Cross-region replication (DR)                                             │
│                                                                              │
│  Content Delivery:                                                           │
│  • AWS CloudFront CDN                                                        │
│  • 225+ global edge locations                                                │
│  • Low-latency delivery (<100ms)                                            │
│  • HTTPS/TLS encryption                                                      │
│                                                                              │
│  Message Queue:                                                              │
│  • Redis / AWS SQS / RabbitMQ                                               │
│  • Job queue for AI processing                                               │
│  • Dead-letter queue for failed jobs                                         │
│                                                                              │
│  Monitoring & Logging:                                                      │
│  • AWS CloudWatch (logs, metrics, alarms)                                    │
│  • Prometheus + Grafana (advanced monitoring)                                │
│  • AWS X-Ray (distributed tracing)                                           │
│  • ELK Stack (Elasticsearch, Logstash, Kibana)                              │
│                                                                              │
│  Security:                                                                   │
│  • AWS WAF (Web Application Firewall)                                        │
│  • AWS Secrets Manager (credential storage)                                  │
│  • IAM roles & policies (least privilege)                                    │
│  • VPC with private subnets                                                  │
│  • Encryption at-rest and in-transit                                         │
│                                                                              │
│  Environments:                                                               │
│  • Dev (local + small AWS)                                                   │
│  • Sandbox (integration testing)                                             │
│  • Staging (production-like)                                                 │
│  • Production (multi-AZ, auto-scaling)                                       │
└──────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                📊 SALESFORCE CRM LAYER (Light Green #8BC34A)                 │
├──────────────────────────────────────────────────────────────────────────────┤
│  Custom Objects:                                                              │
│  • AI_Project__c: Track all video projects                                  │
│    - Fields: Name, User, Title, Script, Status, Credits, URLs, Timestamps   │
│  • AI_Credit__c: Manage user credit balances                                │
│    - Fields: User, Remaining Credits, Plan, Last Updated                    │
│  • YouTube_Integration__c: YouTube upload tracking                          │
│    - Fields: Project, Video ID, URL, Status, Playlist, Thumbnail           │
│                                                                              │
│  Automation (Flows):                                                         │
│  • Credit Deduction Flow (auto-deduct on project completion)                │
│  • Project Status Update Flow (notifications & alerts)                       │
│  • Low Credit Alert Flow (notify users)                                     │
│  • YouTube Upload Trigger Flow (auto-upload on completion)                  │
│                                                                              │
│  Business Logic (Apex):                                                      │
│  • CreditManager.cls (credit operations)                                     │
│  • ProjectTrigger.trigger (project lifecycle hooks)                          │
│  • YouTubeIntegration.cls (YouTube API wrapper)                             │
│                                                                              │
│  Dashboards & Reports:                                                      │
│  • Project Performance Dashboard                                             │
│    - Total projects by month, success rate, processing time                 │
│  • Revenue Analytics Dashboard                                               │
│    - MRR, churn rate, subscription distribution, credit utilization         │
│  • User Activity Report                                                      │
│    - Top users by project count, engagement metrics                         │
└──────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                    ▶️  YOUTUBE / OUTPUT LAYER (Red #F44336)                  │
├──────────────────────────────────────────────────────────────────────────────┤
│  YouTube Data API v3:                                                         │
│  • OAuth 2.0 authentication                                                   │
│  • Video upload (direct to user channel)                                     │
│  • Metadata: Title, description, tags, category                             │
│  • Privacy settings: Public, unlisted, private                              │
│                                                                              │
│  Playlist Creation & Management:                                             │
│  • Automatic playlist assignment                                             │
│  • Create new playlists                                                      │
│  • Playlist name & description                                               │
│                                                                              │
│  Thumbnail Generation & Upload:                                              │
│  • AI-assisted thumbnail creation (1280x720)                                │
│  • Automatic upload to YouTube                                               │
│  • Eye-catching design based on video content                               │
│                                                                              │
│  Download Option:                                                            │
│  • MP4 file download (H.264, 1080p)                                         │
│  • Subtitles download (SRT/VTT)                                              │
│  • Thumbnail download (JPG)                                                  │
│                                                                              │
│  Duration Options:                                                           │
│  • 1 minute: Social media optimized                                          │
│  • 2 minutes: YouTube Shorts extended                                        │
│  • 3 minutes: Standard short film                                            │
│  • 5 minutes: Detailed storytelling (max for MVP)                           │
│                                                                              │
│  Podcast Video Handling:                                                     │
│  • Multi-character dialogue support                                          │
│  • Split-screen or alternating views                                         │
│  • Speaker labels                                                            │
│  • Extended duration support (5-10 minutes)                                  │
└──────────────────────────────────────────────────────────────────────────────┘

════════════════════════════════════════════════════════════════════════════════
                            DATA FLOW & DEPENDENCIES
════════════════════════════════════════════════════════════════════════════════

User Input → Frontend → Backend → Database (create project record)
                         ↓
                    AI Job Queue (enqueue)
                         ↓
                    AI/ML Layer (process)
                         ↓
                    Cloud Storage (upload results)
                         ↓
                    Database (update status)
                         ↓
                    Salesforce (credit deduction, tracking)
                         ↓
                    YouTube API (upload)
                         ↓
                    User Notification (email/in-app)

════════════════════════════════════════════════════════════════════════════════
                        SUBSCRIPTION & CREDIT SYSTEM
════════════════════════════════════════════════════════════════════════════════

┌────────────────────────────────────────────────────────────────┐
│                    SUBSCRIPTION TIERS                          │
├───────────┬─────────┬──────────┬──────────────────────────────┤
│   Plan    │  Price  │ Credits  │         Features             │
├───────────┼─────────┼──────────┼──────────────────────────────┤
│   Free    │   $0    │    3     │ Watermarked, 1-min max       │
├───────────┼─────────┼──────────┼──────────────────────────────┤
│ Standard  │  $39    │   30     │ No watermark, 3-min videos   │
├───────────┼─────────┼──────────┼──────────────────────────────┤
│   Pro     │  $49    │   60     │ Priority queue, 5-min videos │
├───────────┼─────────┼──────────┼──────────────────────────────┤
│Enterprise │  $99    │   150    │ API access, custom voices    │
└───────────┴─────────┴──────────┴──────────────────────────────┘

Credit Calculation: 3 credits = 1 minute of video

════════════════════════════════════════════════════════════════════════════════
```

---

## Color Palette for Visual Design

When creating this diagram in visual tools like Figma, Canva, or PowerPoint, use these hex color codes:

| Layer | Color Name | Hex Code | RGB | Usage |
|-------|-----------|----------|-----|-------|
| **User** | Blue | `#2196F3` | (33, 150, 243) | User input, forms |
| **Frontend** | Light Blue | `#64B5F6` | (100, 181, 246) | UI components |
| **Backend** | Green | `#4CAF50` | (76, 175, 80) | API services |
| **Database** | Yellow | `#FFEB3B` | (255, 235, 59) | Storage systems |
| **AI/ML** | Orange | `#FF9800` | (255, 152, 0) | AI processing |
| **Cloud** | Purple | `#9C27B0` | (156, 39, 176) | Infrastructure |
| **Salesforce** | Light Green | `#8BC34A` | (139, 195, 74) | CRM systems |
| **YouTube** | Red | `#F44336` | (244, 67, 54) | Output delivery |

---

## Icon Set

Use these emoji or equivalent professional icons:

- 👤 **User:** Person, profile, avatar
- �� **Frontend:** Computer, browser, monitor
- ⚙️ **Backend:** Gear, settings, server
- 🗄️ **Database:** Database cylinder, storage box
- 🤖 **AI/ML:** Robot, brain, neural network
- ☁️ **Cloud:** Cloud, infrastructure
- 📊 **Salesforce:** Chart, CRM, analytics
- ▶️ **YouTube:** Play button, video, output

---

## Export Formats

This diagram can be exported as:

1. **PNG/JPG:** For presentations and documentation
2. **SVG:** For scalable web graphics
3. **PDF:** For print and high-quality sharing
4. **ASCII:** For text-based documentation (current format)

---

## Usage Guidelines

### For Presentations
- Use large, clear text (min 18pt font)
- Apply color coding consistently
- Add animations for flow (PowerPoint/Keynote)
- Include company logo and branding

### For Documentation
- Maintain ASCII version for GitHub/text files
- Create high-res PNG for wikis and portals
- Link to detailed component documentation

### For Investor Decks
- Simplify to 4-5 main layers
- Highlight key technologies (AWS, AI models)
- Show cost and scale metrics

---

**End of Visual Architecture Document**

For developer documentation, see [DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md)  
For investor presentation, see [INVESTOR_PRESENTATION.md](./INVESTOR_PRESENTATION.md)  
For infographic guidelines, see [INFOGRAPHIC_GUIDE.md](./INFOGRAPHIC_GUIDE.md)
