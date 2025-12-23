# AI Film Studio

End-to-end AI Film Studio: script → scenes → shots → video → MP4

A complete starter repository for building an AI-powered film generation platform with backend APIs, worker pipeline, and frontend interface.

## 🎬 Features

### Backend (FastAPI)
- **JWT Authentication**: Secure user registration and login with access/refresh tokens
- **Project Management**: Create and manage film projects
- **Job System**: Create and track film generation jobs
- **State Machine**: Robust job state transitions (pending → queued → processing → completed)
- **Content Moderation**: Automated script moderation for safety
- **Cost Governance**: Budget management and cost estimation
- **Signed URL Downloads**: Secure S3-based file downloads with expiring URLs

### Worker (Python + Celery)
- **Image Generation**: Convert script scenes to AI-generated images
- **Video Generation**: Compose images into video with transitions
- **Voice Synthesis**: Text-to-speech narration
- **Music Synthesis**: Background music generation
- **FFmpeg Composition**: Final video assembly with audio tracks
- **Retry Logic**: Automatic retry with exponential backoff
- **Pipeline Architecture**: Celery-based task orchestration

### Frontend (Next.js + TypeScript)
- **Script Input**: Intuitive interface for script creation
- **Job Progress**: Real-time progress tracking with polling
- **Video Preview**: Built-in video player
- **Download Feature**: One-click secure downloads
- **Responsive Design**: Tailwind CSS styling

## 📁 Project Structure

```
AI-Film-Studio/
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── api/             # API endpoints
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       │   ├── auth.py      # Authentication
│   │   │       │   ├── projects.py  # Project management
│   │   │       │   └── jobs.py      # Job management
│   │   │       └── api.py
│   │   ├── core/            # Core configuration
│   │   │   ├── config.py    # Settings
│   │   │   └── security.py  # JWT & auth utilities
│   │   ├── models/          # Database models
│   │   │   └── models.py
│   │   ├── schemas/         # Pydantic schemas
│   │   │   └── schemas.py
│   │   ├── services/        # Business logic
│   │   │   ├── state_machine.py      # Job state machine
│   │   │   ├── moderation.py         # Content moderation
│   │   │   ├── cost_governance.py    # Cost management
│   │   │   └── s3_service.py         # S3 operations
│   │   └── main.py          # FastAPI app
│   ├── requirements.txt
│   └── .env.example
│
├── worker/                   # Celery worker
│   ├── tasks/               # Task handlers
│   │   ├── image_generation.py
│   │   ├── video_generation.py
│   │   ├── voice_synthesis.py
│   │   ├── music_synthesis.py
│   │   └── ffmpeg_composition.py
│   ├── utils/
│   │   └── retry_logic.py   # Retry decorators
│   ├── celery_app.py        # Celery configuration
│   ├── pipeline.py          # Pipeline orchestrator
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/                 # Next.js frontend
    ├── app/                 # App router pages
    │   ├── page.tsx         # Home page
    │   ├── layout.tsx
    │   └── globals.css
    ├── components/          # React components
    │   ├── ScriptInput.tsx
    │   ├── JobProgress.tsx
    │   ├── VideoPreview.tsx
    │   └── DownloadButton.tsx
    ├── lib/                 # Utilities
    │   ├── api.ts           # API client
    │   └── types.ts         # TypeScript types
    ├── package.json
    └── .env.local.example
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Redis (for Celery)
- PostgreSQL (optional, using mock data by default)
- FFmpeg (for video processing)

### Backend Setup

1. **Navigate to backend directory**:
```bash
cd backend
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run the server**:
```bash
python -m app.main
# Or use uvicorn:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
- API Docs: `http://localhost:8000/api/v1/docs`
- Health Check: `http://localhost:8000/health`

### Worker Setup

1. **Navigate to worker directory**:
```bash
cd worker
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment**:
```bash
cp .env.example .env
# Add your API keys for AI services
```

5. **Start Redis** (if not running):
```bash
redis-server
```

6. **Run Celery worker**:
```bash
celery -A celery_app worker --loglevel=info
```

### Frontend Setup

1. **Navigate to frontend directory**:
```bash
cd frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Configure environment**:
```bash
cp .env.local.example .env.local
# Set NEXT_PUBLIC_API_URL to your backend URL
```

4. **Run development server**:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 📖 API Documentation

### Authentication

#### Register
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword123"
}
```

#### Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

### Projects

#### Create Project
```http
POST /api/v1/projects/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "My First Film",
  "description": "A short film about AI"
}
```

#### List Projects
```http
GET /api/v1/projects/
Authorization: Bearer <access_token>
```

### Jobs

#### Create Job
```http
POST /api/v1/jobs/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "project_id": 1,
  "script": "A beautiful sunrise over mountains\nBirds flying in the sky\nA peaceful lake",
  "config": {
    "num_images": 10,
    "video_duration": 30,
    "include_voice": true,
    "include_music": true
  }
}
```

#### Get Job Status
```http
GET /api/v1/jobs/{job_id}
Authorization: Bearer <access_token>
```

#### Get Signed Download URL
```http
POST /api/v1/jobs/signed-url
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "job_id": 1
}
```

## 🔧 Configuration

### Backend Configuration

Edit `backend/.env`:

```env
# Security
SECRET_KEY=your-super-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/aifilmstudio

# AWS S3
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
S3_BUCKET_NAME=ai-film-studio-outputs

# Cost Limits
MAX_COST_PER_JOB=100.0
MAX_COST_PER_USER_DAILY=500.0

# Moderation
ENABLE_CONTENT_MODERATION=true
MODERATION_THRESHOLD=0.8
```

### Worker Configuration

Edit `worker/.env`:

```env
# Redis
REDIS_URL=redis://localhost:6379/0

# AI Service API Keys
OPENAI_API_KEY=your-openai-api-key
STABILITY_API_KEY=your-stability-api-key
ELEVENLABS_API_KEY=your-elevenlabs-key
```

### Frontend Configuration

Edit `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🏗️ Architecture

### Job Processing Pipeline

1. **User submits script** → Frontend sends to backend
2. **Job creation** → Backend validates, estimates cost, moderates content
3. **Job queued** → Added to Celery queue
4. **Worker processes**:
   - Generate images from script scenes
   - Create video from images with transitions
   - Synthesize voice narration (parallel)
   - Generate background music (parallel)
   - Compose final video with FFmpeg
5. **Upload to S3** → Store output file
6. **Job completed** → User can download via signed URL

### State Machine

```
pending → queued → moderating → processing → completed
                        ↓              ↓
                  moderation_failed  failed
                        ↓              ↓
                    cancelled ← ← ← ← ←
```

## 🔐 Security

- **JWT Authentication**: Secure token-based auth with refresh tokens
- **Content Moderation**: Automated script screening
- **Signed URLs**: Temporary, secure download links
- **Cost Governance**: Prevent runaway spending
- **Input Validation**: Pydantic schemas for all inputs

## 💰 Cost Management

The system tracks and limits costs:

- **Per-job limits**: Default $100 per job
- **Daily user limits**: Default $500 per user per day
- **Cost estimation**: Before job creation
- **Real-time tracking**: Actual costs recorded

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📦 Deployment

### Backend Deployment

**Docker**:
```bash
cd backend
docker build -t ai-film-studio-backend .
docker run -p 8000:8000 ai-film-studio-backend
```

**Heroku/Railway/Render**: Use `Procfile` with:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Worker Deployment

**Docker**:
```bash
cd worker
docker build -t ai-film-studio-worker .
docker run ai-film-studio-worker
```

**Cloud**: Deploy to AWS ECS, Google Cloud Run, or Azure Container Instances

### Frontend Deployment

**Vercel** (recommended):
```bash
cd frontend
vercel
```

**Netlify**:
```bash
npm run build
# Deploy the .next directory
```

## 🛠️ Development

### Adding New Task Types

1. Create new task file in `worker/tasks/`
2. Define task function with `@celery_app.task` decorator
3. Add retry logic with `@celery_retry_on_exception`
4. Update pipeline in `worker/pipeline.py`

### Adding New API Endpoints

1. Create endpoint in `backend/app/api/v1/endpoints/`
2. Add schema to `backend/app/schemas/schemas.py`
3. Include router in `backend/app/api/v1/api.py`

### Adding New Frontend Components

1. Create component in `frontend/components/`
2. Add types to `frontend/lib/types.ts`
3. Import and use in pages

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check documentation at `/docs`

## 🎯 Roadmap

- [ ] WebSocket support for real-time updates
- [ ] Advanced video editing features
- [ ] Multiple AI model support
- [ ] Team collaboration features
- [ ] Video templates library
- [ ] Export to multiple formats
- [ ] Social media integration

---

Built with ❤️ using FastAPI, Celery, and Next.js
