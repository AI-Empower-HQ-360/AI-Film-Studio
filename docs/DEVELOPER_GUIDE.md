# AI Film Studio – Developer Documentation (Ready-to-Paste)

**Version:** 1.0  
**Last Updated:** December 31, 2025  
**Document Owner:** AI-Empower-HQ-360

---

## 1. Project Overview

**AI Film Studio** is an end-to-end AI-powered platform for creating videos from scripts, images, and music, including:

- **AI-generated voices** (multi-age, gender, mature)
- **Cultural context-aware character generation**
- **Music, Slokas, poems** (Indian & Western)
- **Multi-character podcast/video dialogues**
- **Subtitles and multi-language support**
- **Direct YouTube upload** with automatic playlists, thumbnails, and download option

### Key Objective
Enable solo creators and studios to produce high-quality AI videos quickly and efficiently.

### Target Audience
- Content creators and YouTubers
- Podcast producers
- Educational content developers
- Marketing teams
- Entertainment studios

---

## 2. Tech Stack

### Complete Technology Matrix

| Layer | Tech / Services | Functionality |
|-------|----------------|---------------|
| **User** | Browser / Mobile app | Inputs: script, images, voice, music, duration, YouTube credentials |
| **Frontend** | React, Next.js, TailwindCSS / Material UI | Video preview, input validation, multi-language interface |
| **Backend** | Node.js / NestJS, Microservices | Business logic, async jobs, credit management, authentication |
| **Database / Storage** | PostgreSQL/MySQL, Redis/ElastiCache, AWS S3 + CloudFront | Users, projects, credits, job queue, media files |
| **AI / ML** | Script analysis, Image/voice generation, lip-sync, music, subtitles | AI pipelines, animation, multi-character videos |
| **Cloud / Infrastructure** | AWS EC2 GPU, ECS / Kubernetes, Terraform, monitoring | AI rendering, backend orchestration, media storage, monitoring |
| **Salesforce CRM** | Contacts, AI_Project__c, AI_Credit__c, YouTube_Integration__c, Flows / Apex | Project tracking, credit deduction, dashboards |
| **YouTube / Output** | YouTube API | Upload, playlist creation, thumbnail generation, download |
| **Subscription / Credits** | Backend + Salesforce | Free / Standard / Pro / Enterprise; 3 credits = 1 min |

### Detailed Tech Stack by Component

#### Frontend Technologies
- **Framework:** React 18+ with Next.js 14
- **Language:** TypeScript 5.x
- **Styling:** TailwindCSS 3.x / Material UI 5.x
- **State Management:** Zustand / Redux Toolkit
- **API Client:** Axios with interceptors
- **Forms:** React Hook Form
- **Media Players:** react-player, Video.js
- **File Upload:** react-dropzone

#### Backend Technologies
- **Runtime:** Node.js 18+ / Python 3.11+
- **Framework:** NestJS / FastAPI
- **API Design:** RESTful + GraphQL (optional)
- **Authentication:** JWT (OAuth2)
- **Task Queue:** BullMQ, Redis Queue
- **Real-time:** Socket.io / WebSockets
- **Validation:** Class-validator, Pydantic

#### Database & Storage
- **Primary Database:** PostgreSQL 15+ / MySQL 8+
- **Cache:** Redis 7+ / ElastiCache
- **Message Queue:** Redis / AWS SQS / RabbitMQ
- **Object Storage:** AWS S3
- **CDN:** AWS CloudFront
- **Search:** Elasticsearch (optional)

#### AI/ML Stack
- **Text Generation:** GPT-3.5/4, Claude, LLaMA
- **Image Generation:** Stable Diffusion XL, DALL-E, Midjourney API
- **Voice Synthesis:** ElevenLabs, Coqui TTS, Azure Speech
- **Lip-sync:** Wav2Lip, Rhubarb Lip Sync
- **Music Generation:** MusicGen, AudioCraft
- **Video Processing:** FFmpeg, MoviePy
- **ML Framework:** PyTorch, TensorFlow

#### Cloud & Infrastructure
- **Cloud Provider:** AWS (Primary)
- **Compute:** EC2 (GPU: g4dn.xlarge), ECS Fargate, Lambda
- **Container Orchestration:** ECS, EKS (Kubernetes)
- **IaC:** Terraform, AWS CDK
- **CI/CD:** GitHub Actions, AWS CodePipeline
- **Monitoring:** CloudWatch, Prometheus, Grafana
- **Logging:** CloudWatch Logs, ELK Stack

---

## 3. Environment Setup

### 3.1 Development Environments

| Environment | Purpose | Infrastructure |
|-------------|---------|----------------|
| **Dev** | Local development & testing | Docker Compose, minimal AWS resources |
| **Sandbox** | Integration testing | Small AWS instances, single AZ |
| **Staging** | Pre-production validation | Production-like, scaled down |
| **Production** | Live user traffic | Multi-AZ, auto-scaling, HA |

### 3.2 Required Accounts
- AWS Account (with IAM permissions)
- Salesforce Developer Account
- YouTube API credentials (OAuth 2.0)
- GitHub Account (for CI/CD)
- OpenAI / Anthropic API keys
- ElevenLabs / Azure Speech API keys

### 3.3 Development Tools
- **Docker Desktop** (for local containers)
- **Node.js 18+** or **Python 3.11+**
- **PostgreSQL 15+** (local instance or Docker)
- **Redis 7+** (local instance or Docker)
- **Terraform 1.5+** (for infrastructure)
- **kubectl** (for Kubernetes)
- **AWS CLI** (configured with credentials)
- **Git** (version control)

### 3.4 Local Development Setup

#### Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/AI-Empower-HQ-360/AI-Film-Studio.git
cd AI-Film-Studio

# Copy environment variables
cp .env.example .env
# Edit .env with your credentials

# Start all services
docker-compose up -d

# Services will be available at:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - PostgreSQL: localhost:5432
# - Redis: localhost:6379
```

#### Manual Setup

**Backend Setup:**
```bash
cd backend
npm install  # or pip install -r requirements.txt
cp .env.example .env
npm run db:migrate  # or alembic upgrade head
npm run dev  # or uvicorn main:app --reload
```

**Frontend Setup:**
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

**Worker Setup (AI Processing):**
```bash
cd worker
pip install -r requirements.txt
cp .env.example .env
python main.py
```

---

## 4. File Structure

```
ai-film-studio/
├── frontend/                      # React/Next.js frontend application
│   ├── src/
│   │   ├── components/           # Reusable UI components
│   │   ├── pages/                # Next.js pages (routes)
│   │   ├── hooks/                # Custom React hooks
│   │   ├── utils/                # Utility functions
│   │   ├── api/                  # API client functions
│   │   └── styles/               # Global styles
│   ├── public/                   # Static assets
│   ├── package.json
│   └── next.config.js
│
├── backend/                       # Node.js/NestJS or Python/FastAPI backend
│   ├── src/
│   │   ├── modules/              # Feature modules
│   │   │   ├── auth/            # Authentication module
│   │   │   ├── projects/        # Project management
│   │   │   ├── credits/         # Credit system
│   │   │   ├── ai-jobs/         # AI job orchestration
│   │   │   └── youtube/         # YouTube integration
│   │   ├── common/              # Shared utilities
│   │   ├── database/            # Database models & migrations
│   │   └── config/              # Configuration files
│   ├── tests/
│   └── package.json (or requirements.txt)
│
├── ai/                            # AI/ML processing workers
│   ├── services/
│   │   ├── script_analyzer/     # Script analysis & storyboarding
│   │   ├── image_generator/     # AI image generation
│   │   ├── voice_synthesizer/   # Voice synthesis (multi-age/gender)
│   │   ├── lipsync/             # Lip-sync and animation
│   │   ├── music_generator/     # Music, Slokas, poems
│   │   ├── subtitle_generator/  # Multi-language subtitles
│   │   └── video_composer/      # Final video rendering
│   ├── models/                  # Pre-trained model configs
│   ├── utils/
│   └── requirements.txt
│
├── cloud-infra/                   # Infrastructure as Code
│   ├── terraform/
│   │   ├── environments/        # Dev, Staging, Prod configs
│   │   │   ├── dev/
│   │   │   ├── staging/
│   │   │   └── production/
│   │   └── modules/             # Reusable Terraform modules
│   │       ├── vpc/
│   │       ├── ecs/
│   │       ├── rds/
│   │       ├── s3/
│   │       └── sqs/
│   └── kubernetes/              # K8s manifests & Helm charts
│       ├── deployments/
│       ├── services/
│       └── ingress/
│
├── salesforce/                    # Salesforce CRM integration
│   ├── objects/                 # Custom objects (AI_Project__c, AI_Credit__c)
│   ├── flows/                   # Process automation
│   ├── apex/                    # Apex classes
│   │   ├── triggers/
│   │   └── classes/
│   ├── lwc/                     # Lightning Web Components
│   └── reports-dashboards/
│
├── media/                         # Sample media files
│   ├── scripts/                 # Sample scripts
│   ├── images/                  # Sample images
│   ├── voices/                  # Voice samples
│   └── music/                   # Music samples
│
├── scripts/                       # Utility scripts
│   ├── deploy.sh                # Deployment script
│   ├── seed-db.sh               # Database seeding
│   ├── backup.sh                # Backup script
│   └── migrate.sh               # Migration script
│
├── docs/                          # Documentation
│   ├── api/                     # API documentation
│   ├── architecture/            # Architecture diagrams
│   ├── requirements/            # FRD, NFR
│   ├── operations/              # Runbooks
│   └── DEVELOPER_GUIDE.md       # This file
│
├── tests/                         # Integration & E2E tests
│   ├── e2e/
│   ├── integration/
│   └── performance/
│
├── .github/                       # GitHub configuration
│   └── workflows/               # CI/CD pipelines
│       ├── backend-ci.yml
│       ├── frontend-ci.yml
│       ├── ai-worker-ci.yml
│       └── terraform-deploy.yml
│
├── .env.example                   # Environment variables template
├── docker-compose.yml             # Local development setup
├── README.md                      # Project overview
└── LICENSE
```

### Key Directories Explained

- **frontend/**: User-facing web application built with React/Next.js
- **backend/**: API server handling business logic, authentication, and orchestration
- **ai/**: AI processing workers for image generation, voice synthesis, video composition
- **cloud-infra/**: Infrastructure as Code (Terraform) and Kubernetes configurations
- **salesforce/**: Salesforce CRM customizations and integrations
- **scripts/**: Automation scripts for deployment, testing, and maintenance
- **docs/**: Comprehensive documentation for developers and operators

---

## 5. API Contracts (Examples)

### 5.1 Authentication APIs

#### Register User
```http
POST /api/v1/auth/register
Content-Type: application/json

Request:
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}

Response: 201 Created
{
  "userId": "uuid-12345",
  "email": "user@example.com",
  "name": "John Doe",
  "subscriptionPlan": "free",
  "credits": 3,
  "createdAt": "2025-12-31T10:00:00Z"
}
```

#### Login User
```http
POST /api/v1/auth/login
Content-Type: application/json

Request:
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}

Response: 200 OK
{
  "accessToken": "eyJhbGciOiJIUzI1NiIs...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIs...",
  "expiresIn": 3600,
  "user": {
    "userId": "uuid-12345",
    "email": "user@example.com",
    "name": "John Doe",
    "subscriptionPlan": "pro"
  }
}
```

### 5.2 Project APIs

#### Create Project
```http
POST /api/v1/projects
Authorization: Bearer <token>
Content-Type: application/json

Request:
{
  "title": "My AI Film",
  "script": "Once upon a time, in a digital world...",
  "images": ["image1.jpg", "image2.jpg"],
  "voiceType": "mature_male",
  "musicType": "cinematic",
  "duration": 3,
  "language": "en",
  "subtitles": true
}

Response: 201 Created
{
  "projectId": "proj-abc123",
  "userId": "uuid-12345",
  "title": "My AI Film",
  "status": "queued",
  "estimatedCredits": 9,
  "createdAt": "2025-12-31T10:05:00Z"
}
```

#### Get Project Details
```http
GET /api/v1/projects/{projectId}
Authorization: Bearer <token>

Response: 200 OK
{
  "projectId": "proj-abc123",
  "userId": "uuid-12345",
  "title": "My AI Film",
  "status": "completed",
  "script": "Once upon a time...",
  "duration": 3,
  "creditsUsed": 9,
  "outputVideoUrl": "https://cdn.aifilmstudio.com/videos/proj-abc123.mp4",
  "thumbnailUrl": "https://cdn.aifilmstudio.com/thumbnails/proj-abc123.jpg",
  "youtubeUrl": "https://youtube.com/watch?v=xyz",
  "createdAt": "2025-12-31T10:05:00Z",
  "completedAt": "2025-12-31T10:15:00Z"
}
```

#### List User Projects
```http
GET /api/v1/projects?page=1&limit=10&status=completed
Authorization: Bearer <token>

Response: 200 OK
{
  "projects": [
    {
      "projectId": "proj-abc123",
      "title": "My AI Film",
      "status": "completed",
      "duration": 3,
      "createdAt": "2025-12-31T10:05:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 45,
    "totalPages": 5
  }
}
```

### 5.3 AI Job APIs

#### Check AI Job Status
```http
GET /api/v1/ai-jobs/{jobId}
Authorization: Bearer <token>

Response: 200 OK
{
  "jobId": "job-xyz789",
  "projectId": "proj-abc123",
  "status": "processing",
  "progress": 65,
  "currentStep": "voice_synthesis",
  "steps": [
    { "name": "script_analysis", "status": "completed" },
    { "name": "image_generation", "status": "completed" },
    { "name": "voice_synthesis", "status": "processing" },
    { "name": "lipsync", "status": "pending" },
    { "name": "music_overlay", "status": "pending" },
    { "name": "subtitle_generation", "status": "pending" },
    { "name": "video_rendering", "status": "pending" }
  ],
  "estimatedTimeRemaining": 180,
  "startedAt": "2025-12-31T10:05:30Z"
}
```

### 5.4 Credit Management APIs

#### Get User Credits
```http
GET /api/v1/credits
Authorization: Bearer <token>

Response: 200 OK
{
  "userId": "uuid-12345",
  "remainingCredits": 21,
  "subscriptionPlan": "pro",
  "creditAllocation": 30,
  "resetDate": "2026-01-01T00:00:00Z"
}
```

#### Deduct Credits
```http
POST /api/v1/credits/deduct
Authorization: Bearer <token>
Content-Type: application/json

Request:
{
  "projectId": "proj-abc123",
  "minutes": 2,
  "credits": 6
}

Response: 200 OK
{
  "userId": "uuid-12345",
  "remainingCredits": 15,
  "deducted": 6,
  "transaction": {
    "id": "txn-999",
    "type": "deduction",
    "amount": 6,
    "reason": "Video generation (2 minutes)",
    "timestamp": "2025-12-31T10:05:00Z"
  }
}
```

### 5.5 YouTube Integration APIs

#### Upload to YouTube
```http
POST /api/v1/youtube/upload
Authorization: Bearer <token>
Content-Type: application/json

Request:
{
  "projectId": "proj-abc123",
  "title": "My Amazing AI Film",
  "description": "Created with AI Film Studio",
  "tags": ["ai", "film", "animation"],
  "category": "22",
  "privacy": "public",
  "playlistId": "PLxxxxxx",
  "youtubeCredentials": {
    "accessToken": "ya29.xxxxx",
    "channelId": "UCxxxxxx"
  }
}

Response: 202 Accepted
{
  "uploadId": "upl-456",
  "status": "uploading",
  "youtubeVideoId": null,
  "estimatedTime": 120
}
```

#### Check Upload Status
```http
GET /api/v1/youtube/upload/{uploadId}
Authorization: Bearer <token>

Response: 200 OK
{
  "uploadId": "upl-456",
  "status": "completed",
  "youtubeVideoId": "dQw4w9WgXcQ",
  "youtubeUrl": "https://youtube.com/watch?v=dQw4w9WgXcQ",
  "thumbnailUploaded": true,
  "addedToPlaylist": true,
  "completedAt": "2025-12-31T10:20:00Z"
}
```

---

## 6. Database Schema (Simplified)

### 6.1 Core Tables

#### Users Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  subscription_plan VARCHAR(50) DEFAULT 'free',
  credits INTEGER DEFAULT 3,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_login TIMESTAMP
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_subscription ON users(subscription_plan);
```

#### Projects Table
```sql
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  script TEXT NOT NULL,
  images JSONB,
  voice_type VARCHAR(50),
  music_type VARCHAR(50),
  duration INTEGER NOT NULL,
  language VARCHAR(10) DEFAULT 'en',
  subtitles BOOLEAN DEFAULT false,
  status VARCHAR(50) DEFAULT 'queued',
  credits_used INTEGER,
  output_video_url TEXT,
  thumbnail_url TEXT,
  youtube_url TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMP
);

-- Indexes
CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_created_at ON projects(created_at DESC);
```

#### Credits Table
```sql
CREATE TABLE credits (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  remaining_credits INTEGER NOT NULL,
  last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_credits_user_id ON credits(user_id);
```

#### AI Jobs Table
```sql
CREATE TABLE ai_jobs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  status VARCHAR(50) DEFAULT 'pending',
  progress INTEGER DEFAULT 0,
  current_step VARCHAR(100),
  output_video_url TEXT,
  logs JSONB,
  error_message TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  started_at TIMESTAMP,
  completed_at TIMESTAMP
);

-- Indexes
CREATE INDEX idx_ai_jobs_project_id ON ai_jobs(project_id);
CREATE INDEX idx_ai_jobs_status ON ai_jobs(status);
```

#### Subscriptions Table
```sql
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  plan VARCHAR(50) NOT NULL,
  status VARCHAR(50) DEFAULT 'active',
  credits_per_month INTEGER,
  price DECIMAL(10, 2),
  stripe_subscription_id VARCHAR(255),
  current_period_start TIMESTAMP,
  current_period_end TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  canceled_at TIMESTAMP
);

-- Indexes
CREATE INDEX idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);
```

### 6.2 Relationships

```
users (1) ─────┬───── (many) projects
               │
               └───── (many) subscriptions

projects (1) ────── (many) ai_jobs

users (1) ────────── (1) credits
```

---

## 7. AI Pipelines

### 7.1 Complete Video Generation Pipeline

```
Input Script → [Pipeline Stages] → Output Video + YouTube Upload
```

#### Stage 1: Script Analysis
- **Purpose:** Analyze script for scenes, characters, emotions, cultural context
- **Tools:** GPT-4, Claude, LLaMA
- **Output:** Scene breakdown, character descriptions, mood indicators
- **Time:** ~10-20 seconds

#### Stage 2: Image Generation
- **Purpose:** Generate characters and backgrounds based on script analysis
- **Tools:** Stable Diffusion XL, ControlNet, LoRA models
- **Cultural Awareness:** Adjust prompts based on cultural context (Indian vs Western)
- **Output:** High-res images for each scene
- **Time:** ~30-60 seconds per image

#### Stage 3: Voice Synthesis
- **Purpose:** Generate voiceover with appropriate age, gender, accent
- **Tools:** ElevenLabs, Coqui TTS, Azure Speech
- **Options:** Young male/female, mature male/female, child, elderly
- **Output:** Audio file (WAV/MP3)
- **Time:** ~20-40 seconds

#### Stage 4: Lip-sync & Animation
- **Purpose:** Synchronize facial movements with audio
- **Tools:** Wav2Lip, Rhubarb Lip Sync, Synthesia
- **Output:** Animated character video clips
- **Time:** ~60-120 seconds

#### Stage 5: Music & Sound Effects
- **Purpose:** Add background music, Slokas (Indian), poems
- **Tools:** MusicGen, AudioCraft, royalty-free libraries
- **Options:** Cinematic, ambient, classical, Indian classical
- **Output:** Background audio track
- **Time:** ~30 seconds

#### Stage 6: Podcast Mode (Optional)
- **Purpose:** Create multi-character dialogue videos
- **Tools:** Multiple voice synthesis + lip-sync
- **Output:** Two-character conversation video
- **Time:** ~2x standard pipeline

#### Stage 7: Subtitle Generation
- **Purpose:** Generate multi-language subtitles
- **Tools:** Whisper, Google Cloud Speech-to-Text
- **Languages:** English, Hindi, Spanish, French, etc.
- **Output:** SRT/VTT subtitle file
- **Time:** ~15-30 seconds

#### Stage 8: Video Rendering
- **Purpose:** Compose final video with all elements
- **Tools:** FFmpeg, MoviePy
- **Resolution:** 1080p (1920x1080)
- **Format:** MP4 (H.264)
- **Output:** Final rendered video
- **Time:** ~60-90 seconds

#### Stage 9: Thumbnail Generation
- **Purpose:** Create eye-catching thumbnail for YouTube
- **Tools:** AI-assisted thumbnail generation
- **Output:** JPG thumbnail (1280x720)
- **Time:** ~10 seconds

#### Stage 10: YouTube Upload
- **Purpose:** Upload video to YouTube with metadata
- **Tools:** YouTube Data API v3
- **Features:** Playlist creation, thumbnail upload, description, tags
- **Time:** ~60-180 seconds (depending on video size)

### 7.2 Processing Time Estimates

| Video Duration | Processing Time | Credits Required |
|----------------|-----------------|------------------|
| 1 minute | 5-8 minutes | 3 credits |
| 2 minutes | 10-15 minutes | 6 credits |
| 3 minutes | 15-22 minutes | 9 credits |
| 5 minutes | 25-35 minutes | 15 credits |

---

## 8. Salesforce CRM Integration

### 8.1 Custom Objects

#### AI_Project__c
```
Fields:
- Name (Auto-number): AIPROJ-{0000}
- User_Email__c (Email)
- Project_Title__c (Text)
- Script__c (Long Text Area)
- Duration__c (Number)
- Status__c (Picklist: Queued, Processing, Completed, Failed)
- Credits_Used__c (Number)
- Output_Video_URL__c (URL)
- YouTube_URL__c (URL)
- Created_Date__c (Date/Time)
- Completed_Date__c (Date/Time)

Relationships:
- Lookup to Contact (User)
```

#### AI_Credit__c
```
Fields:
- Name (Auto-number): AICREDIT-{0000}
- User_Email__c (Email)
- Remaining_Credits__c (Number)
- Subscription_Plan__c (Picklist: Free, Standard, Pro, Enterprise)
- Last_Updated__c (Date/Time)

Relationships:
- Lookup to Contact (User)
```

#### YouTube_Integration__c
```
Fields:
- Name (Auto-number): YTINT-{0000}
- Project__c (Lookup to AI_Project__c)
- Video_Title__c (Text)
- YouTube_Video_ID__c (Text)
- YouTube_URL__c (URL)
- Upload_Status__c (Picklist: Pending, Uploading, Completed, Failed)
- Playlist_ID__c (Text)
- Thumbnail_Uploaded__c (Checkbox)
- Upload_Date__c (Date/Time)

Relationships:
- Lookup to AI_Project__c
```

### 8.2 Flows & Automations

#### Credit Deduction Flow
```
Trigger: When AI_Project__c status changes to "Completed"
Actions:
1. Get related AI_Credit__c record
2. Deduct credits based on duration (Duration__c * 3)
3. Update Remaining_Credits__c
4. If Remaining_Credits__c < 0, send low credit alert
5. Update Last_Updated__c timestamp
```

#### Project Status Update Flow
```
Trigger: When AI_Project__c status changes
Actions:
1. Send email notification to user
2. Update dashboard metrics
3. If status = "Failed", create case for support
4. If status = "Completed", trigger YouTube upload flow
```

### 8.3 Apex Classes

#### CreditManager.cls
```apex
public class CreditManager {
    public static void deductCredits(Id userId, Integer minutes) {
        Integer creditsToDeduct = minutes * 3;
        AI_Credit__c creditRecord = [
            SELECT Remaining_Credits__c 
            FROM AI_Credit__c 
            WHERE User_Email__c = :userId 
            LIMIT 1
        ];
        
        creditRecord.Remaining_Credits__c -= creditsToDeduct;
        creditRecord.Last_Updated__c = System.now();
        update creditRecord;
    }
    
    public static Boolean hasEnoughCredits(Id userId, Integer minutes) {
        Integer creditsRequired = minutes * 3;
        AI_Credit__c creditRecord = [
            SELECT Remaining_Credits__c 
            FROM AI_Credit__c 
            WHERE User_Email__c = :userId 
            LIMIT 1
        ];
        return creditRecord.Remaining_Credits__c >= creditsRequired;
    }
}
```

### 8.4 Dashboards & Reports

#### Project Performance Dashboard
- Total projects created (by month)
- Success rate (Completed vs Failed)
- Average processing time
- Credits consumed by tier
- Top users by project count

#### Revenue Dashboard
- Active subscriptions by tier
- Monthly recurring revenue (MRR)
- Churn rate
- Credit utilization rate
- Conversion from Free to Paid

---

## 9. YouTube Integration

### 9.1 Authentication

**OAuth 2.0 Flow:**
```javascript
// Step 1: User authorizes app
const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?
  client_id=${CLIENT_ID}&
  redirect_uri=${REDIRECT_URI}&
  scope=https://www.googleapis.com/auth/youtube.upload&
  response_type=code&
  access_type=offline`;

// Step 2: Exchange code for tokens
const tokens = await axios.post('https://oauth2.googleapis.com/token', {
  code: authCode,
  client_id: CLIENT_ID,
  client_secret: CLIENT_SECRET,
  redirect_uri: REDIRECT_URI,
  grant_type: 'authorization_code'
});
```

### 9.2 Video Upload

```javascript
const uploadVideo = async (videoPath, metadata, accessToken) => {
  const youtube = google.youtube('v3');
  
  const response = await youtube.videos.insert({
    auth: oauth2Client,
    part: 'snippet,status',
    requestBody: {
      snippet: {
        title: metadata.title,
        description: metadata.description,
        tags: metadata.tags,
        categoryId: metadata.categoryId
      },
      status: {
        privacyStatus: metadata.privacy || 'public'
      }
    },
    media: {
      body: fs.createReadStream(videoPath)
    }
  });
  
  return response.data.id; // YouTube video ID
};
```

### 9.3 Playlist Creation

```javascript
const createPlaylist = async (title, description, accessToken) => {
  const youtube = google.youtube('v3');
  
  const response = await youtube.playlists.insert({
    auth: oauth2Client,
    part: 'snippet,status',
    requestBody: {
      snippet: {
        title: title,
        description: description
      },
      status: {
        privacyStatus: 'public'
      }
    }
  });
  
  return response.data.id; // Playlist ID
};
```

### 9.4 Thumbnail Upload

```javascript
const uploadThumbnail = async (videoId, thumbnailPath, accessToken) => {
  const youtube = google.youtube('v3');
  
  await youtube.thumbnails.set({
    auth: oauth2Client,
    videoId: videoId,
    media: {
      body: fs.createReadStream(thumbnailPath)
    }
  });
};
```

### 9.5 Duration Options

- **1 minute:** Fastest processing, ideal for social media
- **2 minutes:** Balanced content for YouTube Shorts extended
- **3 minutes:** Standard short film format
- **5 minutes:** Detailed storytelling (max for MVP)

### 9.6 Podcast Video Handling

For podcast-style videos with two characters:
- Generate two separate character animations
- Synchronize dialogue timing
- Add split-screen or alternating view
- Include names/labels for speakers
- Support longer durations (5-10 minutes)

---

## 10. Subscription & Credit System

### 10.1 Subscription Tiers

| Plan | Price/Month | Credits/Month | Features |
|------|-------------|---------------|----------|
| **Free** | $0 | 3 | Basic features, watermarked videos, 1-min max |
| **Standard** | $39 | 30 | No watermark, 3-min videos, standard queue |
| **Pro** | $49 | 60 | Priority queue, 5-min videos, advanced AI models |
| **Enterprise** | $99 | 150 | Unlimited*, custom voices, API access, white-label |

*Unlimited with fair use policy

### 10.2 Credit Calculation

**Base Rule:** 3 credits = 1 minute of video

**Additional Credit Costs:**
- Standard video: 3 credits/minute
- HD video (1080p): +1 credit/minute
- Podcast mode (2 characters): +2 credits/minute
- Multi-language subtitles: +1 credit
- Custom voice cloning: +5 credits (one-time)
- Premium music: +2 credits
- Rush processing (priority queue): +50% credits

**Examples:**
- 1-min standard video: 3 credits
- 2-min HD video: 8 credits (2*3 + 2*1)
- 3-min podcast: 15 credits (3*3 + 3*2)

### 10.3 Credit Management

**Credit Deduction:**
- Credits deducted when video generation starts
- If generation fails, credits refunded automatically
- Partial completion: proportional refund

**Credit Expiry:**
- Monthly credits expire at end of billing cycle
- No rollover for Free and Standard plans
- Pro and Enterprise: rollover up to 2x monthly allocation

**Credit Purchase:**
- Additional credits available: $1 per credit
- Bulk discounts: 50 credits for $40, 100 credits for $70

---

## 11. MVP / Roadmap

### 11.1 MVP (Phase 1) - Completed

**Core Features:**
- ✅ User authentication (email/password, OAuth)
- ✅ Script input and analysis
- ✅ Basic image generation (Stable Diffusion)
- ✅ Voice synthesis (single voice type)
- ✅ Simple video composition
- ✅ Download video
- ✅ YouTube upload (basic)
- ✅ Credit system (3 credits = 1 min)
- ✅ Free tier (3 credits/month)

**Tech Stack:**
- ✅ Frontend: React + Next.js
- ✅ Backend: FastAPI
- ✅ Database: PostgreSQL
- ✅ Storage: AWS S3
- ✅ AI: Stable Diffusion + ElevenLabs

### 11.2 Phase 2 - In Progress

**Advanced Features:**
- 🔄 Multi-age/gender voice synthesis
- 🔄 Podcast mode (two-character dialogues)
- 🔄 Multi-language subtitle generation
- 🔄 Automatic thumbnail generation
- 🔄 YouTube playlist management
- 🔄 Advanced AI models (SDXL, AnimateDiff)
- 🔄 Music and Slokas overlay
- 🔄 Cultural context awareness (Indian/Western)
- 🔄 Subscription tiers (Standard, Pro, Enterprise)

**Enhancements:**
- 🔄 Real-time progress tracking (WebSockets)
- 🔄 Video preview before final render
- 🔄 Batch processing
- 🔄 Mobile responsive UI

### 11.3 Phase 3 - Planned

**Full Automation:**
- 📋 AI-powered script generation
- 📋 Automatic scene transitions
- 📋 Advanced lip-sync and facial expressions
- 📋 3D character models
- 📋 Voice cloning (custom voices)
- 📋 Advanced music generation (custom compositions)
- 📋 Multi-video project management
- 📋 Collaborative editing

**Platform Features:**
- 📋 Mobile app (iOS/Android)
- 📋 API access for developers
- 📋 White-label solution for enterprises
- 📋 Marketplace for templates and assets
- 📋 Social sharing and embedding
- 📋 Analytics and insights

**Salesforce Integration:**
- 📋 Advanced dashboards
- 📋 Automated marketing campaigns
- 📋 Customer success workflows
- 📋 Predictive analytics

### 11.4 Timeline

| Phase | Duration | Completion Date |
|-------|----------|-----------------|
| MVP (Phase 1) | 3 months | ✅ Completed |
| Phase 2 | 4 months | Q2 2026 (estimated) |
| Phase 3 | 6 months | Q4 2026 (estimated) |

---

## 12. Getting Help

### 12.1 Documentation Resources

- **API Documentation:** `/docs/api/`
- **Architecture Diagrams:** `/docs/architecture/`
- **Runbooks:** `/docs/operations/`
- **Video Tutorials:** (Coming soon)

### 12.2 Support Channels

- **GitHub Issues:** [Report bugs or request features](https://github.com/AI-Empower-HQ-360/AI-Film-Studio/issues)
- **Developer Forum:** (Coming soon)
- **Email:** support@aifilmstudio.com
- **Discord:** (Coming soon)

### 12.3 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

## 13. Appendix

### 13.1 Glossary

- **Credit:** Unit of currency in the platform (3 credits = 1 minute of video)
- **AI Job:** Asynchronous task for AI processing
- **Podcast Mode:** Two-character dialogue video
- **Sloka:** Indian devotional verse/poem
- **Lip-sync:** Synchronization of lip movements with audio
- **LoRA:** Low-Rank Adaptation (fine-tuned AI model)

### 13.2 Quick Commands

```bash
# Start development environment
docker-compose up -d

# Run migrations
npm run db:migrate  # or alembic upgrade head

# Run tests
npm test  # or pytest

# Build for production
npm run build  # or docker build

# Deploy to staging
./scripts/deploy.sh staging

# View logs
docker-compose logs -f backend
```

---

**End of Developer Documentation**

For investor presentation content, see [INVESTOR_PRESENTATION.md](./INVESTOR_PRESENTATION.md)
