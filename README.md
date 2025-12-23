# AI Film Studio Hub

End-to-end AI Film Studio: script → scenes → shots → video → MP4

A complete starter repository for an AI-powered film generation platform with backend API, GPU worker pipeline, and modern web frontend.

## 🎬 Overview

AI Film Studio Hub enables users to generate AI-powered films from text scripts. The system consists of three main components:

1. **Backend (FastAPI)**: Authentication, project management, job orchestration
2. **Worker (Python GPU)**: Image generation, video synthesis, audio creation, FFmpeg composition
3. **Frontend (Next.js)**: User interface for script entry, job tracking, video preview

## 🏗️ Architecture

```
┌─────────────────┐
│   Frontend      │
│   (Next.js)     │
│                 │
│ - Script Entry  │
│ - Job Progress  │
│ - Video Preview │
└────────┬────────┘
         │
         │ REST API
         │
┌────────▼────────┐      ┌─────────────────┐
│    Backend      │      │     Worker      │
│    (FastAPI)    │◄────►│  (Celery+GPU)   │
│                 │ Queue│                 │
│ - Auth (JWT)    │      │ - Image Gen     │
│ - Projects      │      │ - Video Gen     │
│ - Jobs API      │      │ - Audio Gen     │
│ - Moderation    │      │ - FFmpeg        │
│ - Signed URLs   │      │                 │
└────────┬────────┘      └─────────────────┘
         │
         │
    ┌────▼────┐
    │  Redis  │
    │  Queue  │
    └─────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Redis
- FFmpeg
- (Optional) CUDA-capable GPU for faster processing

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
uvicorn app.main:app --reload
```

Backend will be available at http://localhost:8000
API docs at http://localhost:8000/api/v1/docs

### 2. Worker Setup

```bash
cd worker
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
celery -A celery_app worker --loglevel=info
```

### 3. Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with your API URL
npm run dev
```

Frontend will be available at http://localhost:3000

### 4. Redis Setup

```bash
# Ubuntu/Debian
sudo apt-get install redis-server
redis-server

# macOS
brew install redis
redis-server

# Docker
docker run -d -p 6379:6379 redis:alpine
```

## 📁 Project Structure

```
ai-film-studio/
├── backend/                 # FastAPI backend service
│   ├── app/
│   │   ├── api/            # API endpoints (auth, projects, jobs)
│   │   ├── core/           # Config, security, state machine
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── main.py         # FastAPI app
│   ├── requirements.txt
│   └── README.md
│
├── worker/                  # GPU worker pipeline
│   ├── pipelines/
│   │   ├── image_generation.py   # Stable Diffusion
│   │   ├── video_generation.py   # Video synthesis
│   │   ├── audio_generation.py   # Audio/music gen
│   │   └── ffmpeg_composer.py    # Video composition
│   ├── utils/
│   │   └── api_client.py         # Backend API client
│   ├── celery_app.py            # Celery config
│   ├── tasks.py                 # Job processing
│   ├── config.py
│   ├── requirements.txt
│   └── README.md
│
├── frontend/                # Next.js frontend
│   ├── app/                # App Router pages
│   ├── components/         # React components
│   │   ├── ScriptEditor.tsx
│   │   ├── JobProgress.tsx
│   │   └── VideoPreview.tsx
│   ├── lib/                # API client, auth
│   ├── styles/             # CSS styles
│   ├── package.json
│   └── README.md
│
├── .gitignore
├── LICENSE
└── README.md
```

## 🔑 Key Features

### Backend
- **JWT Authentication**: Secure user authentication with JWT tokens
- **Project Management**: CRUD operations for film projects
- **Job State Machine**: Robust state transitions for job processing
- **Content Moderation**: OpenAI-powered content filtering
- **Signed URLs**: S3 presigned URLs for secure asset storage
- **RESTful API**: Comprehensive API with OpenAPI documentation

### Worker
- **Image Generation**: Stable Diffusion XL for high-quality images
- **Video Synthesis**: Convert images to video with motion
- **Audio Generation**: Background music and narration (placeholder)
- **FFmpeg Composition**: Professional video encoding and composition
- **GPU Acceleration**: CUDA/MPS support for fast processing
- **Distributed Processing**: Celery-based task queue

### Frontend
- **Modern UI**: Responsive design with Tailwind CSS
- **Real-time Updates**: Auto-refreshing job progress
- **Script Editor**: Rich text input for film scripts
- **Video Preview**: In-browser video playback
- **Download Management**: Secure video downloads via signed URLs

## 🔄 Job Processing Flow

1. User writes script in frontend
2. Frontend creates project and job via API
3. Backend validates and queues job
4. Worker picks up job from queue
5. Worker generates images from scenes
6. Worker creates video from images
7. Worker generates background audio
8. Worker composes final video with FFmpeg
9. Worker uploads video to storage
10. Job status updated to "completed"
11. User previews and downloads video

## 🎛️ Configuration

Each component has its own configuration:

- **Backend**: `backend/.env` - Database, Redis, AWS, API keys
- **Worker**: `worker/.env` - GPU settings, models, storage
- **Frontend**: `frontend/.env.local` - API URL

See individual README files for detailed configuration options.

## 🧪 Testing

### Backend
```bash
cd backend
# Add pytest and tests (to be implemented)
pytest
```

### Frontend
```bash
cd frontend
npm run lint
npm run build
```

### Worker
```bash
cd worker
# Test celery worker
celery -A celery_app call tasks.test_task
```

## 📊 Job State Machine

Jobs follow these states:

```
PENDING → VALIDATING → QUEUED → PROCESSING → 
  GENERATING_IMAGES → GENERATING_VIDEO → 
  GENERATING_AUDIO → COMPOSING → COMPLETED

(Any state can transition to FAILED or CANCELLED)
```

## 🛠️ Technology Stack

**Backend:**
- FastAPI
- SQLAlchemy
- JWT (python-jose)
- Boto3 (AWS S3)
- OpenAI API

**Worker:**
- Celery
- PyTorch
- Diffusers (Stable Diffusion)
- MoviePy
- FFmpeg

**Frontend:**
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Zustand
- Axios

**Infrastructure:**
- Redis (job queue)
- PostgreSQL/SQLite (database)
- S3 (asset storage)

## 📝 API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## 🤝 Contributing

This is a starter repository. To extend:

1. Add more AI models (video, audio, effects)
2. Implement advanced video editing features
3. Add team collaboration features
4. Implement payment/subscription system
5. Add analytics and monitoring
6. Optimize GPU utilization
7. Add more export formats

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Stability AI for Stable Diffusion models
- OpenAI for moderation API
- HuggingFace for model hosting
- FastAPI and Next.js communities

## 📞 Support

For issues or questions:
- Check individual component READMEs
- Review API documentation
- Open an issue on GitHub

---

Built with ❤️ for the AI film generation community
