# 🚀 AI Film Studio - Quick Setup Guide

> **Get started with AI Film Studio in under 30 minutes**

📋 **Tags:** `#quickstart` `#setup` `#onboarding` `#getting-started`

---

## 🎯 Prerequisites

Before you begin, ensure you have:

- [ ] **AWS Account** with admin access
- [ ] **GitHub Account** and repository cloned
- [ ] **Docker Desktop** installed and running
- [ ] **Node.js 18+** and npm installed
- [ ] **Python 3.11+** installed
- [ ] **Terraform 1.5+** installed
- [ ] **AWS CLI** configured with credentials
- [ ] **Google Cloud Account** (for YouTube API)
- [ ] **Salesforce Developer Account** (free tier)

---

## ⚡ Quick Start (Development Environment)

### Step 1: Clone and Setup Environment (5 minutes)

```bash
# Clone the repository
git clone https://github.com/AI-Empower-HQ-360/AI-Film-Studio.git
cd AI-Film-Studio

# Copy environment template
cp .env.dev.template .env.dev

# Edit .env.dev with your credentials
nano .env.dev  # or use your preferred editor
```

**Required Changes in `.env.dev`:**
- Update AWS credentials (or use AWS CLI profile)
- Add Salesforce credentials
- Add YouTube API credentials
- Generate JWT secret: `openssl rand -hex 32`
- Generate session secret: `openssl rand -hex 32`

### Step 2: Start Local Services with Docker (3 minutes)

> **Note:** The repository currently uses standalone Docker containers for local development.
> A `docker-compose.yml` file can be created using the template in [FILE_STRUCTURE_TEMPLATE.md](./FILE_STRUCTURE_TEMPLATE.md).

```bash
# Start PostgreSQL
docker run --name ai-film-studio-postgres \
  -e POSTGRES_USER=aifilm \
  -e POSTGRES_PASSWORD="$(openssl rand -base64 24)" \
  -e POSTGRES_DB=aifilmstudio_dev \
  -p 5432:5432 \
  -d postgres:15

# Start Redis
docker run --name ai-film-studio-redis \
  -p 6379:6379 \
  -d redis:7-alpine

# Verify services are running
docker ps
```

### Step 3: Setup Backend (5 minutes)

```bash
# From the repository root (not a backend/ subdirectory)
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations (if alembic is configured)
# alembic upgrade head

# Start backend server with environment file
uvicorn src.api.main:app --reload --env-file .env.dev
```

> **Loading Environment Variables:** The Python services read from `os.environ`.
> Use `--env-file` with uvicorn, or `source .env.dev` before running.

Backend should now be running at `http://localhost:8000`

### Step 4: Setup Frontend (5 minutes)

> **Note:** The Next.js frontend lives in the `frontend/` directory.
> Verify it exists before proceeding.

```bash
# In a new terminal, from the repository root
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.local.example .env.local

# Edit .env.local
nano .env.local

# Start development server
npm run dev
```

Frontend should now be running at `http://localhost:3000`

### Step 5: Setup Worker (Optional - GPU Service)

> **Note:** The dedicated GPU worker service for heavy AI generation jobs may be
> deployed separately or integrated with the main backend. Follow the worker
> service's own setup guide if available.

```bash
# If a worker/ directory exists:
cd worker

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download AI models (this may take a while)
python scripts/download_models.py

# Start worker
python src/main.py
```

### Step 6: Test the Setup (2 minutes)

1. Open browser: `http://localhost:3000`
2. Register a new account
3. Create a test project
4. Verify API connection: `http://localhost:8000/docs`

---

## 🏗️ Infrastructure Setup (AWS)

### Option 1: Automated Setup with Terraform (Recommended)

```bash
cd infrastructure/terraform/environments/dev

# Initialize Terraform
terraform init

# Review planned changes
terraform plan

# Apply infrastructure
terraform apply

# Save outputs
terraform output > outputs.txt
```

**What This Creates:**
- VPC with public/private subnets
- RDS PostgreSQL instance
- ElastiCache Redis cluster
- S3 buckets for media/videos
- SQS queue for jobs
- Security groups and IAM roles

### Option 2: Manual Setup via AWS Console

Follow the detailed guide in the [Environment Setup Master Checklist](./ENVIRONMENT_SETUP_MASTER_CHECKLIST.md#2️⃣-aws-account-setup)

---

## 🔧 Configuration Checklist

### AWS Configuration

- [ ] Create IAM user with programmatic access
- [ ] Configure AWS CLI: `aws configure`
- [ ] Create S3 buckets:
  - `aifilmstudio-dev-media`
  - `aifilmstudio-dev-videos`
  - `aifilmstudio-dev-models`
- [ ] Create SQS queue: `aifilmstudio-dev-jobs`
- [ ] Set up RDS PostgreSQL instance
- [ ] Set up ElastiCache Redis cluster

### Salesforce Configuration

- [ ] Sign up for Salesforce Developer Edition
- [ ] Create custom objects (AI_Project__c, AI_Credit__c, etc.)
- [ ] Create connected app for API access
- [ ] Generate OAuth credentials
- [ ] Add credentials to `.env.dev`

### YouTube API Configuration

- [ ] Create Google Cloud project
- [ ] Enable YouTube Data API v3
- [ ] Create OAuth 2.0 credentials
- [ ] Add authorized redirect URIs
- [ ] Add credentials to `.env.dev`

### Security Setup

- [ ] Generate JWT secret key
- [ ] Generate session secret
- [ ] Set up AWS Secrets Manager (for staging/prod)
- [ ] Configure CORS origins
- [ ] Set up API rate limiting

---

## 🧪 Testing Your Setup

### Backend Tests

```bash\n# Run from repository root\npytest tests/ -v\n```

### Frontend Tests

```bash
cd frontend
npm test
```

### Integration Tests

```bash
# From repository root
pytest tests/ -v
```

### Manual Testing

1. **API Health Check**
   ```bash
   curl http://localhost:8000/api/v1/health
   ```

2. **API Root Status**
   ```bash
   curl http://localhost:8000/
   ```

3. **Create Project**
   - Log in to `http://localhost:3000`
   - Create a new project
   - Upload a script
   - Submit for processing

---

## 🐛 Common Issues and Solutions

### Issue: "Connection refused" to PostgreSQL

**Solution:**
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Restart PostgreSQL
docker-compose restart postgres

# Check logs
docker-compose logs postgres
```

### Issue: "Module not found" errors

**Solution:**
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Issue: Port already in use

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or change the port in .env.dev
API_PORT=8001
```

### Issue: AWS credentials not working

**Solution:**
```bash
# Verify AWS CLI configuration
aws sts get-caller-identity

# Reconfigure if needed
aws configure

# Or use environment variables in .env.dev
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
```

### Issue: GPU not detected (Worker)

**Solution:**
```bash
# Check CUDA installation
nvidia-smi

# Verify PyTorch can see GPU
python -c "import torch; print(torch.cuda.is_available())"

# Install CUDA toolkit if missing
# Follow: https://developer.nvidia.com/cuda-downloads
```

---

## 📚 Next Steps

### For Developers

1. Review Coding Standards (coming soon)
2. Read API Documentation (coming soon)
3. Explore [Architecture Design](../architecture/system-design.md)
4. Check Testing Guide (coming soon)

### For DevOps

1. Complete AWS Setup Guide (follow [Environment Setup Checklist](./ENVIRONMENT_SETUP_MASTER_CHECKLIST.md#2️⃣-aws-account-setup))
2. Configure CI/CD Pipelines (coming soon)
3. Set up Monitoring (follow [Environment Setup Checklist](./ENVIRONMENT_SETUP_MASTER_CHECKLIST.md#23-monitoring--logging))
4. Review Deployment Strategy (coming soon)

### For QA

1. Set up [Sandbox Environment](./ENVIRONMENT_SETUP_MASTER_CHECKLIST.md#9️⃣-environment-mapping-summary)
2. Review Test Cases (coming soon)
3. Configure Test Data (coming soon)

---

## 🎓 Learning Resources

### Documentation

- [Environment Setup Master Checklist](./ENVIRONMENT_SETUP_MASTER_CHECKLIST.md)
- [File Structure Template](./FILE_STRUCTURE_TEMPLATE.md)
- [Environment Variables Reference](./ENV_VARIABLES_REFERENCE.md)

### Video Tutorials (Coming Soon)

- Setting up development environment
- Creating your first project
- Deploying to AWS
- Monitoring and troubleshooting

### Community

- GitHub Discussions: [Ask Questions](https://github.com/AI-Empower-HQ-360/AI-Film-Studio/discussions)
- Issues: [Report Bugs](https://github.com/AI-Empower-HQ-360/AI-Film-Studio/issues)

---

## ✅ Setup Verification Checklist

Before moving to development, verify:

- [ ] Backend API responding at `http://localhost:8000`
- [ ] Frontend app running at `http://localhost:3000`
- [ ] PostgreSQL database connection working
- [ ] Redis cache connection working
- [ ] AWS S3 buckets accessible
- [ ] SQS queue created and accessible
- [ ] User registration working
- [ ] Project creation working
- [ ] API documentation accessible at `/docs`
- [ ] Tests passing (`pytest` and `npm test`)

---

## 🆘 Getting Help

If you encounter issues:

1. **Check Logs**
   ```bash
   # Backend logs
   docker-compose logs backend
   
   # Worker logs
   docker-compose logs worker
   
   # Database logs
   docker-compose logs postgres
   ```

2. **Search Existing Issues**
   - [GitHub Issues](https://github.com/AI-Empower-HQ-360/AI-Film-Studio/issues)

3. **Ask for Help**
   - [GitHub Discussions](https://github.com/AI-Empower-HQ-360/AI-Film-Studio/discussions)
   - Create a new issue with:
     - Environment details (OS, versions)
     - Steps to reproduce
     - Error messages
     - Relevant logs

4. **Contact Support**
   - Email: support@aifilmstudio.com
   - Slack: [Join our workspace](https://aifilmstudio.slack.com)

---

## 🎉 Congratulations!

You've successfully set up AI Film Studio on your local machine!

**What's Next?**

- Start coding and contributing
- Deploy to staging environment
- Explore advanced features
- Join our community

---

_Last Updated: 2025-01-01_  
_Version: 1.0.0_  
_Maintained by: AI-Empower-HQ-360_
