# AI Film Studio - Quick Reference Guide

**Version:** 1.0  
**Last Updated:** 2025-12-31

---

## 🚀 Quick Start Commands

### **Development Environment**

```bash
# Clone repository
git clone https://github.com/AI-Empower-HQ-360/AI-Film-Studio.git
cd AI-Film-Studio

# Start infrastructure
docker-compose up -d postgres redis

# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload

# Frontend
cd frontend
npm install
npm run dev

# Worker
cd worker
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

---

## 📦 Project Overview

### **What is AI Film Studio?**

An AI-powered platform that transforms text scripts into complete videos with:
- AI-generated visuals (Stable Diffusion XL)
- Voice synthesis (ElevenLabs, OpenAI TTS)
- Background music
- Multi-character podcast mode
- Direct YouTube upload

### **Technology Stack**

- **Frontend:** Next.js 14 + React 18 + TypeScript + TailwindCSS
- **Backend:** Node.js/Python + FastAPI + PostgreSQL + Redis
- **AI:** Stable Diffusion, ElevenLabs, FFmpeg
- **Cloud:** AWS (EC2, S3, RDS, SQS, CloudFront)
- **DevOps:** Docker, Terraform, GitHub Actions

---

## 🗂️ Key File Locations

```
AI-Film-Studio/
├── docs/MASTER_BLUEPRINT.md           # Complete system blueprint
├── docs/deployment/local-setup.md     # Setup guide
├── docs/guides/developer-guide.md     # Coding standards
├── backend/src/api/main.py            # Backend entry point
├── frontend/src/app/page.tsx          # Frontend home page
├── worker/src/main.py                 # Worker entry point
├── infrastructure/terraform/          # Infrastructure as Code
└── .github/workflows/                 # CI/CD pipelines
```

---

## 🔑 Environment Variables

### **Backend (.env)**

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_film_studio
REDIS_URL=redis://localhost:6379/0
JWT_SECRET=your-secret-key
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
OPENAI_API_KEY=sk-your-key
STRIPE_SECRET_KEY=sk_test_your-key
```

### **Frontend (.env.local)**

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your-key
```

---

## 📡 API Endpoints

### **Authentication**
- `POST /api/v1/auth/register` - Register user
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh token

### **Projects**
- `GET /api/v1/projects` - List projects
- `POST /api/v1/projects` - Create project
- `GET /api/v1/projects/:id` - Get project
- `PATCH /api/v1/projects/:id` - Update project
- `DELETE /api/v1/projects/:id` - Delete project

### **Jobs**
- `POST /api/v1/jobs` - Create generation job
- `GET /api/v1/jobs/:id` - Get job status
- `GET /api/v1/jobs/:id/download` - Download video

### **Credits**
- `GET /api/v1/credits/balance` - Get balance
- `POST /api/v1/credits/purchase` - Buy credits

### **YouTube**
- `GET /api/v1/youtube/auth` - Authenticate
- `POST /api/v1/youtube/upload` - Upload video

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest
pytest --cov=src

# Frontend tests
cd frontend
npm test
npm run test:e2e

# Linting
cd backend
ruff check .
black .

cd frontend
npm run lint
```

---

## 🐛 Common Issues & Solutions

### **Database Connection Error**
```bash
docker ps | grep postgres
docker-compose restart postgres
```

### **Port Already in Use**
```bash
# Find and kill process
lsof -i :8000
kill -9 <PID>
```

### **Redis Connection Error**
```bash
redis-cli -h localhost ping
docker-compose restart redis
```

### **Module Not Found**
```bash
# Backend
pip install -r requirements.txt --force-reinstall

# Frontend
npm install --legacy-peer-deps
```

---

## 🔐 Subscription Plans

| Plan | Price | Credits | Features |
|------|-------|---------|----------|
| Creator | $0 | 3/month | Basic, watermarked |
| Standard | $39 | 40/month | HD, no watermark |
| Pro | $49 | 60/month | Full features, priority |
| Enterprise | $99 | Unlimited | YouTube, CRM, support |

**Credit System:** 1 credit = 1 minute of video

---

## 🎬 Video Generation Process

1. **User inputs script** (max 500 words)
2. **Uploads character images** (optional)
3. **Selects voice** (age, gender, language)
4. **Chooses music** (genre, style)
5. **Sets duration** (1-5 minutes)
6. **Generates video** (3-5 min processing)
7. **Downloads or uploads to YouTube**

---

## 📊 Architecture Layers

```
User → CloudFront CDN → Next.js Frontend
            ↓
    Load Balancer → Backend API (ECS)
            ↓
    [PostgreSQL, Redis, S3]
            ↓
    SQS Queue → GPU Workers → AI Models
            ↓
    Final MP4 Video → S3 → User
```

---

## 🌍 Environments

| Env | URL | Purpose |
|-----|-----|---------|
| Local | http://localhost:3000 | Development |
| Sandbox | https://sandbox.ai-film-studio.com | Testing |
| Staging | https://staging.ai-film-studio.com | Pre-production |
| Production | https://ai-film-studio.com | Live |

---

## 🔀 Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes
git add .
git commit -m "feat(scope): description"

# Push and create PR
git push origin feature/my-feature
```

**Commit Format:** `<type>(<scope>): <subject>`
- Types: feat, fix, docs, style, refactor, test, chore

---

## 📞 Support & Contact

- **Documentation:** [docs/MASTER_BLUEPRINT.md](./docs/MASTER_BLUEPRINT.md)
- **Issues:** [GitHub Issues](https://github.com/AI-Empower-HQ-360/AI-Film-Studio/issues)
- **Email:** dev-team@ai-film-studio.com
- **Discord:** [Join Community](https://discord.gg/ai-film-studio)

---

## 📚 Essential Documentation

1. [Master Blueprint](./docs/MASTER_BLUEPRINT.md) - Complete overview
2. [Local Setup](./docs/deployment/local-setup.md) - Get started
3. [Developer Guide](./docs/guides/developer-guide.md) - Best practices
4. [API Docs](./docs/api/README.md) - API reference
5. [System Design](./docs/architecture/system-design.md) - Architecture

---

## ✅ Pre-Commit Checklist

- [ ] Code follows style guide
- [ ] Tests pass (`pytest` or `npm test`)
- [ ] Lint passes (`ruff` or `npm run lint`)
- [ ] Commit message follows convention
- [ ] Branch is up to date with develop
- [ ] No sensitive data in code

---

## 🎯 Useful Commands

```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f worker

# Database migrations
alembic upgrade head
alembic revision --autogenerate -m "message"

# Build Docker images
docker build -t ai-film-studio-backend ./backend
docker build -t ai-film-studio-frontend ./frontend

# Run specific test
pytest tests/test_user_service.py::test_create_user
npm test -- Button.test.tsx

# Check code coverage
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

---

**🎬 Keep this guide handy for quick reference!**

For detailed information, always refer to the [Master Blueprint](./docs/MASTER_BLUEPRINT.md).
