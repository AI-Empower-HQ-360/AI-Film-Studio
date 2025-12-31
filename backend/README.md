# Backend - AI Film Studio

## Overview

The backend of AI Film Studio consists of multiple microservices built with **FastAPI** and **Python 3.11+**. Each service handles specific business logic and communicates via REST APIs and message queues.

## Architecture

```
backend/
├── services/           # Microservices
│   ├── user-service/   # Authentication & user management
│   ├── project-service/    # Project CRUD operations
│   ├── credit-service/ # Billing & subscriptions
│   ├── ai-job-service/ # Job queue management
│   ├── youtube-service/    # YouTube integration
│   └── admin-service/  # Admin panel
├── common/             # Shared utilities
├── queue/              # Job queue definitions
├── config/             # Configuration
└── migrations/         # Database migrations
```

## Technology Stack

- **Framework**: FastAPI 0.104+
- **Language**: Python 3.11+
- **Database**: PostgreSQL 15+ (via SQLAlchemy 2.0)
- **Cache**: Redis (via redis-py)
- **Queue**: Amazon SQS
- **Authentication**: JWT (PyJWT)
- **ASGI Server**: Uvicorn
- **Migrations**: Alembic

## Microservices

### 1. User Service
**Purpose**: User authentication and profile management

**Endpoints**:
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - Logout user
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update user profile

**Database Models**:
- User (id, email, password_hash, created_at, updated_at)
- Session (id, user_id, token, expires_at)

### 2. Project Service
**Purpose**: Project CRUD and metadata management

**Endpoints**:
- `GET /api/v1/projects` - List user projects
- `POST /api/v1/projects` - Create new project
- `GET /api/v1/projects/{id}` - Get project details
- `PUT /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Delete project

**Database Models**:
- Project (id, user_id, name, description, status, created_at)
- Asset (id, project_id, type, s3_key, metadata)

### 3. Credit Service
**Purpose**: Subscription and credit management

**Endpoints**:
- `GET /api/v1/credits/balance` - Get user credit balance
- `POST /api/v1/subscriptions/checkout` - Create Stripe checkout
- `POST /api/v1/subscriptions/webhook` - Handle Stripe webhooks
- `GET /api/v1/subscriptions/current` - Get current subscription

**Database Models**:
- Subscription (id, user_id, plan, status, expires_at)
- Credit (id, user_id, balance, transaction_type)

### 4. AI Job Service
**Purpose**: Job queue management and status tracking

**Endpoints**:
- `POST /api/v1/jobs` - Create new AI job
- `GET /api/v1/jobs/{id}` - Get job status
- `GET /api/v1/jobs` - List user jobs
- `DELETE /api/v1/jobs/{id}` - Cancel job

**Database Models**:
- Job (id, project_id, type, status, parameters, result_url)

### 5. YouTube Service
**Purpose**: YouTube OAuth and video upload

**Endpoints**:
- `GET /api/v1/youtube/oauth` - Initiate OAuth flow
- `POST /api/v1/youtube/callback` - Handle OAuth callback
- `POST /api/v1/youtube/upload` - Upload video to YouTube

### 6. Admin Service
**Purpose**: Admin panel and system monitoring

**Endpoints**:
- `GET /api/v1/admin/users` - List all users
- `GET /api/v1/admin/stats` - System statistics
- `POST /api/v1/admin/users/{id}/suspend` - Suspend user

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- AWS Account (for S3, SQS)

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Run database migrations
alembic upgrade head

# Start development server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Environment Variables

Create a `.env` file with:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/aifilmstudio
REDIS_URL=redis://localhost:6379/0

# AWS
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
S3_BUCKET_NAME=ai-film-studio-media-dev
SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/123456789/ai-film-studio-jobs

# Authentication
JWT_SECRET=your-super-secret-jwt-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# External APIs
OPENAI_API_KEY=sk-xxxxx
STRIPE_SECRET_KEY=sk_test_xxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxx
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Projects Table
```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Jobs Table
```sql
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    parameters JSONB,
    result_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## Authentication

### JWT Token Flow

1. **Login**: User provides email and password
2. **Validation**: Backend validates credentials
3. **Token Generation**: JWT access token (15 min) and refresh token (7 days)
4. **Token Storage**: Frontend stores tokens (localStorage or cookies)
5. **Token Usage**: Include in `Authorization: Bearer <token>` header
6. **Token Refresh**: Use refresh token to get new access token

### Password Hashing

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
hashed = pwd_context.hash("plain_password")

# Verify password
is_valid = pwd_context.verify("plain_password", hashed)
```

## Error Handling

Standard error response format:

```json
{
  "detail": "Error message",
  "status_code": 400,
  "timestamp": "2025-12-31T12:00:00Z"
}
```

Common status codes:
- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Logging

```python
import logging

logger = logging.getLogger(__name__)

# Log levels
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

## Testing

### Unit Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=src --cov-report=html
```

### Integration Tests

```bash
# Run integration tests
pytest tests/integration/
```

## Database Migrations

### Create Migration

```bash
alembic revision --autogenerate -m "Add users table"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migration

```bash
alembic downgrade -1
```

## Docker Deployment

### Build Image

```bash
docker build -t ai-film-studio-backend:latest .
```

### Run Container

```bash
docker run -p 8000:8000 --env-file .env ai-film-studio-backend:latest
```

### Docker Compose (Local Development)

```bash
docker-compose up -d
```

This will start:
- Backend API (port 8000)
- PostgreSQL (port 5432)
- Redis (port 6379)

## Performance

### Connection Pooling

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

### Caching

```python
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Set cache
redis_client.setex('key', 3600, 'value')  # TTL: 1 hour

# Get cache
value = redis_client.get('key')
```

## Security

### CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/auth/login")
@limiter.limit("5/minute")
async def login(request: Request):
    pass
```

## Monitoring

### Health Check Endpoint

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": check_database(),
        "redis": check_redis(),
        "timestamp": datetime.utcnow()
    }
```

### Prometheus Metrics

```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

## Contributing

Please read the [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](../LICENSE)

---

For more details, see the [System Design Documentation](../docs/architecture/system-design.md).
