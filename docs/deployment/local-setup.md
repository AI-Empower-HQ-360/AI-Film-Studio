# Local Development Setup - AI Film Studio

**Version:** 1.0  
**Last Updated:** 2025-12-31

---

## 📋 Prerequisites

Before setting up the local development environment, ensure you have the following installed:

### **Required Software**

- **Node.js** 20+ and npm/yarn
- **Python** 3.11+
- **Docker** 24+ and Docker Compose
- **Git** 2.x
- **PostgreSQL** 15+ (via Docker)
- **Redis** 7+ (via Docker)

### **Optional (for AI features)**

- **CUDA Toolkit** 12.1+ (for GPU acceleration)
- **NVIDIA GPU** with 8GB+ VRAM

### **Accounts & API Keys**

- AWS Account (for S3, SQS)
- OpenAI API Key
- ElevenLabs API Key (optional)
- Stripe API Keys (test mode)
- YouTube Data API credentials (optional)

---

## 🚀 Quick Start

### **1. Clone the Repository**

```bash
git clone https://github.com/AI-Empower-HQ-360/AI-Film-Studio.git
cd AI-Film-Studio
```

### **2. Start Infrastructure Services**

```bash
# Start PostgreSQL and Redis using Docker Compose
docker-compose up -d postgres redis

# Verify services are running
docker-compose ps
```

### **3. Set Up Backend**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Edit .env with your configuration
nano .env

# Run database migrations
alembic upgrade head

# Start the backend server
uvicorn src.main:app --reload --port 8000
```

Backend will be available at: `http://localhost:8000`

### **4. Set Up Worker (Optional)**

```bash
cd worker
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Start the worker
python src/main.py
```

### **5. Set Up Frontend**

```bash
cd frontend
npm install

# Copy environment variables
cp .env.example .env.local

# Start the development server
npm run dev
```

Frontend will be available at: `http://localhost:3000`

---

## ⚙️ Configuration

### **Backend Environment Variables (.env)**

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_film_studio

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION=86400

# AWS
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
S3_BUCKET_NAME=ai-film-studio-dev

# SQS
SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/123456789/ai-film-studio-jobs-dev

# OpenAI
OPENAI_API_KEY=sk-...your-openai-key

# ElevenLabs
ELEVENLABS_API_KEY=...your-elevenlabs-key

# Stripe
STRIPE_SECRET_KEY=sk_test_...your-stripe-test-key
STRIPE_PUBLISHABLE_KEY=pk_test_...your-stripe-test-key
STRIPE_WEBHOOK_SECRET=whsec_...your-webhook-secret

# YouTube
YOUTUBE_CLIENT_ID=...your-youtube-client-id
YOUTUBE_CLIENT_SECRET=...your-youtube-client-secret

# Environment
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
```

### **Frontend Environment Variables (.env.local)**

```env
# API
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Authentication
NEXT_PUBLIC_JWT_SECRET=your-super-secret-jwt-key-change-in-production

# Stripe
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...your-stripe-test-key

# Google OAuth
NEXT_PUBLIC_GOOGLE_CLIENT_ID=...your-google-client-id

# Feature Flags
NEXT_PUBLIC_ENABLE_YOUTUBE=true
NEXT_PUBLIC_ENABLE_PODCAST=true

# Environment
NEXT_PUBLIC_ENVIRONMENT=development
```

### **Worker Environment Variables (.env)**

```env
# Same as backend, plus:

# Model Settings
MODEL_CACHE_DIR=/tmp/model-cache
USE_GPU=false
GPU_MEMORY_FRACTION=0.8

# AI APIs
HUGGINGFACE_TOKEN=hf_...your-huggingface-token
```

---

## 🗄️ Database Setup

### **Create Database**

```bash
# Using Docker
docker exec -it ai-film-studio-postgres psql -U postgres

# Inside psql
CREATE DATABASE ai_film_studio;
\q
```

### **Run Migrations**

```bash
cd backend
alembic upgrade head
```

### **Seed Data (Optional)**

```bash
# Create sample users and projects
python scripts/seed_data.py
```

---

## 🧪 Testing

### **Backend Tests**

```bash
cd backend
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific test file
pytest tests/test_user_service.py
```

### **Frontend Tests**

```bash
cd frontend
npm test

# E2E tests
npm run test:e2e

# Watch mode
npm run test:watch
```

---

## 🛠️ Development Tools

### **Database Management**

```bash
# pgAdmin (via Docker)
docker run -p 5050:80 \
  -e PGADMIN_DEFAULT_EMAIL=admin@admin.com \
  -e PGADMIN_DEFAULT_PASSWORD=admin \
  dpage/pgadmin4

# Access at: http://localhost:5050
```

### **Redis Management**

```bash
# Redis Commander
docker run -d \
  -p 8081:8081 \
  --link ai-film-studio-redis:redis \
  rediscommander/redis-commander

# Access at: http://localhost:8081
```

### **API Documentation**

```bash
# Swagger UI (automatically available)
# http://localhost:8000/docs

# ReDoc
# http://localhost:8000/redoc
```

---

## 🐛 Debugging

### **Backend Debugging (VS Code)**

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "src.main:app",
        "--reload",
        "--port",
        "8000"
      ],
      "jinja": true,
      "justMyCode": false
    }
  ]
}
```

### **Frontend Debugging (Chrome DevTools)**

1. Open Chrome DevTools
2. Go to Sources tab
3. Set breakpoints in code
4. Reload page

### **Logs**

```bash
# Backend logs
tail -f logs/backend.log

# Worker logs
tail -f logs/worker.log

# Docker logs
docker-compose logs -f postgres
docker-compose logs -f redis
```

---

## 🔧 Common Issues

### **Issue: Database Connection Error**

**Solution:**
```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Restart PostgreSQL
docker-compose restart postgres

# Check connection
psql -h localhost -U postgres -d ai_film_studio
```

### **Issue: Redis Connection Error**

**Solution:**
```bash
# Check Redis is running
docker ps | grep redis

# Test connection
redis-cli -h localhost ping
```

### **Issue: Port Already in Use**

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn src.main:app --reload --port 8001
```

### **Issue: Module Not Found**

**Solution:**
```bash
# Reinstall dependencies
cd backend
pip install -r requirements.txt --force-reinstall

cd ../frontend
npm install --legacy-peer-deps
```

---

## 📚 Additional Resources

- [Backend API Documentation](../api/README.md)
- [Frontend Component Guide](../guides/frontend-components.md)
- [AI Models Setup](../guides/ai-models-setup.md)
- [Troubleshooting Guide](../guides/troubleshooting.md)

---

## 🤝 Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for development workflow and coding standards.

---

**💻 Happy Coding!**
