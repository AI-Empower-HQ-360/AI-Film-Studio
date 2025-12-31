# AI Film Studio API - Quick Start Guide

## Overview

The AI Film Studio API provides a comprehensive platform for AI-powered video generation with user management, project tracking, credit systems, and integrations.

## Features

- 🔐 **User Authentication**: JWT-based authentication with bcrypt password hashing
- 🎬 **Project Management**: Full CRUD operations for video projects
- 💳 **Credit System**: Subscription plans and credit tracking
- 📹 **YouTube Integration**: Direct upload to YouTube
- 🤖 **AI Services**: Video, audio, lip-sync, and music generation

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/AI-Empower-HQ-360/AI-Film-Studio.git
cd AI-Film-Studio

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

### 2. Database Setup

```bash
# Install PostgreSQL and create database
createdb ai_film_studio

# Run migrations
alembic upgrade head

# Seed subscription plans
python scripts/seed_data.py
```

### 3. Run the Server

```bash
# Development mode
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# The API will be available at:
# - API: http://localhost:8000
# - Swagger Docs: http://localhost:8000/api/docs
# - ReDoc: http://localhost:8000/api/redoc
```

## API Endpoints

### Authentication

```bash
# Register a new user
curl -X POST http://localhost:8000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePass123"
  }'

# Login
curl -X POST http://localhost:8000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123"
  }'

# Response: { "access_token": "...", "token_type": "bearer" }
```

### Projects

```bash
# Create a project (requires authentication)
curl -X POST http://localhost:8000/api/projects/create \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Film",
    "script": "Once upon a time...",
    "duration": 2,
    "voice": "male"
  }'

# List projects
curl -X GET http://localhost:8000/api/projects/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get project details
curl -X GET http://localhost:8000/api/projects/{project_id} \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Credits & Subscriptions

```bash
# Get credit balance
curl -X GET http://localhost:8000/api/credits/balance \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get available plans
curl -X GET http://localhost:8000/api/credits/plans

# Top up credits
curl -X POST http://localhost:8000/api/credits/topup \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"plan_type": "Pro"}'
```

### AI Services

```bash
# Generate video
curl -X POST http://localhost:8000/api/ai/video-generate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "uuid-here",
    "script": "Your story here...",
    "duration": 2,
    "voice": "female"
  }'

# Response: { "job_id": "...", "status": "queued" }
```

## Subscription Plans

| Plan | Price | Credits | Max Video Length |
|------|-------|---------|------------------|
| **Free** | $0 | 3 | 1 minute |
| **Standard** | $39 | 30 | 10 minutes |
| **Pro** | $49 | 60 | 20 minutes |
| **Enterprise** | $99 | 120 | 40 minutes |

**Note:** 3 credits = 1 minute of video

## Cost Calculation

```
Video Cost = Duration (minutes) × 3 credits/minute
Example: 5-minute video = 5 × 3 = 15 credits
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_api.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## Project Structure

```
ai-film-studio/
├── src/
│   ├── api/
│   │   ├── main.py              # FastAPI app
│   │   ├── routes/              # API endpoints
│   │   └── schemas/             # Pydantic models
│   ├── database/
│   │   ├── base.py              # Database config
│   │   └── models/              # SQLAlchemy models
│   ├── utils/
│   │   └── auth.py              # Authentication
│   └── config/
│       └── settings.py          # Configuration
├── tests/                       # Test suite
├── alembic/                     # Database migrations
├── scripts/                     # Utility scripts
├── docs/                        # Documentation
└── requirements.txt             # Dependencies
```

## Environment Variables

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/ai_film_studio

# JWT
JWT_SECRET_KEY=your-secret-key-min-32-chars

# AWS (optional for production)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
S3_BUCKET_NAME=ai-film-studio-media

# YouTube API (optional)
YOUTUBE_CLIENT_ID=your-client-id
YOUTUBE_CLIENT_SECRET=your-client-secret
```

## API Documentation

Once the server is running:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 402 | Payment Required (insufficient credits) |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Server Error |

## Security

- All passwords are hashed using bcrypt
- JWT tokens expire after 24 hours
- HTTPS required in production
- CORS configured for specific origins
- SQL injection protected by ORM
- Input validation using Pydantic

## Support

For issues and questions:
- GitHub Issues: https://github.com/AI-Empower-HQ-360/AI-Film-Studio/issues
- Documentation: `/docs/api/API_IMPLEMENTATION.md`

## License

MIT License - see LICENSE file for details
