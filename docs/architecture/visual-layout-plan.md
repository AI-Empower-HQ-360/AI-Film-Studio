# AI FILM STUDIO – COLOR-CODED VISUAL LAYOUT PLAN

**Version:** 1.0  
**Last Updated:** 2025-12-31  
**Document Owner:** AI-Empower-HQ-360  
**Purpose:** Comprehensive visual architecture guide for Figma, Canva, or Lucidchart implementation

---

## Table of Contents

1. [Color Scheme for Layers](#color-scheme-for-layers)
2. [Layered Architecture Overview](#layered-architecture-overview)
3. [Layer Specifications](#layer-specifications)
4. [Flow Arrows & Dependencies](#flow-arrows--dependencies)
5. [Icon Suggestions](#icon-suggestions)
6. [Mermaid Diagrams](#mermaid-diagrams)
7. [Implementation Guidelines](#implementation-guidelines)

---

## Color Scheme for Layers

The AI Film Studio architecture is organized into 8 distinct layers, each with a specific color for visual clarity:

| Layer | Color | Hex Code | Usage |
|-------|-------|----------|-------|
| **User Layer** | Blue | `#0066CC` | User inputs, interactions, forms |
| **Frontend** | Light Blue | `#66B3FF` | React/Next.js, UI components |
| **Backend / Microservices** | Green | `#28A745` | Node.js/NestJS, API services |
| **Database / Storage** | Yellow | `#FFC107` | PostgreSQL, Redis, S3 |
| **AI / ML Layer** | Orange | `#FF8C00` | AI models, generation engines |
| **Cloud / Infrastructure** | Purple | `#8B5CF6` | AWS services, deployment |
| **Salesforce CRM** | Light Green | `#90EE90` | CRM integration, data sync |
| **YouTube / Output** | Red | `#DC3545` | Video upload, delivery |

---

## Layered Architecture Overview

```mermaid
graph TB
    subgraph User["👤 USER LAYER (Blue #0066CC)"]
        U1[Script Input]
        U2[Images Upload]
        U3[Voice Selection]
        U4[Music/Slokas]
        U5[Duration Selection]
        U6[YouTube Credentials]
    end
    
    subgraph Frontend["💻 FRONTEND LAYER (Light Blue #66B3FF)"]
        F1[React + Next.js]
        F2[TailwindCSS / Material UI]
        F3[Video Preview]
        F4[Input Validation]
        F5[Multi-language Support]
    end
    
    subgraph Backend["⚙️ BACKEND LAYER (Green #28A745)"]
        B1[User Service]
        B2[Project Service]
        B3[Credit Service]
        B4[AI Job Service]
        B5[YouTube Service]
        B6[Admin Service]
        B7[Redis / BullMQ / SQS]
        B8[JWT / OAuth 2.0]
    end
    
    subgraph Database["🗄️ DATABASE LAYER (Yellow #FFC107)"]
        D1[PostgreSQL / MySQL]
        D2[Redis / ElastiCache]
        D3[S3 + CloudFront]
        D4[User Data]
        D5[Project Data]
        D6[Credit Data]
    end
    
    subgraph AI["🤖 AI/ML LAYER (Orange #FF8C00)"]
        A1[Script Analysis]
        A2[Image Generation]
        A3[Voice Synthesis]
        A4[Lip-sync / Animation]
        A5[Music / Slokas]
        A6[Podcast Mode]
        A7[Subtitles]
    end
    
    subgraph Cloud["☁️ CLOUD LAYER (Purple #8B5CF6)"]
        C1[AWS EC2 GPU]
        C2[ECS / Kubernetes]
        C3[Terraform]
        C4[RDS]
        C5[S3 + CloudFront]
        C6[Redis / ElastiCache]
        C7[CloudWatch / Grafana]
        C8[Environments]
    end
    
    subgraph Salesforce["📊 SALESFORCE CRM (Light Green #90EE90)"]
        S1[Contacts → Users]
        S2[AI_Project__c]
        S3[AI_Credit__c]
        S4[YouTube_Integration__c]
        S5[Flows / Apex]
        S6[Dashboards]
    end
    
    subgraph YouTube["▶️ YOUTUBE OUTPUT (Red #DC3545)"]
        Y1[Video Upload]
        Y2[Playlist Creation]
        Y3[Thumbnail Generation]
        Y4[Download Option]
        Y5[Duration: 1-5 min]
    end
    
    User --> Frontend
    Frontend --> Backend
    Backend --> Database
    Backend --> AI
    AI --> Database
    AI --> Cloud
    Cloud --> Database
    Backend --> Salesforce
    Salesforce --> Frontend
    Backend --> YouTube
    AI --> YouTube
    
    style User fill:#0066CC,color:#fff
    style Frontend fill:#66B3FF,color:#000
    style Backend fill:#28A745,color:#fff
    style Database fill:#FFC107,color:#000
    style AI fill:#FF8C00,color:#fff
    style Cloud fill:#8B5CF6,color:#fff
    style Salesforce fill:#90EE90,color:#000
    style YouTube fill:#DC3545,color:#fff
```

---

## Layer Specifications

### 1. 👤 USER LAYER (Blue #0066CC)

**Purpose:** Entry point for all user interactions and input collection

#### Components:

##### 1.1 Script Input
- **Type:** Text area / Rich text editor
- **Validation:** 
  - Min: 50 words
  - Max: 500 words
  - Language detection
- **Features:** 
  - Auto-save
  - Spell check
  - Template library

##### 1.2 Images Upload
- **Type:** Drag & drop file uploader
- **Supported Formats:** JPG, PNG, WebP
- **Limits:** 
  - Max file size: 10MB per image
  - Max images: 20 per project
- **Features:** 
  - Preview thumbnails
  - Batch upload
  - AI image suggestions

##### 1.3 Voice Selection
- **Type:** Dropdown with audio preview
- **Options:**
  - Age: Child, Teen, Adult, Senior
  - Gender: Male, Female, Neutral
  - Tone: Professional, Friendly, Dramatic
  - Accent: Multiple regional options
- **Features:** 
  - Voice sample playback
  - Custom voice upload (Pro feature)

##### 1.4 Music/Slokas Selection
- **Type:** Multi-select dropdown with categories
- **Categories:**
  - Indian Classical
  - Western Classical
  - Contemporary
  - Slokas/Mantras
  - Poems
  - Ambient
- **Features:** 
  - Preview clips
  - Volume control
  - Custom music upload

##### 1.5 Duration Selection
- **Type:** Slider with presets
- **Range:** 1-5 minutes
- **Presets:** 
  - Short (1 min)
  - Medium (2-3 min)
  - Long (4-5 min)
- **Dynamic:** Adjusts based on script length

##### 1.6 YouTube Credentials
- **Type:** OAuth 2.0 connection
- **Features:**
  - One-click authorization
  - Channel selection
  - Privacy settings
  - Auto-upload toggle

#### User Interactions:
- Forms with progressive disclosure
- Real-time validation
- Multi-step wizard
- Multi-language support (15+ languages)
- Accessibility compliance (WCAG 2.1 AA)

---

### 2. 💻 FRONTEND LAYER (Light Blue #66B3FF)

**Purpose:** User interface and client-side application logic

#### Technology Stack:

##### 2.1 React + Next.js 14+
- **Features:**
  - Server-Side Rendering (SSR)
  - Static Site Generation (SSG)
  - API Routes
  - Image optimization
  - Code splitting
- **Structure:**
  ```
  frontend/
  ├── src/
  │   ├── app/            # Next.js 14+ App Router pages
  │   ├── components/     # Reusable UI components
  │   ├── hooks/          # Custom React hooks
  │   ├── context/        # State management
  │   ├── services/       # API services
  │   └── utils/          # Helper functions
  ```

##### 2.2 TailwindCSS / Material UI
- **Styling Approach:**
  - Tailwind for utility-first styling
  - Material UI for complex components
  - Custom theme configuration
  - Dark mode support
- **Design System:**
  - Typography scale
  - Color palette (matching layer colors)
  - Spacing system
  - Component library

##### 2.3 Video Preview
- **Player:** react-player or custom player
- **Features:**
  - Playback controls
  - Timeline scrubbing
  - Frame-by-frame navigation
  - Quality selection
  - Fullscreen mode
  - Picture-in-picture

##### 2.4 Input Validation
- **Client-Side Validation:**
  - Real-time field validation
  - Form-level validation
  - Error messages
  - Success indicators
- **Libraries:**
  - React Hook Form
  - Yup / Zod for schemas

##### 2.5 API Integration
- **HTTP Client:** Axios with interceptors
- **State Management:** React Query / TanStack Query
- **Features:**
  - Request/response interceptors
  - Automatic retries
  - Cache management
  - Optimistic updates
  - WebSocket for real-time updates

#### UI Components:
```typescript
// Key component interfaces
interface ProjectDashboard {
  projectList: ProjectCard[]
  filters: FilterPanel
  pagination: Pagination
  createButton: ActionButton
}

interface VideoEditor {
  preview: VideoPlayer
  timeline: Timeline
  controls: ControlPanel
  export: ExportSettings
}

interface CreditDisplay {
  balance: number
  usage: UsageChart
  purchaseButton: ActionButton
}
```

---

### 3. ⚙️ BACKEND / MICROSERVICES LAYER (Green #28A745)

**Purpose:** Business logic, API endpoints, and service orchestration

#### Technology Stack:

##### 3.1 Node.js / NestJS
- **Framework:** NestJS (TypeScript)
- **Architecture:** Microservices with message brokers
- **Features:**
  - Dependency injection
  - Modular architecture
  - Decorator-based routing
  - Built-in validation

##### 3.2 Microservices Architecture

###### User Service
- **Endpoints:**
  ```
  POST   /api/v1/auth/register
  POST   /api/v1/auth/login
  POST   /api/v1/auth/refresh
  GET    /api/v1/users/me
  PATCH  /api/v1/users/me
  DELETE /api/v1/users/me
  ```
- **Responsibilities:**
  - User registration/authentication
  - Profile management
  - Session handling
  - Password reset

###### Project Service
- **Endpoints:**
  ```
  GET    /api/v1/projects
  POST   /api/v1/projects
  GET    /api/v1/projects/:id
  PATCH  /api/v1/projects/:id
  DELETE /api/v1/projects/:id
  ```
- **Responsibilities:**
  - Project CRUD operations
  - Asset management
  - Version control
  - Collaboration features

###### Credit Service
- **Endpoints:**
  ```
  GET    /api/v1/credits/balance
  POST   /api/v1/credits/deduct
  POST   /api/v1/credits/purchase
  GET    /api/v1/credits/history
  ```
- **Responsibilities:**
  - Credit balance management
  - Transaction processing
  - Subscription handling
  - Payment integration

###### AI Job Service
- **Endpoints:**
  ```
  POST   /api/v1/jobs/create
  GET    /api/v1/jobs/:id
  GET    /api/v1/jobs/:id/status
  POST   /api/v1/jobs/:id/cancel
  GET    /api/v1/jobs/:id/result
  ```
- **Responsibilities:**
  - Job queue management
  - Status tracking
  - Result retrieval
  - Error handling

###### YouTube Service
- **Endpoints:**
  ```
  POST   /api/v1/youtube/auth
  POST   /api/v1/youtube/upload
  POST   /api/v1/youtube/playlist
  GET    /api/v1/youtube/status
  ```
- **Responsibilities:**
  - OAuth integration
  - Video upload
  - Playlist management
  - Metadata handling

###### Admin Service
- **Endpoints:**
  ```
  GET    /api/v1/admin/dashboard
  GET    /api/v1/admin/users
  PATCH  /api/v1/admin/users/:id
  GET    /api/v1/admin/jobs
  GET    /api/v1/admin/analytics
  ```
- **Responsibilities:**
  - User management
  - System monitoring
  - Content moderation
  - Analytics reporting

##### 3.3 Async Job Queue
- **Technologies:**
  - Redis with BullMQ (Node.js)
  - AWS SQS (cloud-native)
- **Queue Types:**
  - High Priority: Paid users
  - Normal Priority: Free users
  - Batch Processing: Scheduled jobs
- **Features:**
  - Job retry logic
  - Dead letter queue
  - Job scheduling
  - Progress tracking

##### 3.4 Authentication
- **JWT (JSON Web Tokens):**
  - Access token: 15 minutes expiry
  - Refresh token: 7 days expiry
  - Token rotation on refresh
- **OAuth 2.0:**
  - Google Sign-In
  - GitHub Sign-In
  - YouTube API access
- **Security:**
  - bcrypt password hashing
  - Rate limiting
  - CORS configuration
  - XSS protection

---

### 4. 🗄️ DATABASE / STORAGE LAYER (Yellow #FFC107)

**Purpose:** Data persistence, caching, and file storage

#### Components:

##### 4.1 PostgreSQL / MySQL
- **Primary Database:** PostgreSQL 15+
- **Schema Design:**

```sql
-- Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) DEFAULT '',
    subscription_tier VARCHAR(50) NOT NULL DEFAULT 'free',
    credits_balance INTEGER NOT NULL DEFAULT 3,
    credits_reset_date DATE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP
);

-- Projects Table
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    script TEXT NOT NULL,
    duration_seconds INTEGER,
    status VARCHAR(50) DEFAULT 'draft',
    thumbnail_url TEXT,
    video_url TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Credits Transactions Table
CREATE TABLE credit_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    transaction_type VARCHAR(50) NOT NULL,
    amount INTEGER NOT NULL,
    balance_after INTEGER NOT NULL,
    description TEXT,
    reference_id UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AI Jobs Table
CREATE TABLE ai_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    job_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'queued',
    progress_percentage INTEGER DEFAULT 0,
    current_step VARCHAR(100),
    input_parameters JSONB,
    output_urls JSONB,
    error_message TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- YouTube Integrations Table
CREATE TABLE youtube_integrations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    channel_id VARCHAR(255),
    channel_name VARCHAR(255),
    access_token TEXT,
    refresh_token TEXT,
    token_expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_ai_jobs_status ON ai_jobs(status);
CREATE INDEX idx_ai_jobs_user_id ON ai_jobs(user_id);
CREATE INDEX idx_credit_transactions_user_id ON credit_transactions(user_id);
```

##### 4.2 Redis / ElastiCache
- **Use Cases:**
  - Session storage
  - Job queue (BullMQ)
  - API response caching
  - Rate limiting counters
  - Real-time job status
  - WebSocket pub/sub
- **Configuration:**
  ```yaml
  Cache Strategy:
    - Session: TTL 24 hours
    - API Cache: TTL 5 minutes
    - Job Status: No expiry (deleted on completion)
    - Rate Limit: TTL 60 seconds
  
  Connection Pool:
    - Min: 5
    - Max: 50
    - Idle Timeout: 300s
  ```

##### 4.3 AWS S3 + CloudFront
- **Bucket Structure:**
  ```
  ai-film-studio-media-prod/
  ├── users/
  │   └── {user_id}/
  │       ├── uploads/
  │       │   ├── images/
  │       │   ├── audio/
  │       │   └── scripts/
  │       └── projects/
  │           └── {project_id}/
  │               ├── raw/          # Original assets
  │               ├── generated/    # AI-generated content
  │               ├── intermediate/ # Processing artifacts
  │               ├── final/        # Final videos
  │               └── thumbnails/   # Video thumbnails
  ```

- **Storage Classes:**
  - Standard: Active projects (0-30 days)
  - Standard-IA: Completed projects (30-90 days)
  - Glacier: Archive (90+ days)

- **CloudFront Distribution:**
  - Global edge locations
  - SSL/TLS termination
  - Custom domain
  - Cache behaviors by file type
  - Signed URLs for private content

---

### 5. 🤖 AI / ML LAYER (Orange #FF8C00)

**Purpose:** Artificial Intelligence and Machine Learning processing

#### AI Components:

##### 5.1 Script Analysis
- **Functionality:**
  - Natural language processing
  - Scene segmentation
  - Character extraction
  - Emotion detection
  - Cultural context analysis
- **Models:**
  - GPT-4 / Claude API for text understanding
  - Custom NER (Named Entity Recognition)
  - Sentiment analysis models
- **Output:**
  - Scene breakdown with timestamps
  - Character list with descriptions
  - Cultural references identified
  - Mood and tone tags

##### 5.2 Image Generation
- **Characters & Backgrounds:**
  - Stable Diffusion XL
  - ControlNet for pose control
  - Custom LoRA models for consistency
- **Culture-Aware Generation:**
  - Indian cultural elements
  - Western themes
  - Mixed cultural contexts
  - Historical accuracy
- **Features:**
  - Character consistency across scenes
  - Background matching scene description
  - Lighting and mood adaptation
  - Style transfer options

##### 5.3 Voice Synthesis
- **Multi-age Support:**
  - Child voices (6-12 years)
  - Teen voices (13-19 years)
  - Adult voices (20-60 years)
  - Senior/mature voices (60+ years)
- **Gender Options:**
  - Male voices
  - Female voices
  - Gender-neutral voices
- **Technologies:**
  - ElevenLabs API
  - Google Cloud TTS
  - Azure Speech Services
  - Custom voice cloning (Pro feature)

##### 5.4 Lip-sync / Animation
- **Facial Animation:**
  - Lip-sync to voice audio
  - Facial expressions matching emotion
  - Eye movement and blinking
  - Micro-expressions
- **Head Movement:**
  - Natural head tilts
  - Nods and shakes
  - Gaze direction
  - Body language
- **Technologies:**
  - Wav2Lip
  - SadTalker
  - Custom animation models

##### 5.5 Music / Slokas / Poems
- **Music Generation:**
  - Background score matching mood
  - Cultural music styles
  - Adaptive tempo
- **Indian Elements:**
  - Vedic slokas
  - Devotional music
  - Classical ragas
- **Western Elements:**
  - Orchestral scores
  - Contemporary music
  - Ambient soundscapes
- **Technologies:**
  - MusicGen (Meta)
  - AudioCraft
  - Licensed music library

##### 5.6 Podcast / Dialogue Mode
- **Two-Character Conversation:**
  - Natural conversation flow
  - Turn-taking
  - Interruptions and pauses
  - Emotional reactions
- **Use Cases:**
  - Educational dialogues
  - Debates
  - Interviews
  - Storytelling
- **Features:**
  - Voice differentiation
  - Background ambiance
  - Dynamic pacing

##### 5.7 Subtitles / Multi-language
- **Generation:**
  - Automatic transcription
  - Timestamp synchronization
  - Speaker labeling
- **Languages Supported:**
  - English, Hindi, Tamil, Telugu, Malayalam
  - Spanish, French, German, Chinese
  - 15+ total languages
- **Formats:**
  - SRT, VTT, WebVTT
  - Burned-in subtitles
  - Customizable styling

#### AI Pipeline Flow:
```mermaid
sequenceDiagram
    participant Job as Job Queue
    participant Script as Script Analyzer
    participant Image as Image Generator
    participant Voice as Voice Synthesizer
    participant Lipsync as Lip-sync Engine
    participant Music as Music Generator
    participant Composer as Video Composer
    participant Output as Output Storage
    
    Job->>Script: 1. Analyze script
    Script->>Script: Extract scenes, characters, emotions
    Script->>Image: 2. Generate images for each scene
    Image->>Image: Create characters & backgrounds
    Script->>Voice: 3. Generate voice narration
    Voice->>Voice: Synthesize speech
    Voice->>Lipsync: 4. Apply lip-sync
    Lipsync->>Lipsync: Animate characters
    Script->>Music: 5. Generate music
    Music->>Music: Create background score
    
    Image->>Composer: Scene images ready
    Lipsync->>Composer: Animated scenes ready
    Music->>Composer: Audio tracks ready
    
    Composer->>Composer: 6. Compose final video
    Composer->>Output: 7. Upload final MP4
    Output->>Job: Job completed
```

---

### 6. ☁️ CLOUD / INFRASTRUCTURE LAYER (Purple #8B5CF6)

**Purpose:** Cloud services, deployment, and infrastructure management

#### Components:

##### 6.1 AWS EC2 GPU
- **Instance Types:**
  - g4dn.xlarge: NVIDIA T4, 16GB GPU memory
  - g4dn.2xlarge: For high-priority jobs
  - p3.2xlarge: NVIDIA V100 (optional for faster processing)
- **Auto Scaling:**
  - Metric: SQS queue depth
  - Scale out: Queue > 10 messages
  - Scale in: Queue < 2 messages
  - Spot instances for cost savings

##### 6.2 ECS / Kubernetes
- **ECS (Elastic Container Service):**
  - Backend API services
  - Fargate launch type
  - Service auto-scaling
  - Application Load Balancer integration
- **EKS (Elastic Kubernetes Service) - Alternative:**
  - GPU worker pods
  - Horizontal pod autoscaling
  - Node auto-scaling
  - Prometheus monitoring

##### 6.3 Terraform (IaC)
- **Infrastructure Modules:**
  ```
  infrastructure/terraform/
  ├── modules/
  │   ├── vpc/
  │   ├── ecs/
  │   ├── rds/
  │   ├── s3/
  │   ├── cloudfront/
  │   └── monitoring/
  └── environments/
      ├── dev/
      ├── sandbox/
      ├── staging/
      └── production/
  ```
- **State Management:**
  - S3 backend with versioning
  - DynamoDB for state locking
  - Separate state per environment

##### 6.4 RDS (PostgreSQL/MySQL)
- **Configuration:**
  - Multi-AZ deployment
  - Automated backups
  - Read replicas for scaling
  - Encryption at rest and in transit
- **Specifications:**
  - Dev: db.t3.medium
  - Prod: db.r6g.xlarge

##### 6.5 S3 + CloudFront
- **S3 Features:**
  - Versioning enabled
  - Lifecycle policies
  - Cross-region replication
  - Server-side encryption
- **CloudFront:**
  - Global CDN
  - Custom SSL certificate
  - Cache invalidation
  - Geo-restriction (optional)

##### 6.6 Redis / ElastiCache
- **Cluster Mode:**
  - Dev: Single node
  - Prod: Multi-AZ with replicas
- **Backup:**
  - Automated snapshots
  - Point-in-time recovery

##### 6.7 Monitoring
- **CloudWatch:**
  - Logs aggregation
  - Custom metrics
  - Alarms and notifications
  - Dashboards
- **Grafana (Optional):**
  - Advanced visualizations
  - Custom dashboards
  - Prometheus integration
- **Prometheus (Optional):**
  - Metrics collection
  - Time-series database
  - Alerting rules

##### 6.8 Environments
- **Development:**
  - Minimal resources
  - Shared services
  - Rapid iteration
  - Cost: ~$335/month
- **Sandbox:**
  - Testing new features
  - Experimental setups
  - Isolated from dev/prod
- **Staging:**
  - Production mirror
  - Pre-deployment validation
  - Performance testing
  - Cost: ~$1,500/month
- **Production:**
  - High availability
  - Auto-scaling enabled
  - Multi-AZ deployment
  - Cost: ~$2,600/month

---

### 7. 📊 SALESFORCE CRM LAYER (Light Green #90EE90)

**Purpose:** Customer relationship management and business intelligence

#### Salesforce Objects:

##### 7.1 Contacts → Users
- **Mapping:**
  ```
  Salesforce Contact ↔ Application User
  - Email → Email
  - Name → Full Name
  - Account → Subscription Tier
  - Custom Fields:
    * User_ID__c (External ID)
    * Subscription_Tier__c
    * Credits_Balance__c
    * Last_Login__c
    * Total_Projects__c
  ```
- **Sync Strategy:**
  - Real-time via API
  - Bi-directional sync
  - Conflict resolution

##### 7.2 AI_Project__c → Projects
- **Custom Object Schema:**
  ```
  AI_Project__c:
    - Name (Auto-number: PROJ-{0000})
    - User__c (Lookup to Contact)
    - Project_ID__c (External ID)
    - Title__c (Text)
    - Script__c (Long Text Area)
    - Status__c (Picklist: Draft, Processing, Completed, Failed)
    - Duration__c (Number)
    - Video_URL__c (URL)
    - Thumbnail_URL__c (URL)
    - Created_Date__c (Date/Time)
    - Completed_Date__c (Date/Time)
  ```

##### 7.3 AI_Credit__c → Credits
- **Custom Object Schema:**
  ```
  AI_Credit__c:
    - Name (Auto-number: CREDIT-{0000})
    - User__c (Lookup to Contact)
    - Transaction_Type__c (Picklist: Deduction, Purchase, Grant)
    - Amount__c (Number)
    - Balance_After__c (Number)
    - Description__c (Text)
    - Reference_ID__c (Text)
    - Transaction_Date__c (Date/Time)
  ```

##### 7.4 YouTube_Integration__c
- **Custom Object Schema:**
  ```
  YouTube_Integration__c:
    - Name (Auto-number: YT-{0000})
    - User__c (Lookup to Contact)
    - Channel_ID__c (Text)
    - Channel_Name__c (Text)
    - Is_Active__c (Checkbox)
    - Connected_Date__c (Date/Time)
    - Last_Upload_Date__c (Date/Time)
    - Total_Uploads__c (Number)
  ```

##### 7.5 Flows / Apex
- **Automated Processes:**

###### Flow: Credit Deduction on Project Start
```
Trigger: AI_Project__c status changed to "Processing"
Actions:
1. Get user's credit balance
2. Check if balance >= 1
3. If yes:
   - Create AI_Credit__c record (type: Deduction, amount: -1)
   - Update Contact's Credits_Balance__c (-1)
4. If no:
   - Update project status to "Failed"
   - Send notification to user
```

###### Flow: Credit Reset Monthly
```
Scheduled: 1st of every month, 12:00 AM
Actions:
1. Query all Contacts with Subscription_Tier__c != "Free"
2. For each contact:
   - Update Credits_Balance__c based on tier
   - Create AI_Credit__c record (type: Grant)
   - Send email notification
```

###### Apex Trigger: Project Status Update
```apex
trigger ProjectStatusTrigger on AI_Project__c (after update) {
    List<Task> tasksToCreate = new List<Task>();
    
    for (AI_Project__c project : Trigger.new) {
        AI_Project__c oldProject = Trigger.oldMap.get(project.Id);
        
        if (project.Status__c == 'Completed' && oldProject.Status__c != 'Completed') {
            // Create task for admin to review
            Task reviewTask = new Task(
                Subject = 'Review completed project: ' + project.Name,
                WhatId = project.Id,
                OwnerId = // Admin user ID,
                Priority = 'Normal',
                Status = 'Not Started'
            );
            tasksToCreate.add(reviewTask);
            
            // Send completion email to user
            // Email logic here
        }
    }
    
    if (!tasksToCreate.isEmpty()) {
        insert tasksToCreate;
    }
}
```

##### 7.6 Dashboards & Reports
- **User Analytics Dashboard:**
  - Total users by tier
  - Active users (last 30 days)
  - New registrations (daily/weekly/monthly)
  - Churn rate
- **Project Analytics Dashboard:**
  - Projects by status
  - Completion rate
  - Average processing time
  - Failed jobs analysis
- **Revenue Dashboard:**
  - MRR (Monthly Recurring Revenue)
  - Credit purchases
  - Subscription conversions
  - Revenue by tier
- **Reports:**
  - User engagement report
  - Credit usage report
  - System performance report
  - YouTube upload statistics

---

### 8. ▶️ YOUTUBE / OUTPUT LAYER (Red #DC3545)

**Purpose:** Video delivery and YouTube integration

#### Components:

##### 8.1 Video Upload (Direct)
- **YouTube Data API v3:**
  ```javascript
  const uploadVideo = async (videoFile, metadata) => {
    const youtube = google.youtube({
      version: 'v3',
      auth: oAuth2Client
    });
    
    const response = await youtube.videos.insert({
      part: 'snippet,status',
      requestBody: {
        snippet: {
          title: metadata.title,
          description: metadata.description,
          tags: metadata.tags,
          categoryId: '22', // People & Blogs
        },
        status: {
          privacyStatus: metadata.privacy || 'private',
        },
      },
      media: {
        body: fs.createReadStream(videoFile),
      },
    });
    
    return response.data;
  };
  ```
- **Features:**
  - Resumable uploads
  - Progress tracking
  - Error handling and retries
  - Batch uploads

##### 8.2 Playlist Creation
- **Functionality:**
  - Auto-create playlist per user
  - Add videos to playlist
  - Organize by project or date
  - Update playlist metadata
- **API Usage:**
  ```javascript
  const createPlaylist = async (title, description) => {
    const response = await youtube.playlists.insert({
      part: 'snippet,status',
      requestBody: {
        snippet: {
          title: title,
          description: description,
        },
        status: {
          privacyStatus: 'public',
        },
      },
    });
    return response.data;
  };
  ```

##### 8.3 Thumbnail Generation
- **Automatic Generation:**
  - Extract frame from video (at 2-second mark)
  - AI-enhanced thumbnail
  - Add title overlay
  - Branding elements
- **Upload to YouTube:**
  ```javascript
  const uploadThumbnail = async (videoId, thumbnailFile) => {
    const response = await youtube.thumbnails.set({
      videoId: videoId,
      media: {
        body: fs.createReadStream(thumbnailFile),
      },
    });
    return response.data;
  };
  ```

##### 8.4 Download Option
- **Direct Download:**
  - Generate presigned S3 URL
  - Valid for 1 hour
  - Track download count
- **Formats Available:**
  - MP4 (H.264, 1080p)
  - WebM (VP9, 1080p) - Optional
  - SRT subtitle file (separate)
- **Download API:**
  ```
  GET /api/v1/projects/:id/download
  Response: {
    "videoUrl": "https://...",
    "subtitleUrl": "https://...",
    "expiresAt": "2025-12-31T17:00:00Z"
  }
  ```

##### 8.5 Duration Selection: 1-5 Minutes
- **Duration Control:**
  - User selects desired duration
  - AI adjusts pacing and content
  - Maintains narrative coherence
- **Optimization:**
  - Shorter videos: Focus on key points
  - Longer videos: More detailed scenes
  - Dynamic scene duration
- **Implementation:**
  ```javascript
  const calculateSceneDuration = (totalDuration, sceneCount) => {
    const baseSceneDuration = totalDuration / sceneCount;
    // Adjust for intro/outro
    const introDuration = 3; // seconds
    const outroDuration = 2; // seconds
    const contentDuration = totalDuration - introDuration - outroDuration;
    
    return {
      intro: introDuration,
      sceneAverage: contentDuration / sceneCount,
      outro: outroDuration
    };
  };
  ```

---

## Flow Arrows & Dependencies

### Complete System Flow

```mermaid
graph LR
    A[👤 User Input] --> B[💻 Frontend]
    B --> C[⚙️ Backend]
    C --> D[🗄️ Database]
    C --> E[🤖 AI Layer]
    E --> F[☁️ Cloud]
    F --> D
    E --> D
    C --> G[📊 Salesforce]
    G --> B
    E --> H[▶️ YouTube]
    C --> H
    H --> B
    
    style A fill:#0066CC,color:#fff
    style B fill:#66B3FF,color:#000
    style C fill:#28A745,color:#fff
    style D fill:#FFC107,color:#000
    style E fill:#FF8C00,color:#fff
    style F fill:#8B5CF6,color:#fff
    style G fill:#90EE90,color:#000
    style H fill:#DC3545,color:#fff
```

### Detailed Dependency Flow

```mermaid
sequenceDiagram
    participant U as 👤 User
    participant FE as 💻 Frontend
    participant BE as ⚙️ Backend
    participant DB as 🗄️ Database
    participant AI as 🤖 AI Layer
    participant CL as ☁️ Cloud
    participant SF as 📊 Salesforce
    participant YT as ▶️ YouTube
    
    U->>FE: 1. Enter script & preferences
    FE->>FE: 2. Validate inputs
    FE->>BE: 3. Submit project
    BE->>DB: 4. Save project (status: draft)
    DB-->>BE: Project created
    BE-->>FE: Project ID
    FE-->>U: Show project dashboard
    
    U->>FE: 5. Click "Generate Video"
    FE->>BE: 6. Start generation job
    BE->>DB: 7. Check user credits
    DB-->>BE: Credits available
    BE->>SF: 8. Deduct credit (sync)
    BE->>DB: 9. Create job record
    BE->>AI: 10. Enqueue AI job
    BE-->>FE: Job ID
    FE-->>U: Show progress tracker
    
    AI->>AI: 11. Analyze script
    AI->>CL: 12. Request GPU resources
    CL-->>AI: GPU allocated
    AI->>AI: 13. Generate images
    AI->>AI: 14. Synthesize voice
    AI->>AI: 15. Apply lip-sync
    AI->>AI: 16. Generate music
    AI->>AI: 17. Compose video
    AI->>CL: 18. Upload to S3
    CL->>DB: 19. Update video URL
    AI->>DB: 20. Update job status (completed)
    
    FE->>BE: 21. Poll job status (every 5s)
    BE->>DB: Query job
    DB-->>BE: Status: completed
    BE-->>FE: Video ready
    FE-->>U: Show preview
    
    U->>FE: 22. Upload to YouTube
    FE->>BE: YouTube upload request
    BE->>YT: 23. Authenticate & upload
    YT-->>BE: Video ID
    BE->>DB: 24. Save YouTube video ID
    BE->>SF: 25. Update YouTube_Integration__c
    BE-->>FE: Upload successful
    FE-->>U: YouTube link
    
    U->>FE: 26. Download video
    FE->>BE: Download request
    BE->>CL: 27. Generate presigned URL
    CL-->>BE: Signed URL
    BE-->>FE: Download link
    FE-->>U: File download starts
```

### Credit and Subscription Flow

```mermaid
graph TD
    A[User Action] --> B{Has Credits?}
    B -->|Yes| C[Deduct Credit]
    B -->|No| D{Subscription Active?}
    D -->|Yes| E[Reset Credits Monthly]
    D -->|No| F[Prompt to Purchase]
    
    C --> G[Update Backend DB]
    E --> G
    F --> H[Payment Gateway]
    H --> I[Purchase Credits]
    I --> G
    
    G --> J[Sync to Salesforce]
    J --> K[Update CRM Records]
    K --> L[Send Notifications]
    L --> M[Proceed with Generation]
    
    style A fill:#0066CC,color:#fff
    style G fill:#28A745,color:#fff
    style J fill:#90EE90,color:#000
```

### AI Pipeline Dependency

```mermaid
graph TD
    A[Script Input] --> B[Script Analysis]
    B --> C{Culture Detected}
    C -->|Indian| D[Indian Cultural Assets]
    C -->|Western| E[Western Cultural Assets]
    C -->|Mixed| F[Mixed Cultural Assets]
    
    D --> G[Image Generation]
    E --> G
    F --> G
    
    B --> H[Voice Selection]
    H --> I{Multi-character?}
    I -->|Yes| J[Podcast Mode]
    I -->|No| K[Single Voice]
    
    J --> L[Voice Synthesis]
    K --> L
    
    G --> M[Lip-sync & Animation]
    L --> M
    
    B --> N{Music Type}
    N -->|Indian| O[Slokas/Classical]
    N -->|Western| P[Orchestral/Contemporary]
    
    O --> Q[Music Generation]
    P --> Q
    
    M --> R[Video Composition]
    Q --> R
    
    B --> S[Subtitle Generation]
    S --> T[Multi-language Translation]
    T --> R
    
    R --> U[Final Video Output]
    
    style A fill:#0066CC,color:#fff
    style B fill:#FF8C00,color:#fff
    style G fill:#FF8C00,color:#fff
    style L fill:#FF8C00,color:#fff
    style M fill:#FF8C00,color:#fff
    style Q fill:#FF8C00,color:#fff
    style R fill:#FF8C00,color:#fff
    style U fill:#DC3545,color:#fff
```

---

## Icon Suggestions

### Layer Icons

| Layer | Icon | Unicode | Alternative |
|-------|------|---------|-------------|
| User Layer | 👤 | U+1F464 | 👥 (multiple users) |
| Frontend | 💻 | U+1F4BB | 🖥️ (desktop computer) |
| Backend | ⚙️ | U+2699 | 🔧 (wrench) |
| Database | 🗄️ | U+1F5C4 | 💾 (floppy disk) |
| AI/ML | 🤖 | U+1F916 | 🧠 (brain) |
| Cloud | ☁️ | U+2601 | ⛅ (cloud with sun) |
| Salesforce CRM | 📊 | U+1F4CA | 📈 (chart increasing) |
| YouTube/Output | ▶️ | U+25B6 | 🎬 (clapper board) |

### Feature Icons

| Feature | Icon | Usage |
|---------|------|-------|
| Script | 📝 | Script input |
| Image | 🖼️ | Image upload/generation |
| Voice | 🎤 | Voice synthesis |
| Music | 🎵 | Music/audio |
| Video | 🎥 | Video generation |
| Upload | ⬆️ | File/video upload |
| Download | ⬇️ | File/video download |
| Settings | ⚙️ | Configuration |
| Analytics | 📊 | Reports/dashboards |
| Security | 🔒 | Authentication/encryption |
| Credit | 💳 | Payment/credits |
| Success | ✅ | Completed action |
| Error | ❌ | Failed action |
| Warning | ⚠️ | Warning message |
| Processing | ⏳ | In progress |

---

## Mermaid Diagrams

### System Architecture Diagram

```mermaid
architecture-beta
    group user[User Layer]
    group frontend[Frontend Layer]
    group backend[Backend Layer]
    group data[Data Layer]
    group ai[AI Layer]
    group cloud[Cloud Layer]
    group crm[CRM Layer]
    group output[Output Layer]

    service userInput(internet)[User Input] in user
    service reactApp(server)[React/Next.js] in frontend
    service nestjs(server)[NestJS API] in backend
    service postgres(database)[PostgreSQL] in data
    service redis(database)[Redis] in data
    service s3(disk)[S3 Storage] in data
    service aiEngine(server)[AI Engine] in ai
    service imageGen(server)[Image Gen] in ai
    service voiceGen(server)[Voice Gen] in ai
    service ec2(server)[EC2 GPU] in cloud
    service ecs(server)[ECS/K8s] in cloud
    service salesforce(server)[Salesforce] in crm
    service youtube(server)[YouTube] in output
    
    userInput:R --> L:reactApp
    reactApp:R --> L:nestjs
    nestjs:R --> L:postgres
    nestjs:R --> L:redis
    nestjs:R --> L:aiEngine
    aiEngine:R --> L:imageGen
    aiEngine:R --> L:voiceGen
    imageGen:B --> T:ec2
    voiceGen:B --> T:ec2
    aiEngine:R --> L:s3
    nestjs:B --> T:salesforce
    aiEngine:R --> L:youtube
```

### C4 Model - System Context

```mermaid
C4Context
    title System Context Diagram for AI Film Studio
    
    Person(user, "User", "Content creator, marketer, educator")
    System(aiFilmStudio, "AI Film Studio", "Generates AI-powered short films from text scripts")
    
    System_Ext(youtube, "YouTube", "Video hosting platform")
    System_Ext(salesforce, "Salesforce", "CRM system")
    System_Ext(openai, "OpenAI", "GPT models")
    System_Ext(elevenlabs, "ElevenLabs", "Voice synthesis")
    System_Ext(stripe, "Stripe", "Payment processing")
    
    Rel(user, aiFilmStudio, "Creates projects, generates videos")
    Rel(aiFilmStudio, youtube, "Uploads videos")
    Rel(aiFilmStudio, salesforce, "Syncs user and project data")
    Rel(aiFilmStudio, openai, "Uses for script analysis")
    Rel(aiFilmStudio, elevenlabs, "Uses for voice generation")
    Rel(aiFilmStudio, stripe, "Processes payments")
```

### C4 Model - Container Diagram

```mermaid
C4Container
    title Container Diagram for AI Film Studio
    
    Person(user, "User", "End user")
    
    Container(spa, "Web Application", "React, Next.js", "Provides UI for creating and managing film projects")
    Container(api, "API Gateway", "NestJS", "Handles HTTP requests, authentication, business logic")
    Container(worker, "AI Worker", "Python, PyTorch", "Processes AI generation jobs")
    ContainerDb(db, "Database", "PostgreSQL", "Stores users, projects, jobs")
    ContainerDb(cache, "Cache", "Redis", "Session storage, job queue")
    ContainerDb(storage, "Object Storage", "AWS S3", "Stores media files")
    
    System_Ext(youtube, "YouTube API")
    System_Ext(salesforce, "Salesforce API")
    
    Rel(user, spa, "Uses", "HTTPS")
    Rel(spa, api, "Makes API calls", "JSON/HTTPS")
    Rel(api, db, "Reads/writes", "SQL")
    Rel(api, cache, "Reads/writes", "Redis Protocol")
    Rel(api, storage, "Uploads/downloads", "S3 API")
    Rel(api, worker, "Enqueues jobs", "SQS/Redis")
    Rel(worker, storage, "Uploads generated content", "S3 API")
    Rel(worker, db, "Updates job status", "SQL")
    Rel(api, youtube, "Uploads videos", "YouTube Data API")
    Rel(api, salesforce, "Syncs data", "REST API")
```

---

## Implementation Guidelines

### For Figma/Canva/Lucidchart

#### Layout Structure
1. **Canvas Size:**
   - Width: 3840px (for 4K display)
   - Height: 2160px
   - Orientation: Landscape

2. **Layer Arrangement:**
   - Horizontal arrangement (left to right)
   - Or vertical arrangement (top to bottom)
   - Or hub-and-spoke (centered)

3. **Component Spacing:**
   - Margin between layers: 100px
   - Padding within layer boxes: 40px
   - Arrow spacing: 20px from components

#### Visual Design

##### Layer Boxes
- **Shape:** Rounded rectangles (corner radius: 20px)
- **Border:** 4px solid, color matching layer
- **Background:** Layer color with 20% opacity
- **Shadow:** Drop shadow (X: 4px, Y: 4px, Blur: 12px, Color: #00000040)

##### Text Styling
- **Layer Title:**
  - Font: Inter or Roboto Bold
  - Size: 32px
  - Color: White (dark backgrounds) or Black (light backgrounds)
  - Add icon prefix
- **Component Labels:**
  - Font: Inter or Roboto Regular
  - Size: 18px
  - Color: #333333
- **Descriptions:**
  - Font: Inter or Roboto Light
  - Size: 14px
  - Color: #666666

##### Arrows & Connectors
- **Arrow Style:** Solid line with arrow head
- **Width:** 3px
- **Color:** #666666
- **Types:**
  - Straight: For direct dependencies
  - Curved: For complex flows
  - Dashed: For optional/async flows

##### Icons
- **Size:** 48x48px for layer icons
- **Size:** 24x24px for feature icons
- **Style:** Consistent (all filled or all outlined)
- **Placement:** Top-left of layer boxes or inline with text

#### Color Application

```
User Layer:
- Primary: #0066CC
- Light variant: #4D94E0
- Dark variant: #004D99

Frontend Layer:
- Primary: #66B3FF
- Light variant: #99CCFF
- Dark variant: #3399FF

Backend Layer:
- Primary: #28A745
- Light variant: #5CB85C
- Dark variant: #218838

Database Layer:
- Primary: #FFC107
- Light variant: #FFD54F
- Dark variant: #FFA000

AI/ML Layer:
- Primary: #FF8C00
- Light variant: #FFB347
- Dark variant: #FF6600

Cloud Layer:
- Primary: #8B5CF6
- Light variant: #A78BFA
- Dark variant: #7C3AED

Salesforce Layer:
- Primary: #90EE90
- Light variant: #B4F0B4
- Dark variant: #6FD96F

YouTube Layer:
- Primary: #DC3545
- Light variant: #E57373
- Dark variant: #C82333
```

#### Best Practices

1. **Hierarchy:**
   - Main flow should be clearly visible
   - Secondary flows can be lighter/thinner
   - Group related components

2. **Clarity:**
   - Avoid crossing arrows when possible
   - Use consistent direction (left-to-right or top-to-bottom)
   - Label all connections

3. **Consistency:**
   - Use the same icon style throughout
   - Maintain consistent spacing
   - Apply colors uniformly

4. **Accessibility:**
   - Ensure text contrast (WCAG AA minimum)
   - Don't rely solely on color for meaning
   - Provide alt text for icons

5. **Scalability:**
   - Design at high resolution
   - Use vector graphics when possible
   - Export at multiple sizes

#### Export Settings

**For Presentations:**
- Format: PNG or PDF
- Resolution: 300 DPI
- Background: White or transparent

**For Documentation:**
- Format: SVG (preferred) or PNG
- Resolution: 150-300 DPI
- Include legends and notes

**For Web:**
- Format: SVG or WebP
- Optimize file size
- Ensure responsive design

---

## Appendix A: Technology Stack Summary

| Layer | Technologies |
|-------|-------------|
| **User Layer** | HTML5, CSS3, JavaScript |
| **Frontend** | React 18, Next.js 14, TypeScript, TailwindCSS, Material UI, Zustand, React Query |
| **Backend** | Node.js, NestJS, TypeScript, JWT, OAuth 2.0, BullMQ, Redis |
| **Database** | PostgreSQL 15, Redis 7, AWS S3, CloudFront |
| **AI/ML** | Python 3.11, PyTorch, Transformers, Diffusers, Stable Diffusion XL, ElevenLabs API, FFmpeg |
| **Cloud** | AWS (EC2, ECS, EKS, RDS, S3, SQS, CloudWatch), Terraform, Docker, Kubernetes |
| **Salesforce** | Salesforce Platform, Apex, Flow, Custom Objects, REST API |
| **YouTube** | YouTube Data API v3, OAuth 2.0 |

---

## Appendix B: API Endpoints Quick Reference

```
Authentication:
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
POST   /api/v1/auth/logout
POST   /api/v1/auth/forgot-password

Users:
GET    /api/v1/users/me
PATCH  /api/v1/users/me
DELETE /api/v1/users/me
GET    /api/v1/users/me/credits

Projects:
GET    /api/v1/projects
POST   /api/v1/projects
GET    /api/v1/projects/:id
PATCH  /api/v1/projects/:id
DELETE /api/v1/projects/:id
POST   /api/v1/projects/:id/generate

Jobs:
GET    /api/v1/jobs/:id
GET    /api/v1/jobs/:id/status
POST   /api/v1/jobs/:id/cancel
GET    /api/v1/jobs/:id/download

Credits:
GET    /api/v1/credits/balance
POST   /api/v1/credits/purchase
GET    /api/v1/credits/history

YouTube:
POST   /api/v1/youtube/auth
POST   /api/v1/youtube/upload
POST   /api/v1/youtube/playlist
GET    /api/v1/youtube/status

Admin:
GET    /api/v1/admin/dashboard
GET    /api/v1/admin/users
PATCH  /api/v1/admin/users/:id
GET    /api/v1/admin/jobs
GET    /api/v1/admin/analytics
```

---

## Appendix C: Environment Variables

```env
# Application
NODE_ENV=production
PORT=3000
API_URL=https://api.aifilmstudio.com
FRONTEND_URL=https://app.aifilmstudio.com

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname
REDIS_URL=redis://host:6379

# AWS
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=<access_key>
AWS_SECRET_ACCESS_KEY=<secret_key>
S3_BUCKET_NAME=ai-film-studio-media-prod

# Authentication
JWT_SECRET=<secret>
JWT_EXPIRATION=15m
REFRESH_TOKEN_EXPIRATION=7d

# OAuth
GOOGLE_CLIENT_ID=<client_id>
GOOGLE_CLIENT_SECRET=<secret>
GITHUB_CLIENT_ID=<client_id>
GITHUB_CLIENT_SECRET=<secret>

# AI APIs
OPENAI_API_KEY=<api_key>
ELEVENLABS_API_KEY=<api_key>

# YouTube
YOUTUBE_CLIENT_ID=<client_id>
YOUTUBE_CLIENT_SECRET=<secret>

# Salesforce
SALESFORCE_CLIENT_ID=<client_id>
SALESFORCE_CLIENT_SECRET=<secret>
SALESFORCE_USERNAME=<username>
SALESFORCE_PASSWORD=<password>
SALESFORCE_SECURITY_TOKEN=<token>

# Payment
STRIPE_SECRET_KEY=<secret_key>
STRIPE_PUBLISHABLE_KEY=<publishable_key>
```

---

## Document Revision History

| Version | Date       | Author                | Changes                                  |
|---------|------------|-----------------------|------------------------------------------|
| 1.0     | 2025-12-31 | AI-Empower-HQ-360     | Initial visual layout plan document      |

---

## Approval Signatures

This document represents the approved visual architecture layout for the AI Film Studio platform as of 2025-12-31.

**Approved by:**
- Engineering Lead: _________________ Date: _______
- Product Manager: _________________ Date: _______
- Design Lead: _________________ Date: _______

---

**End of Document**
