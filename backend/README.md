# AI Film Studio Hub - Backend

FastAPI backend service for the AI Film Studio Hub, providing authentication, project management, job orchestration, content moderation, and asset storage.

## Features

- **JWT Authentication**: Secure user authentication with JWT tokens
- **Project Management**: Create and manage video projects
- **Job State Machine**: Robust job processing with state transitions
- **Content Moderation**: OpenAI-powered content moderation pipeline
- **Signed URLs**: S3 presigned URLs for secure asset uploads/downloads
- **RESTful APIs**: Comprehensive API for all operations

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Initialize database:
```bash
# Database will be created automatically on first run
```

## Running

### Development
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## Architecture

```
backend/
├── app/
│   ├── api/           # API endpoints
│   │   ├── auth.py    # Authentication endpoints
│   │   ├── projects.py # Project management
│   │   └── jobs.py    # Job management
│   ├── core/          # Core functionality
│   │   ├── config.py  # Configuration
│   │   ├── security.py # JWT & password handling
│   │   └── state_machine.py # Job state machine
│   ├── models/        # Database models
│   │   ├── database.py # Database setup
│   │   └── models.py  # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   │   ├── user.py
│   │   ├── project.py
│   │   └── job.py
│   ├── services/      # Business logic
│   │   ├── moderation.py # Content moderation
│   │   ├── storage.py    # S3 signed URLs
│   │   └── job_service.py # Job management
│   └── main.py        # FastAPI app
└── requirements.txt
```

## Job State Machine

Jobs follow this state machine:

```
PENDING → VALIDATING → QUEUED → PROCESSING → 
  GENERATING_IMAGES → GENERATING_VIDEO → 
  GENERATING_AUDIO → COMPOSING → COMPLETED

(Any state can transition to FAILED or CANCELLED)
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get token
- `GET /api/v1/auth/me` - Get current user

### Projects
- `POST /api/v1/projects` - Create project
- `GET /api/v1/projects` - List projects
- `GET /api/v1/projects/{id}` - Get project
- `PUT /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Delete project

### Jobs
- `POST /api/v1/jobs` - Create job
- `GET /api/v1/jobs` - List jobs
- `GET /api/v1/jobs/{id}` - Get job
- `PATCH /api/v1/jobs/{id}/status` - Update job status
- `POST /api/v1/jobs/{id}/cancel` - Cancel job
- `GET /api/v1/jobs/{id}/download-url` - Get signed download URL
- `GET /api/v1/jobs/{id}/valid-transitions` - Get valid state transitions

## Configuration

See `.env.example` for all configuration options.

Key settings:
- `SECRET_KEY`: JWT secret (generate with `openssl rand -hex 32`)
- `DATABASE_URL`: Database connection string
- `AWS_*`: AWS credentials for S3 storage
- `OPENAI_API_KEY`: OpenAI API key for content moderation
- `REDIS_*`: Redis connection for job queue
