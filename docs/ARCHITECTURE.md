# Architecture Documentation

## System Overview

AI Film Studio is a microservices-based platform for generating AI films from text scripts.

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│             │         │             │         │             │
│  Frontend   │────────▶│   Backend   │────────▶│   Worker    │
│  (Next.js)  │         │  (FastAPI)  │         │  (Celery)   │
│             │◀────────│             │◀────────│             │
└─────────────┘         └─────────────┘         └─────────────┘
                              │                        │
                              │                        │
                              ▼                        ▼
                        ┌──────────┐           ┌──────────┐
                        │PostgreSQL│           │  Redis   │
                        └──────────┘           └──────────┘
                              │                        
                              │                        
                              ▼                        
                        ┌──────────┐                   
                        │   AWS S3 │                   
                        └──────────┘                   
```

## Components

### Frontend (Next.js)

**Technology:** Next.js 14, TypeScript, Tailwind CSS

**Responsibilities:**
- User interface for script input
- Real-time job progress tracking
- Video preview and download
- Authentication UI

**Key Features:**
- Server-side rendering (SSR)
- API client with automatic token refresh
- Responsive design
- Real-time polling for job updates

### Backend (FastAPI)

**Technology:** FastAPI, Python 3.9+, Pydantic

**Responsibilities:**
- RESTful API endpoints
- JWT authentication
- Request validation
- Business logic coordination
- Database operations
- Cost governance
- Content moderation

**Architecture Layers:**
```
Controllers (API Endpoints)
      ↓
Services (Business Logic)
      ↓
Models (Data Layer)
      ↓
Database
```

**Key Components:**

1. **Authentication (`/auth`)**
   - User registration
   - Login with JWT tokens
   - Token refresh

2. **Projects (`/projects`)**
   - CRUD operations for projects
   - User ownership validation

3. **Jobs (`/jobs`)**
   - Job creation and management
   - State machine transitions
   - Cost estimation
   - Signed URL generation

4. **Services:**
   - `state_machine.py` - Job lifecycle management
   - `moderation.py` - Content safety checking
   - `cost_governance.py` - Budget management
   - `s3_service.py` - File storage and retrieval

### Worker (Celery)

**Technology:** Celery, Redis, Python 3.9+

**Responsibilities:**
- Asynchronous task processing
- AI model integrations
- Video composition
- Retry logic

**Task Pipeline:**

```
┌──────────────────┐
│ Image Generation │ (10-20 images)
└────────┬─────────┘
         ▼
┌──────────────────┐
│ Video Generation │ (compose with transitions)
└────────┬─────────┘
         ▼
    ┌────────────────────┐
    │  Audio Generation  │ (parallel)
    ├────────────────────┤
    │ Voice Synthesis    │
    │ Music Synthesis    │
    └────────┬───────────┘
             ▼
    ┌────────────────────┐
    │ FFmpeg Composition │ (final assembly)
    └────────┬───────────┘
             ▼
    ┌────────────────────┐
    │    Upload to S3    │
    └────────────────────┘
```

**Task Types:**

1. **Image Generation**
   - Input: Text prompts from script
   - Output: PNG images
   - API: OpenAI DALL-E / Stability AI

2. **Video Generation**
   - Input: Image sequence
   - Output: Video file (no audio)
   - Tools: FFmpeg / Runway ML

3. **Voice Synthesis**
   - Input: Script text
   - Output: Audio file (voice)
   - API: OpenAI TTS / ElevenLabs

4. **Music Synthesis**
   - Input: Genre, mood, duration
   - Output: Audio file (music)
   - API: MusicGen / Mubert

5. **FFmpeg Composition**
   - Input: Video + voice + music
   - Output: Final MP4 with audio
   - Tools: FFmpeg

### Database (PostgreSQL)

**Schema:**

```sql
users
  - id (PK)
  - email (unique)
  - username (unique)
  - hashed_password
  - is_active
  - created_at

projects
  - id (PK)
  - name
  - description
  - user_id (FK -> users.id)
  - created_at
  - updated_at

jobs
  - id (PK)
  - project_id (FK -> projects.id)
  - user_id (FK -> users.id)
  - script
  - status (enum)
  - progress (0-100)
  - estimated_cost
  - actual_cost
  - moderation_status
  - moderation_score
  - output_url
  - signed_url
  - signed_url_expires_at
  - config (JSON)
  - error_message
  - retry_count
  - created_at
  - updated_at
  - started_at
  - completed_at

job_state_history
  - id (PK)
  - job_id (FK -> jobs.id)
  - from_state
  - to_state
  - reason
  - created_at

cost_records
  - id (PK)
  - user_id (FK -> users.id)
  - job_id (FK -> jobs.id)
  - service
  - cost
  - currency
  - created_at
```

### Message Broker (Redis)

**Purpose:**
- Celery task queue
- Task results storage
- Distributed locking (optional)

**Queues:**
- `celery` - Default queue for all tasks
- Can be expanded to separate queues for different task types

### Storage (AWS S3)

**Structure:**
```
bucket/
  outputs/
    job_{id}/
      output.mp4
      images/
        image_0001.png
        ...
      audio/
        narration.mp3
        music.mp3
  temp/
    job_{id}/
      ...
```

**Features:**
- Signed URLs for secure downloads
- Lifecycle policies for cleanup
- Regional distribution

## State Machine

Job lifecycle is managed by a strict state machine:

```
┌─────────┐
│ pending │
└────┬────┘
     ▼
┌─────────┐
│ queued  │
└────┬────┘
     ▼
┌────────────┐
│ moderating │
└────┬────┬──┘
     │    │
     │    ▼
     │  ┌──────────────────┐
     │  │ moderation_failed│
     │  └────────┬─────────┘
     │           │
     │           ▼
     │      ┌──────────┐
     │      │cancelled │
     │      └──────────┘
     ▼
┌────────────┐
│ processing │
└────┬───┬───┘
     │   │
     │   ▼
     │ ┌────────┐
     │ │ failed │
     │ └───┬────┘
     │     │
     │     ▼
     │ ┌──────────┐
     │ │cancelled │
     │ └──────────┘
     ▼
┌───────────┐
│ completed │
└───────────┘
```

**Transition Rules:**
- Only valid transitions are allowed
- All transitions are logged in `job_state_history`
- Terminal states: `completed`, `cancelled`, `moderation_failed`

## Security

### Authentication
- JWT tokens (access + refresh)
- Access token expiry: 30 minutes
- Refresh token expiry: 7 days
- bcrypt password hashing

### Authorization
- User-based resource isolation
- Project ownership validation
- Job ownership validation

### Content Moderation
- Automated script scanning
- Keyword filtering
- Configurable threshold
- Integration-ready for ML-based moderation

### Data Protection
- Signed URLs with expiration
- Environment variable secrets
- No sensitive data in logs

## Scalability

### Horizontal Scaling
- **Frontend:** Static deployment (CDN)
- **Backend:** Multiple API instances behind load balancer
- **Worker:** Multiple Celery workers
- **Database:** Read replicas
- **Redis:** Redis Cluster

### Vertical Scaling
- Worker instance size for heavy tasks
- Database instance size for high load

### Performance Optimizations
- Connection pooling
- Async I/O in FastAPI
- Task result expiry in Redis
- Database query optimization
- Image/video compression

## Monitoring

### Metrics to Track
- API response times
- Task processing times
- Error rates
- Queue lengths
- Cost per job
- User activity

### Recommended Tools
- **APM:** New Relic, DataDog
- **Logs:** ELK Stack, CloudWatch
- **Metrics:** Prometheus + Grafana
- **Errors:** Sentry

## Deployment

### Development
```bash
# Backend
uvicorn app.main:app --reload

# Worker
celery -A celery_app worker --loglevel=info

# Frontend
npm run dev
```

### Production

**Backend:**
- Docker + Kubernetes
- Or: AWS ECS, Google Cloud Run
- Environment variables via secrets

**Worker:**
- Docker + Kubernetes
- Or: AWS ECS with autoscaling
- Separate queue consumers

**Frontend:**
- Vercel (recommended)
- Or: Netlify, AWS Amplify
- CDN distribution

**Database:**
- Managed PostgreSQL (RDS, Cloud SQL)
- Automated backups
- Connection pooling

**Redis:**
- Managed Redis (ElastiCache, MemoryStore)
- Persistence enabled

## Cost Optimization

1. **Use spot instances** for workers
2. **Implement caching** for repeated requests
3. **Set S3 lifecycle policies** to delete old files
4. **Use compression** for videos
5. **Batch operations** where possible
6. **Monitor AI API costs** closely

## Future Enhancements

- WebSocket support for real-time updates
- Video editing capabilities
- Multiple output formats
- Template library
- Team collaboration
- Advanced analytics
- Custom AI model fine-tuning
