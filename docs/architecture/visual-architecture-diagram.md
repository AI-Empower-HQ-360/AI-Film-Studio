# Visual Architecture Diagram - AI Film Studio

**Version:** 1.0  
**Last Updated:** 2025-12-31  
**Document Owner:** AI-Empower-HQ-360

---

## 📐 Complete System Architecture

This document provides comprehensive visual diagrams showing all pages, microservices, AI models, cloud infrastructure, environments, and data flow for the AI Film Studio platform.

---

## 🏗️ Master System Architecture

```mermaid
graph TB
    subgraph "User Access Layer"
        U1[Web Users]
        U2[Mobile Users - Future]
        U3[Admin Users]
    end
    
    subgraph "CDN & Security Layer"
        CF[CloudFront CDN<br/>Global Edge Network]
        WAF[AWS WAF<br/>DDoS Protection]
        R53[Route 53<br/>DNS Management]
    end
    
    subgraph "Frontend Application Layer"
        FE[Next.js Frontend<br/>React 18 + TypeScript]
        S3FE[S3 Static Hosting<br/>Frontend Assets]
    end
    
    subgraph "API Gateway & Load Balancing"
        ALB[Application Load Balancer<br/>HTTPS Termination]
        AG[API Gateway<br/>Rate Limiting & Auth]
    end
    
    subgraph "Backend Microservices - ECS Fargate Cluster"
        direction TB
        B1[User Service<br/>Auth & Profile]
        B2[Project Service<br/>CRUD Operations]
        B3[Credit Service<br/>Payments & Subscriptions]
        B4[AI Job Service<br/>Job Orchestration]
        B5[YouTube Service<br/>Upload & Playlists]
        B6[Admin Service<br/>Management]
        B7[Analytics Service<br/>Metrics & Reports]
    end
    
    subgraph "AI Processing Layer - GPU Workers"
        direction LR
        W1[Video Generation Worker<br/>Stable Diffusion XL]
        W2[Voice Synthesis Worker<br/>ElevenLabs / TTS]
        W3[Music Generation Worker<br/>MusicGen]
        W4[Video Composition Worker<br/>FFmpeg]
        W5[Podcast Mode Worker<br/>Multi-Character]
    end
    
    subgraph "Message Queue"
        SQS[Amazon SQS<br/>Job Queue]
        DLQ[Dead Letter Queue<br/>Failed Jobs]
    end
    
    subgraph "Data Persistence Layer"
        RDS[(RDS PostgreSQL<br/>Multi-AZ + Read Replicas)]
        REDIS[(ElastiCache Redis<br/>Session & Cache)]
        S3M[(S3 Media Storage<br/>Videos, Images, Audio)]
        S3B[(S3 Backup Bucket<br/>Cross-Region)]
    end
    
    subgraph "External Service Integrations"
        STRIPE[Stripe<br/>Payment Processing]
        YT[YouTube Data API v3<br/>Video Upload]
        SFDC[Salesforce CRM<br/>Customer Management]
        ELEVEN[ElevenLabs API<br/>Voice Synthesis]
        OPENAI[OpenAI API<br/>GPT & TTS]
    end
    
    subgraph "Monitoring & Operations"
        CW[CloudWatch<br/>Logs & Metrics]
        PROM[Prometheus + Grafana<br/>Advanced Monitoring]
        PD[PagerDuty<br/>Alerting]
        SECRETS[Secrets Manager<br/>Credentials]
    end
    
    subgraph "CI/CD Pipeline"
        GH[GitHub<br/>Code Repository]
        GHA[GitHub Actions<br/>CI/CD Workflows]
        ECR[Amazon ECR<br/>Container Registry]
    end
    
    U1 --> R53
    U2 -.-> R53
    U3 --> R53
    R53 --> CF
    CF --> WAF
    WAF --> FE
    FE --> S3FE
    WAF --> ALB
    ALB --> AG
    
    AG --> B1
    AG --> B2
    AG --> B3
    AG --> B4
    AG --> B5
    AG --> B6
    AG --> B7
    
    B1 --> RDS
    B2 --> RDS
    B3 --> RDS
    B4 --> RDS
    B5 --> RDS
    B6 --> RDS
    B7 --> RDS
    
    B1 --> REDIS
    B3 --> REDIS
    B4 --> REDIS
    
    B4 --> SQS
    SQS --> DLQ
    SQS --> W1
    SQS --> W2
    SQS --> W3
    SQS --> W4
    SQS --> W5
    
    W1 --> S3M
    W2 --> S3M
    W3 --> S3M
    W4 --> S3M
    W5 --> S3M
    
    W1 --> RDS
    W2 --> RDS
    W3 --> RDS
    W4 --> RDS
    W5 --> RDS
    
    S3M --> S3B
    
    B3 --> STRIPE
    B5 --> YT
    B6 --> SFDC
    W1 --> OPENAI
    W2 --> ELEVEN
    W3 --> OPENAI
    
    B1 --> CW
    B2 --> CW
    B3 --> CW
    B4 --> CW
    B5 --> CW
    B6 --> CW
    B7 --> CW
    W1 --> CW
    W2 --> CW
    W3 --> CW
    W4 --> CW
    W5 --> CW
    
    CW --> PROM
    PROM --> PD
    
    B1 --> SECRETS
    B2 --> SECRETS
    B3 --> SECRETS
    B4 --> SECRETS
    B5 --> SECRETS
    B6 --> SECRETS
    W1 --> SECRETS
    W2 --> SECRETS
    W3 --> SECRETS
    W4 --> SECRETS
    W5 --> SECRETS
    
    GH --> GHA
    GHA --> ECR
    ECR --> B1
    ECR --> B2
    ECR --> B3
    ECR --> B4
    ECR --> B5
    ECR --> B6
    ECR --> W1
    ECR --> W2
    ECR --> W3
    ECR --> W4
    ECR --> W5
    
    style CF fill:#FF9900
    style WAF fill:#FF6B6B
    style FE fill:#4CAF50
    style ALB fill:#FF9900
    style AG fill:#2196F3
    style RDS fill:#527FFF
    style REDIS fill:#DC382D
    style S3M fill:#569A31
    style S3B fill:#569A31
    style SQS fill:#FF9900
    style W1 fill:#FF6B35
    style W2 fill:#FF6B35
    style W3 fill:#FF6B35
    style W4 fill:#FF6B35
    style W5 fill:#FF6B35
```

---

## 🎭 Frontend Pages & Components Architecture

```mermaid
graph TB
    subgraph "Public Pages"
        LP[Landing Page<br/>Hero, Features, Demo, Pricing]
        SUP[Sign Up Page<br/>Auth Form, OAuth]
        LIP[Login Page<br/>Email/Password, Social Login]
        PP[Pricing Page<br/>Plan Cards, Comparison Table]
        HP[Help Center<br/>FAQs, Tutorials, Contact]
    end
    
    subgraph "Authenticated Pages"
        DB[Dashboard<br/>Projects Overview, Quick Actions]
        PL[Projects List<br/>All Projects, Filters]
        PC[Project Create<br/>Script, Images, Voice, Music]
        PD[Project Detail<br/>Video Player, Download, YouTube]
        CR[Credits Page<br/>Balance, History, Purchase]
        YT[YouTube Page<br/>Uploads, Playlists, Settings]
        SE[Settings<br/>Profile, Billing, Security]
    end
    
    subgraph "Admin Pages"
        AD[Admin Dashboard<br/>Stats, Overview]
        AU[User Management<br/>Search, Edit, Suspend]
        AP[Project Management<br/>View All, Moderate]
        AN[Analytics<br/>Charts, Reports, Export]
        AL[Logs Viewer<br/>System Logs, Errors]
    end
    
    subgraph "Shared Components"
        NAV[Navigation Bar<br/>Logo, Menu, User Dropdown]
        FOOT[Footer<br/>Links, Social, Copyright]
        MOD[Modals<br/>Confirm, Alert, Form]
        TOAST[Toast Notifications<br/>Success, Error, Info]
        LOAD[Loading States<br/>Spinners, Skeletons]
    end
    
    LP --> SUP
    LP --> LIP
    LP --> PP
    SUP --> DB
    LIP --> DB
    
    DB --> PL
    DB --> PC
    DB --> CR
    PL --> PD
    PC --> PD
    PD --> YT
    
    DB --> SE
    DB --> HP
    
    DB -.Admin Only.-> AD
    AD --> AU
    AD --> AP
    AD --> AN
    AD --> AL
    
    LP --> NAV
    LP --> FOOT
    DB --> NAV
    DB --> FOOT
    AD --> NAV
    
    DB --> MOD
    DB --> TOAST
    DB --> LOAD
    
    style LP fill:#4CAF50
    style DB fill:#2196F3
    style AD fill:#F44336
    style NAV fill:#9E9E9E
```

---

## 🤖 AI Models & Processing Pipeline

```mermaid
graph LR
    subgraph "Input Layer"
        I1[User Script<br/>Text Input]
        I2[Character Images<br/>PNG/JPG Upload]
        I3[Voice Selection<br/>Age/Gender/Language]
        I4[Music Preference<br/>Genre/Style]
        I5[Duration<br/>1-5 Minutes]
    end
    
    subgraph "AI Processing Pipeline"
        direction TB
        
        subgraph "Step 1: Script Analysis"
            SA[Script Parser<br/>GPT-4]
            SS[Scene Segmentation<br/>NLP]
            SB[Storyboard Generator<br/>DALL-E / SD]
        end
        
        subgraph "Step 2: Visual Generation"
            IG[Image Generation<br/>Stable Diffusion XL]
            VG[Video Generation<br/>Stable Video Diffusion]
            AN[Animation<br/>First Order Motion Model]
        end
        
        subgraph "Step 3: Audio Generation"
            TTS[Voice Synthesis<br/>ElevenLabs / OpenAI TTS]
            LS[Lip Sync<br/>Wav2Lip]
            MG[Music Generation<br/>MusicGen / MIDI]
        end
        
        subgraph "Step 4: Composition"
            VC[Video Composition<br/>FFmpeg]
            AM[Audio Mixing<br/>FFmpeg]
            SG[Subtitle Generation<br/>Whisper / SRT]
        end
        
        subgraph "Step 5: Post-Processing"
            ENC[Video Encoding<br/>H.264 / H.265]
            QC[Quality Check<br/>Validation]
            THU[Thumbnail Generation<br/>Frame Extraction]
        end
    end
    
    subgraph "Output Layer"
        O1[Final MP4 Video<br/>1080p HD]
        O2[Subtitle Files<br/>SRT / VTT]
        O3[Thumbnail Image<br/>PNG]
        O4[Metadata JSON<br/>Project Details]
    end
    
    I1 --> SA
    I2 --> IG
    I3 --> TTS
    I4 --> MG
    I5 --> VC
    
    SA --> SS
    SS --> SB
    SB --> IG
    
    IG --> VG
    VG --> AN
    AN --> VC
    
    TTS --> LS
    LS --> AM
    MG --> AM
    AM --> VC
    
    VC --> ENC
    VC --> SG
    ENC --> QC
    QC --> THU
    
    QC --> O1
    SG --> O2
    THU --> O3
    SA --> O4
    
    style SA fill:#9C27B0
    style IG fill:#FF5722
    style VG fill:#FF5722
    style TTS fill:#00BCD4
    style MG fill:#4CAF50
    style VC fill:#FF9800
    style ENC fill:#3F51B5
```

---

## 🔄 End-to-End Data Flow

```mermaid
sequenceDiagram
    actor User
    participant Frontend as Frontend<br/>(Next.js)
    participant ALB as Load Balancer
    participant Auth as Auth Service
    participant Project as Project Service
    participant Credit as Credit Service
    participant Job as AI Job Service
    participant Queue as SQS Queue
    participant Worker as GPU Worker
    participant Storage as S3 Storage
    participant DB as PostgreSQL
    participant Cache as Redis
    participant YouTube as YouTube API
    
    %% Authentication Flow
    User->>Frontend: 1. Visit Platform
    Frontend->>ALB: 2. Request Page
    ALB->>Frontend: 3. Serve Static Assets
    User->>Frontend: 4. Login
    Frontend->>Auth: 5. POST /auth/login
    Auth->>DB: 6. Verify Credentials
    DB-->>Auth: 7. User Data
    Auth->>Cache: 8. Store Session
    Auth-->>Frontend: 9. JWT Token
    Frontend-->>User: 10. Redirect to Dashboard
    
    %% Project Creation Flow
    User->>Frontend: 11. Create New Project
    Frontend->>Project: 12. POST /projects
    Project->>DB: 13. INSERT Project
    DB-->>Project: 14. project_id
    Project-->>Frontend: 15. Project Created
    
    User->>Frontend: 16. Upload Character Images
    Frontend->>Storage: 17. Upload to S3 (presigned URL)
    Storage-->>Frontend: 18. Upload Success
    
    User->>Frontend: 19. Configure & Generate
    Frontend->>Job: 20. POST /jobs/generate
    Job->>Credit: 21. Check Credits
    Credit->>DB: 22. SELECT credits
    DB-->>Credit: 23. credits = 10
    Credit->>DB: 24. Deduct 3 Credits
    DB-->>Credit: 25. Updated
    Credit->>Cache: 26. Invalidate Cache
    
    Job->>DB: 27. Create Job Record
    Job->>Queue: 28. Enqueue Job Message
    Job-->>Frontend: 29. Job Queued (job_id)
    Frontend-->>User: 30. Processing Started
    
    %% AI Processing Flow
    Worker->>Queue: 31. Poll Queue
    Queue-->>Worker: 32. Job Message
    Worker->>DB: 33. Update Status: Processing
    Worker->>Storage: 34. Download Assets
    Storage-->>Worker: 35. Assets Downloaded
    
    Worker->>Worker: 36. Load AI Models
    Worker->>Worker: 37. Generate Video (3-5 min)
    Worker->>Worker: 38. Compose Audio
    Worker->>Worker: 39. Merge Video + Audio
    
    Worker->>Storage: 40. Upload Final Video
    Storage-->>Worker: 41. Video URL
    Worker->>DB: 42. Update Status: Completed
    Worker->>Queue: 43. Delete Message
    Worker->>Cache: 44. Cache Video URL
    
    %% Result Retrieval Flow
    Frontend->>Job: 45. GET /jobs/:id (polling)
    Job->>Cache: 46. Check Cache
    Cache-->>Job: 47. Job Status
    Job-->>Frontend: 48. Status: Completed + URL
    Frontend-->>User: 49. Video Ready!
    
    User->>Frontend: 50. Download Video
    Frontend->>Storage: 51. Generate Signed URL
    Storage-->>Frontend: 52. Download URL
    Frontend-->>User: 53. Download Started
    
    %% YouTube Upload Flow (Optional)
    User->>Frontend: 54. Upload to YouTube
    Frontend->>YouTube: 55. POST /youtube/upload
    YouTube->>Storage: 56. Download Video
    YouTube->>YouTube: 57. Upload to YouTube API
    YouTube->>DB: 58. Save Upload Record
    YouTube-->>Frontend: 59. Upload Success
    Frontend-->>User: 60. Published to YouTube!
    
    style User fill:#4CAF50
    style Worker fill:#FF6B35
    style Storage fill:#569A31
    style Queue fill:#FF9900
```

---

## 🌐 Multi-Environment Architecture

```mermaid
graph TB
    subgraph "Development Environment"
        DEV_CODE[Local Code<br/>VS Code / IDE]
        DEV_DB[(PostgreSQL<br/>Docker)]
        DEV_REDIS[(Redis<br/>Docker)]
        DEV_S3[S3 Dev Bucket<br/>Local Storage]
        DEV_GPU[CPU Only<br/>Small Models]
    end
    
    subgraph "Sandbox/QA Environment"
        QA_FE[Frontend<br/>S3 + CloudFront]
        QA_API[API Services<br/>ECS t3.medium]
        QA_DB[(RDS db.t3.medium<br/>Single AZ)]
        QA_REDIS[(ElastiCache<br/>cache.t3.micro)]
        QA_S3[S3 Sandbox Bucket]
        QA_GPU[1x g4dn.xlarge<br/>On-Demand]
    end
    
    subgraph "Staging Environment"
        STG_FE[Frontend<br/>S3 + CloudFront]
        STG_API[API Services<br/>ECS r6g.large]
        STG_DB[(RDS db.r6g.large<br/>Multi-AZ)]
        STG_REDIS[(ElastiCache<br/>cache.r6g.large)]
        STG_S3[S3 Staging Bucket]
        STG_GPU[2x g4dn.xlarge<br/>Spot + On-Demand]
    end
    
    subgraph "Production Environment"
        PROD_FE[Frontend<br/>S3 + CloudFront<br/>Global CDN]
        PROD_API[API Services<br/>ECS Auto-Scaling<br/>2-10 Tasks]
        PROD_DB[(RDS db.r6g.xlarge<br/>Multi-AZ + Read Replicas)]
        PROD_REDIS[(ElastiCache<br/>cache.r6g.xlarge<br/>Cluster Mode)]
        PROD_S3[S3 Production<br/>Cross-Region Replication]
        PROD_GPU[5-20x g4dn.xlarge<br/>Auto-Scaling<br/>70% Spot]
        PROD_MON[CloudWatch<br/>Prometheus<br/>PagerDuty]
    end
    
    DEV_CODE --> |Git Push| GH[GitHub Repository]
    GH --> |CI Trigger| GHA[GitHub Actions]
    
    GHA --> |Deploy| QA_FE
    GHA --> |Deploy| QA_API
    QA_API --> QA_DB
    QA_API --> QA_REDIS
    QA_API --> QA_S3
    QA_API --> QA_GPU
    
    QA_API --> |QA Approved| STG_FE
    GHA --> |Deploy| STG_API
    STG_API --> STG_DB
    STG_API --> STG_REDIS
    STG_API --> STG_S3
    STG_API --> STG_GPU
    
    STG_API --> |Production Ready| PROD_FE
    GHA --> |Deploy| PROD_API
    PROD_API --> PROD_DB
    PROD_API --> PROD_REDIS
    PROD_API --> PROD_S3
    PROD_API --> PROD_GPU
    PROD_API --> PROD_MON
    
    style DEV_CODE fill:#4CAF50
    style QA_FE fill:#FFC107
    style STG_FE fill:#FF9800
    style PROD_FE fill:#F44336
```

---

## 💳 Subscription & Payment Flow

```mermaid
graph TB
    subgraph "User Actions"
        U1[User Visits Pricing Page]
        U2[Select Plan]
        U3[Enter Payment Details]
        U4[Confirm Purchase]
    end
    
    subgraph "Payment Processing"
        FE[Frontend]
        BE[Backend Credit Service]
        STRIPE[Stripe Payment Gateway]
        WH[Webhook Handler]
    end
    
    subgraph "Credit Management"
        CR_CHECK[Check Current Credits]
        CR_ADD[Add Credits to Account]
        CR_LOG[Log Transaction]
        CR_EMAIL[Send Confirmation Email]
    end
    
    subgraph "Database Updates"
        DB_USER[(Update users.credits)]
        DB_SUB[(Update subscriptions)]
        DB_TXN[(Insert credit_transactions)]
    end
    
    subgraph "Notification Layer"
        EMAIL[SendGrid Email]
        SLACK[Slack Notification<br/>Admin Channel]
    end
    
    U1 --> U2
    U2 --> FE
    FE --> BE
    BE --> CR_CHECK
    CR_CHECK --> U3
    U3 --> STRIPE
    STRIPE --> U4
    U4 --> STRIPE
    STRIPE --> |payment_intent.succeeded| WH
    WH --> BE
    BE --> CR_ADD
    CR_ADD --> DB_USER
    CR_ADD --> DB_SUB
    BE --> CR_LOG
    CR_LOG --> DB_TXN
    BE --> CR_EMAIL
    CR_EMAIL --> EMAIL
    EMAIL --> U1
    BE --> SLACK
    
    style STRIPE fill:#6772E5
    style BE fill:#2196F3
    style DB_USER fill:#4CAF50
```

---

## 🎥 Video Generation Pipeline (Detailed)

```mermaid
graph TB
    subgraph "Input Processing"
        IN_SCRIPT[User Script<br/>Max 500 words]
        IN_IMAGES[Character Images<br/>PNG/JPG]
        IN_VOICE[Voice Selection<br/>Age, Gender, Language]
        IN_MUSIC[Music Preference<br/>Genre, Style]
        IN_DUR[Duration<br/>1-5 minutes]
    end
    
    subgraph "Stage 1: Script Processing"
        direction LR
        S1A[Parse Script<br/>GPT-4 API]
        S1B[Extract Scenes<br/>Sentence Tokenization]
        S1C[Generate Prompts<br/>Scene Descriptions]
        S1D[Timing Calculation<br/>Scene Duration]
    end
    
    subgraph "Stage 2: Visual Generation"
        direction LR
        S2A[Load SD Model<br/>SDXL]
        S2B[Generate Images<br/>1024x1024]
        S2C[Apply ControlNet<br/>Pose, Depth]
        S2D[Generate Video Clips<br/>SVD, 24fps]
    end
    
    subgraph "Stage 3: Audio Generation"
        direction LR
        S3A[Text-to-Speech<br/>ElevenLabs API]
        S3B[Audio Processing<br/>Noise Reduction]
        S3C[Background Music<br/>MusicGen]
        S3D[Mix Audio Tracks<br/>FFmpeg]
    end
    
    subgraph "Stage 4: Lip Sync"
        direction LR
        S4A[Extract Audio Features<br/>MFCC]
        S4B[Generate Mouth Movements<br/>Wav2Lip]
        S4C[Apply to Video<br/>Frame-by-frame]
    end
    
    subgraph "Stage 5: Final Composition"
        direction LR
        S5A[Merge Video Clips<br/>FFmpeg concat]
        S5B[Add Audio Track<br/>FFmpeg]
        S5C[Add Subtitles<br/>SRT Overlay]
        S5D[Encode Final Video<br/>H.264, 1080p]
    end
    
    subgraph "Stage 6: Quality & Upload"
        direction LR
        S6A[Quality Check<br/>Validation]
        S6B[Generate Thumbnail<br/>Frame at 3s]
        S6C[Upload to S3<br/>Final MP4]
        S6D[Update Database<br/>Status: Completed]
    end
    
    IN_SCRIPT --> S1A
    IN_IMAGES --> S2C
    IN_VOICE --> S3A
    IN_MUSIC --> S3C
    IN_DUR --> S1D
    
    S1A --> S1B
    S1B --> S1C
    S1C --> S1D
    S1D --> S2A
    
    S2A --> S2B
    S2B --> S2C
    S2C --> S2D
    S2D --> S4A
    
    S1B --> S3A
    S3A --> S3B
    S3B --> S3D
    S3C --> S3D
    S3D --> S4D
    
    S4A --> S4B
    S4B --> S4C
    S4C --> S5A
    S4D --> S5B
    
    S5A --> S5B
    S5B --> S5C
    S5C --> S5D
    S5D --> S6A
    
    S6A --> S6B
    S6B --> S6C
    S6C --> S6D
    
    style S1A fill:#9C27B0
    style S2A fill:#FF5722
    style S3A fill:#00BCD4
    style S4A fill:#4CAF50
    style S5A fill:#FF9800
    style S6A fill:#3F51B5
```

---

## 📊 Cost Breakdown by Environment

```mermaid
graph TB
    subgraph "Development - $300/month"
        D1[Compute: $50<br/>Local + Minimal Cloud]
        D2[Database: $80<br/>db.t3.medium]
        D3[Storage: $20<br/>S3 Dev Bucket]
        D4[GPU: $100<br/>40 hrs @ $0.526/hr]
        D5[Other: $50<br/>Networking, Misc]
    end
    
    subgraph "Sandbox/QA - $500/month"
        Q1[Compute: $120<br/>ECS Tasks]
        Q2[Database: $150<br/>RDS + ElastiCache]
        Q3[Storage: $50<br/>S3 + Transfer]
        Q4[GPU: $150<br/>1x g4dn.xlarge]
        Q5[Other: $30<br/>Monitoring]
    end
    
    subgraph "Staging - $1,500/month"
        S1[Compute: $250<br/>ECS Auto-Scaling]
        S2[Database: $400<br/>RDS Multi-AZ]
        S3[Storage: $200<br/>S3 + Transfer]
        S4[GPU: $550<br/>2x g4dn.xlarge]
        S5[Other: $100<br/>Monitoring + WAF]
    end
    
    subgraph "Production - $2,600/month"
        P1[Compute: $400<br/>ECS Auto-Scaling<br/>4-10 Tasks]
        P2[Database: $900<br/>RDS Multi-AZ + Replicas]
        P3[Storage: $300<br/>S3 + CDN + Replication]
        P4[GPU: $700<br/>5-20x g4dn.xlarge<br/>Auto-Scaling, 70% Spot]
        P5[Monitoring: $100<br/>CloudWatch + Grafana]
        P6[Security: $50<br/>WAF + GuardDuty]
        P7[Other: $150<br/>Networking, Backups]
    end
    
    style D1 fill:#4CAF50
    style Q1 fill:#FFC107
    style S1 fill:#FF9800
    style P1 fill:#F44336
```

---

## 🔐 Security Architecture Layers

```mermaid
graph TB
    subgraph "Layer 1: Network Security"
        L1A[AWS WAF<br/>DDoS Protection]
        L1B[VPC Isolation<br/>Private Subnets]
        L1C[Security Groups<br/>Firewall Rules]
        L1D[Network ACLs<br/>Subnet Level]
    end
    
    subgraph "Layer 2: Application Security"
        L2A[JWT Authentication<br/>Token Validation]
        L2B[OAuth 2.0<br/>Google, YouTube]
        L2C[API Rate Limiting<br/>Per User/IP]
        L2D[Input Validation<br/>XSS, SQL Injection]
    end
    
    subgraph "Layer 3: Data Security"
        L3A[Encryption at Rest<br/>S3 SSE-AES256]
        L3B[Encryption in Transit<br/>TLS 1.3]
        L3C[Database Encryption<br/>RDS KMS]
        L3D[Secrets Manager<br/>Credentials Storage]
    end
    
    subgraph "Layer 4: Access Control"
        L4A[IAM Roles<br/>Least Privilege]
        L4B[RBAC<br/>User Roles]
        L4C[MFA<br/>Admin Accounts]
        L4D[Audit Logs<br/>CloudTrail]
    end
    
    subgraph "Layer 5: Monitoring & Response"
        L5A[GuardDuty<br/>Threat Detection]
        L5B[CloudWatch Alarms<br/>Anomaly Detection]
        L5C[Security Hub<br/>Compliance]
        L5D[Incident Response<br/>Runbooks]
    end
    
    L1A --> L2A
    L1B --> L2B
    L1C --> L2C
    L1D --> L2D
    
    L2A --> L3A
    L2B --> L3B
    L2C --> L3C
    L2D --> L3D
    
    L3A --> L4A
    L3B --> L4B
    L3C --> L4C
    L3D --> L4D
    
    L4A --> L5A
    L4B --> L5B
    L4C --> L5C
    L4D --> L5D
    
    style L1A fill:#FF6B6B
    style L2A fill:#FF9800
    style L3A fill:#4CAF50
    style L4A fill:#2196F3
    style L5A fill:#9C27B0
```

---

## 📈 Scaling Strategy

```mermaid
graph LR
    subgraph "0-100 Users"
        U100[2 ECS Tasks<br/>1 GPU Worker<br/>db.t3.medium<br/>Cost: $500/mo]
    end
    
    subgraph "100-1,000 Users"
        U1K[4 ECS Tasks<br/>3 GPU Workers<br/>db.r6g.large<br/>Cost: $2,500/mo]
    end
    
    subgraph "1,000-5,000 Users"
        U5K[8 ECS Tasks<br/>8 GPU Workers<br/>db.r6g.xlarge<br/>Read Replicas<br/>Cost: $6,500/mo]
    end
    
    subgraph "5,000-10,000 Users"
        U10K[16 ECS Tasks<br/>15 GPU Workers<br/>db.r6g.2xlarge<br/>Multi-Region CDN<br/>Cost: $12,000/mo]
    end
    
    subgraph "10,000+ Users"
        U10KP[Auto-Scaling<br/>20+ GPU Workers<br/>db.r6g.4xlarge<br/>Global Distribution<br/>Cost: $20,000+/mo]
    end
    
    U100 -->|Growth| U1K
    U1K -->|Growth| U5K
    U5K -->|Growth| U10K
    U10K -->|Growth| U10KP
    
    style U100 fill:#4CAF50
    style U1K fill:#8BC34A
    style U5K fill:#FFC107
    style U10K fill:#FF9800
    style U10KP fill:#F44336
```

---

## 🎯 Key Takeaways

### **Architecture Principles**
1. **Scalability**: Auto-scaling at every layer
2. **Reliability**: Multi-AZ deployments, failover mechanisms
3. **Security**: Defense in depth, encryption everywhere
4. **Cost Optimization**: Spot instances, right-sizing, caching
5. **Performance**: GPU acceleration, CDN, Redis caching

### **Technology Choices**
- **Frontend**: Next.js for SSR, SEO, and performance
- **Backend**: Microservices for scalability and maintainability
- **AI**: Best-in-class models (SDXL, ElevenLabs, FFmpeg)
- **Cloud**: AWS for comprehensive services and global reach
- **Database**: PostgreSQL for reliability and ACID compliance

### **Critical Success Factors**
1. Efficient GPU worker utilization (70% spot instances)
2. Aggressive caching strategy (Redis + CloudFront)
3. Optimized AI model loading (preload, cache)
4. Robust error handling and retry logic
5. Comprehensive monitoring and alerting

---

**📊 END OF VISUAL ARCHITECTURE DOCUMENT**

This comprehensive visual reference provides a complete view of the AI Film Studio platform architecture, from user interfaces to AI processing pipelines, and from development environments to production deployments.
