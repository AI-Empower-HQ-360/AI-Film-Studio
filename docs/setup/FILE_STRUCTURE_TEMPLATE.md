# 📁 AI Film Studio - Complete Master File Structure Template

> **Comprehensive directory structure for all layers: Backend, Frontend, Worker, Infrastructure, and DevOps**

📋 **Tags:** `#file-structure` `#architecture` `#project-template` `#organization`

---

## 📑 Table of Contents

- [Root Level Structure](#root-level-structure)
- [Backend Service Structure](#backend-service-structure)
- [Worker Service Structure](#worker-service-structure)
- [Frontend Structure](#frontend-structure)
- [Infrastructure Structure](#infrastructure-structure)
- [Documentation Structure](#documentation-structure)
- [Scripts & Utilities](#scripts--utilities)
- [Configuration Files](#configuration-files)

---

## Root Level Structure

```
ai-film-studio/
├── .github/                          # GitHub specific files
│   ├── workflows/                    # CI/CD pipelines
│   │   ├── backend-ci-cd.yml         # Backend deployment workflow
│   │   ├── frontend-ci-cd.yml        # Frontend deployment workflow
│   │   ├── worker-ci-cd.yml          # Worker deployment workflow
│   │   ├── terraform-deploy.yml      # Infrastructure deployment
│   │   ├── security-scan.yml         # Security scanning
│   │   └── test-coverage.yml         # Test coverage reporting
│   ├── ISSUE_TEMPLATE/               # Issue templates
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── enhancement.md
│   ├── PULL_REQUEST_TEMPLATE.md      # PR template
│   └── CODEOWNERS                    # Code ownership
│
├── backend/                          # Backend FastAPI service
│   ├── src/                          # Source code
│   │   ├── api/                      # API routes and endpoints
│   │   │   ├── v1/                   # API version 1
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py           # Authentication endpoints
│   │   │   │   ├── users.py          # User management endpoints
│   │   │   │   ├── projects.py       # Project management endpoints
│   │   │   │   ├── credits.py        # Credit management endpoints
│   │   │   │   ├── jobs.py           # Job management endpoints
│   │   │   │   ├── youtube.py        # YouTube integration endpoints
│   │   │   │   ├── admin.py          # Admin endpoints
│   │   │   │   └── webhooks.py       # Webhook endpoints
│   │   │   └── dependencies.py       # API dependencies
│   │   │
│   │   ├── models/                   # Database models (SQLAlchemy)
│   │   │   ├── __init__.py
│   │   │   ├── user.py               # User model
│   │   │   ├── project.py            # Project model
│   │   │   ├── credit.py             # Credit model
│   │   │   ├── job.py                # Job model
│   │   │   ├── subscription.py       # Subscription model
│   │   │   └── youtube_integration.py # YouTube integration model
│   │   │
│   │   ├── schemas/                  # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py               # User schemas
│   │   │   ├── project.py            # Project schemas
│   │   │   ├── credit.py             # Credit schemas
│   │   │   ├── job.py                # Job schemas
│   │   │   └── auth.py               # Auth schemas
│   │   │
│   │   ├── services/                 # Business logic services
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py       # Authentication service
│   │   │   ├── user_service.py       # User service
│   │   │   ├── project_service.py    # Project service
│   │   │   ├── credit_service.py     # Credit service
│   │   │   ├── job_service.py        # Job service
│   │   │   ├── youtube_service.py    # YouTube service
│   │   │   ├── salesforce_service.py # Salesforce integration
│   │   │   ├── notification_service.py # Notification service
│   │   │   └── payment_service.py    # Payment service
│   │   │
│   │   ├── core/                     # Core functionality
│   │   │   ├── __init__.py
│   │   │   ├── config.py             # Configuration management
│   │   │   ├── database.py           # Database connection
│   │   │   ├── security.py           # Security utilities
│   │   │   ├── cache.py              # Cache management
│   │   │   ├── logging.py            # Logging configuration
│   │   │   └── exceptions.py         # Custom exceptions
│   │   │
│   │   ├── middleware/               # Custom middleware
│   │   │   ├── __init__.py
│   │   │   ├── auth_middleware.py    # Authentication middleware
│   │   │   ├── rate_limit.py         # Rate limiting
│   │   │   ├── cors.py               # CORS configuration
│   │   │   └── error_handler.py      # Error handling
│   │   │
│   │   ├── utils/                    # Utility functions
│   │   │   ├── __init__.py
│   │   │   ├── aws.py                # AWS utilities
│   │   │   ├── validators.py         # Validation utilities
│   │   │   ├── helpers.py            # Helper functions
│   │   │   └── constants.py          # Constants
│   │   │
│   │   ├── migrations/               # Database migrations (Alembic)
│   │   │   ├── versions/             # Migration versions
│   │   │   ├── env.py                # Alembic environment
│   │   │   └── script.py.mako        # Migration template
│   │   │
│   │   └── main.py                   # FastAPI application entry point
│   │
│   ├── tests/                        # Backend tests
│   │   ├── unit/                     # Unit tests
│   │   │   ├── test_auth.py
│   │   │   ├── test_users.py
│   │   │   ├── test_projects.py
│   │   │   └── test_credits.py
│   │   ├── integration/              # Integration tests
│   │   │   ├── test_api_endpoints.py
│   │   │   ├── test_database.py
│   │   │   └── test_services.py
│   │   ├── e2e/                      # End-to-end tests
│   │   │   └── test_workflows.py
│   │   ├── conftest.py               # Pytest configuration
│   │   └── fixtures/                 # Test fixtures
│   │
│   ├── alembic.ini                   # Alembic configuration
│   ├── requirements.txt              # Python dependencies
│   ├── requirements-dev.txt          # Development dependencies
│   ├── Dockerfile                    # Docker configuration
│   ├── docker-compose.yml            # Local development setup
│   ├── .dockerignore                 # Docker ignore file
│   ├── pyproject.toml                # Python project configuration
│   ├── setup.py                      # Setup script
│   └── README.md                     # Backend documentation
│
├── worker/                           # AI Worker service (GPU)
│   ├── src/                          # Source code
│   │   ├── main.py                   # Worker entry point
│   │   ├── config.py                 # Worker configuration
│   │   │
│   │   ├── queue/                    # Queue management
│   │   │   ├── __init__.py
│   │   │   ├── consumer.py           # SQS consumer
│   │   │   ├── producer.py           # SQS producer
│   │   │   └── handlers.py           # Job handlers
│   │   │
│   │   ├── processors/               # Processing pipeline
│   │   │   ├── __init__.py
│   │   │   ├── script_parser.py      # Parse script into scenes
│   │   │   ├── image_generator.py    # Generate images with SD
│   │   │   ├── video_generator.py    # Generate video clips
│   │   │   ├── audio_generator.py    # Generate audio/voiceover
│   │   │   ├── lip_sync.py           # Lip-sync processing
│   │   │   ├── video_compositor.py   # Compose final video
│   │   │   └── uploader.py           # Upload to S3/YouTube
│   │   │
│   │   ├── models/                   # AI model management
│   │   │   ├── __init__.py
│   │   │   ├── stable_diffusion.py   # Stable Diffusion wrapper
│   │   │   ├── video_diffusion.py    # Video generation models
│   │   │   ├── tts_engine.py         # Text-to-speech
│   │   │   ├── music_generator.py    # Music generation
│   │   │   └── model_loader.py       # Model loading utilities
│   │   │
│   │   ├── utils/                    # Worker utilities
│   │   │   ├── __init__.py
│   │   │   ├── ffmpeg.py             # FFmpeg utilities
│   │   │   ├── gpu_utils.py          # GPU management
│   │   │   ├── file_utils.py         # File operations
│   │   │   └── logging.py            # Logging
│   │   │
│   │   └── schemas/                  # Data schemas
│   │       ├── __init__.py
│   │       ├── job_schema.py         # Job data structure
│   │       └── scene_schema.py       # Scene data structure
│   │
│   ├── tests/                        # Worker tests
│   │   ├── test_processors.py
│   │   ├── test_models.py
│   │   └── test_queue.py
│   │
│   ├── scripts/                      # Utility scripts
│   │   ├── download_models.py        # Download AI models
│   │   ├── test_gpu.py               # Test GPU setup
│   │   └── benchmark.py              # Performance benchmarking
│   │
│   ├── requirements.txt              # Python dependencies
│   ├── requirements-gpu.txt          # GPU-specific dependencies
│   ├── Dockerfile                    # Docker configuration
│   └── README.md                     # Worker documentation
│
├── frontend/                         # Next.js Frontend
│   ├── src/                          # Source code
│   │   ├── app/                      # Next.js App Router
│   │   │   ├── layout.tsx            # Root layout
│   │   │   ├── page.tsx              # Home page
│   │   │   ├── globals.css           # Global styles
│   │   │   │
│   │   │   ├── (auth)/               # Auth routes group
│   │   │   │   ├── login/
│   │   │   │   │   └── page.tsx
│   │   │   │   ├── register/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── forgot-password/
│   │   │   │       └── page.tsx
│   │   │   │
│   │   │   ├── (dashboard)/          # Dashboard routes group
│   │   │   │   ├── layout.tsx        # Dashboard layout
│   │   │   │   ├── projects/
│   │   │   │   │   ├── page.tsx      # Projects list
│   │   │   │   │   ├── [id]/
│   │   │   │   │   │   └── page.tsx  # Project detail
│   │   │   │   │   └── new/
│   │   │   │   │       └── page.tsx  # New project
│   │   │   │   ├── credits/
│   │   │   │   │   └── page.tsx
│   │   │   │   ├── settings/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── admin/
│   │   │   │       └── page.tsx
│   │   │   │
│   │   │   └── api/                  # API routes
│   │   │       ├── auth/
│   │   │       │   ├── [...nextauth]/
│   │   │       │   │   └── route.ts
│   │   │       │   └── youtube/
│   │   │       │       └── callback/
│   │   │       │           └── route.ts
│   │   │       └── webhooks/
│   │   │           └── stripe/
│   │   │               └── route.ts
│   │   │
│   │   ├── components/               # React components
│   │   │   ├── ui/                   # UI components
│   │   │   │   ├── button.tsx
│   │   │   │   ├── input.tsx
│   │   │   │   ├── card.tsx
│   │   │   │   ├── dialog.tsx
│   │   │   │   ├── dropdown.tsx
│   │   │   │   └── ...
│   │   │   │
│   │   │   ├── layout/               # Layout components
│   │   │   │   ├── header.tsx
│   │   │   │   ├── sidebar.tsx
│   │   │   │   ├── footer.tsx
│   │   │   │   └── navigation.tsx
│   │   │   │
│   │   │   ├── project/              # Project components
│   │   │   │   ├── project-card.tsx
│   │   │   │   ├── project-form.tsx
│   │   │   │   ├── script-editor.tsx
│   │   │   │   └── video-preview.tsx
│   │   │   │
│   │   │   └── common/               # Common components
│   │   │       ├── loading.tsx
│   │   │       ├── error.tsx
│   │   │       └── toast.tsx
│   │   │
│   │   ├── lib/                      # Library code
│   │   │   ├── api.ts                # API client
│   │   │   ├── auth.ts               # Authentication
│   │   │   ├── utils.ts              # Utilities
│   │   │   └── constants.ts          # Constants
│   │   │
│   │   ├── hooks/                    # Custom React hooks
│   │   │   ├── useAuth.ts
│   │   │   ├── useProjects.ts
│   │   │   ├── useCredits.ts
│   │   │   └── useToast.ts
│   │   │
│   │   ├── store/                    # State management
│   │   │   ├── index.ts
│   │   │   ├── authStore.ts
│   │   │   ├── projectStore.ts
│   │   │   └── uiStore.ts
│   │   │
│   │   ├── types/                    # TypeScript types
│   │   │   ├── index.ts
│   │   │   ├── user.ts
│   │   │   ├── project.ts
│   │   │   └── api.ts
│   │   │
│   │   └── styles/                   # Styles
│   │       └── tailwind.css
│   │
│   ├── public/                       # Static assets
│   │   ├── images/
│   │   ├── icons/
│   │   └── fonts/
│   │
│   ├── tests/                        # Frontend tests
│   │   ├── unit/
│   │   ├── integration/
│   │   └── e2e/
│   │
│   ├── .env.local.example            # Environment variables example
│   ├── next.config.js                # Next.js configuration
│   ├── tailwind.config.js            # Tailwind CSS configuration
│   ├── tsconfig.json                 # TypeScript configuration
│   ├── package.json                  # Node dependencies
│   ├── package-lock.json
│   ├── .eslintrc.json                # ESLint configuration
│   ├── .prettierrc                   # Prettier configuration
│   └── README.md                     # Frontend documentation
│
├── infrastructure/                   # Infrastructure as Code
│   ├── terraform/                    # Terraform configurations
│   │   ├── modules/                  # Reusable modules
│   │   │   ├── vpc/                  # VPC module
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   ├── outputs.tf
│   │   │   │   └── README.md
│   │   │   │
│   │   │   ├── rds/                  # RDS module
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   │
│   │   │   ├── elasticache/          # ElastiCache module
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   │
│   │   │   ├── s3/                   # S3 module
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   │
│   │   │   ├── ecs/                  # ECS module
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   │
│   │   │   ├── eks/                  # EKS module
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   │
│   │   │   ├── alb/                  # Application Load Balancer
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   │
│   │   │   ├── cloudfront/           # CloudFront module
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   │
│   │   │   ├── sqs/                  # SQS module
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   │
│   │   │   └── monitoring/           # Monitoring module
│   │   │       ├── main.tf
│   │   │       ├── variables.tf
│   │   │       └── outputs.tf
│   │   │
│   │   ├── environments/             # Environment configurations
│   │   │   ├── dev/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   ├── terraform.tfvars
│   │   │   │   ├── backend.tf
│   │   │   │   └── outputs.tf
│   │   │   │
│   │   │   ├── sandbox/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   ├── terraform.tfvars
│   │   │   │   ├── backend.tf
│   │   │   │   └── outputs.tf
│   │   │   │
│   │   │   ├── staging/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   ├── terraform.tfvars
│   │   │   │   ├── backend.tf
│   │   │   │   └── outputs.tf
│   │   │   │
│   │   │   └── prod/
│   │   │       ├── main.tf
│   │   │       ├── variables.tf
│   │   │       ├── terraform.tfvars
│   │   │       ├── backend.tf
│   │   │       └── outputs.tf
│   │   │
│   │   └── README.md                 # Terraform documentation
│   │
│   ├── kubernetes/                   # Kubernetes manifests
│   │   ├── base/                     # Base configurations
│   │   │   ├── namespace.yaml
│   │   │   ├── configmap.yaml
│   │   │   ├── secrets.yaml
│   │   │   └── service-account.yaml
│   │   │
│   │   ├── backend/                  # Backend deployment
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
│   │   │   ├── hpa.yaml              # Horizontal Pod Autoscaler
│   │   │   └── ingress.yaml
│   │   │
│   │   ├── worker/                   # Worker deployment
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
│   │   │   └── pvc.yaml              # Persistent Volume Claim
│   │   │
│   │   ├── monitoring/               # Monitoring stack
│   │   │   ├── prometheus.yaml
│   │   │   ├── grafana.yaml
│   │   │   └── alertmanager.yaml
│   │   │
│   │   └── helm/                     # Helm charts
│   │       ├── backend/
│   │       │   ├── Chart.yaml
│   │       │   ├── values.yaml
│   │       │   ├── values-dev.yaml
│   │       │   ├── values-staging.yaml
│   │       │   ├── values-prod.yaml
│   │       │   └── templates/
│   │       │
│   │       └── worker/
│   │           ├── Chart.yaml
│   │           ├── values.yaml
│   │           └── templates/
│   │
│   └── docker/                       # Docker configurations
│       ├── docker-compose.dev.yml
│       ├── docker-compose.test.yml
│       └── docker-compose.prod.yml
│
├── docs/                             # Documentation
│   ├── setup/                        # Setup guides
│   │   ├── ENVIRONMENT_SETUP_MASTER_CHECKLIST.md
│   │   ├── FILE_STRUCTURE_TEMPLATE.md
│   │   ├── ENV_VARIABLES_REFERENCE.md
│   │   ├── AWS_SETUP_GUIDE.md
│   │   ├── SALESFORCE_INTEGRATION_GUIDE.md
│   │   └── AI_MODELS_CONFIGURATION.md
│   │
│   ├── architecture/                 # Architecture documentation
│   │   ├── system-design.md          # High-level system design
│   │   ├── database-schema.md        # Database schema
│   │   ├── api-design.md             # API design
│   │   ├── security-design.md        # Security architecture
│   │   └── diagrams/                 # Architecture diagrams
│   │       ├── system-overview.png
│   │       ├── data-flow.png
│   │       └── deployment.png
│   │
│   ├── requirements/                 # Requirements documents
│   │   ├── FRD.md                    # Functional Requirements
│   │   ├── NFR.md                    # Non-Functional Requirements
│   │   └── BRD.md                    # Business Requirements
│   │
│   ├── api/                          # API documentation
│   │   ├── openapi.yaml              # OpenAPI specification
│   │   ├── postman-collection.json   # Postman collection
│   │   └── README.md                 # API overview
│   │
│   ├── operations/                   # Operations documentation
│   │   ├── runbooks/                 # Operational runbooks
│   │   │   ├── deployment.md
│   │   │   ├── rollback.md
│   │   │   ├── incident-response.md
│   │   │   └── disaster-recovery.md
│   │   │
│   │   ├── monitoring.md             # Monitoring guide
│   │   ├── alerting.md               # Alerting configuration
│   │   └── troubleshooting.md        # Troubleshooting guide
│   │
│   └── development/                  # Development guides
│       ├── getting-started.md        # Getting started guide
│       ├── coding-standards.md       # Coding standards
│       ├── testing-guide.md          # Testing guide
│       └── contributing.md           # Contributing guide
│
├── scripts/                          # Utility scripts
│   ├── setup/                        # Setup scripts
│   │   ├── init-dev.sh               # Initialize dev environment
│   │   ├── init-database.sh          # Initialize database
│   │   ├── seed-data.sh              # Seed test data
│   │   └── download-models.sh        # Download AI models
│   │
│   ├── deploy/                       # Deployment scripts
│   │   ├── deploy-backend.sh
│   │   ├── deploy-worker.sh
│   │   ├── deploy-frontend.sh
│   │   └── rollback.sh
│   │
│   ├── maintenance/                  # Maintenance scripts
│   │   ├── backup-database.sh
│   │   ├── cleanup-storage.sh
│   │   └── rotate-logs.sh
│   │
│   └── utils/                        # Utility scripts
│       ├── check-health.sh
│       ├── run-migrations.sh
│       └── generate-secrets.sh
│
├── tests/                            # End-to-end tests
│   ├── e2e/
│   │   ├── test_full_workflow.py
│   │   └── test_integration.py
│   └── load/
│       ├── locustfile.py
│       └── scenarios/
│
├── .env.dev.template                 # Dev environment template
├── .env.sandbox.template             # Sandbox environment template
├── .env.staging.template             # Staging environment template
├── .env.prod.template                # Production environment template
│
├── .gitignore                        # Git ignore file
├── .gitattributes                    # Git attributes
├── .editorconfig                     # Editor configuration
├── .dockerignore                     # Docker ignore file
│
├── Makefile                          # Make commands
├── docker-compose.yml                # Docker Compose for local dev
├── LICENSE                           # License file
├── README.md                         # Main README
├── CONTRIBUTING.md                   # Contributing guidelines
├── CHANGELOG.md                      # Change log
└── CODE_OF_CONDUCT.md                # Code of conduct
```

---

## Configuration Files

### Root Level Configuration Files

#### `.gitignore`
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
dist/
*.egg-info/

# AI/ML
models/
*.pth
*.pt
*.ckpt
data/raw/
data/processed/

# Environment
.env
.env.local
.env.*.local
!.env*.template

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
logs/
*.log

# OS
.DS_Store
Thumbs.db

# Build
dist/
build/
.next/
node_modules/

# Terraform
*.tfstate
*.tfstate.*
.terraform/
*.tfvars
!*.tfvars.example

# Secrets
secrets/
credentials/
*.pem
*.key
*.crt
```

#### `Makefile`
```makefile
.PHONY: help install dev test build deploy clean

help:
	@echo "AI Film Studio - Make Commands"
	@echo "==============================="
	@echo "install      - Install all dependencies"
	@echo "dev          - Start development environment"
	@echo "test         - Run all tests"
	@echo "build        - Build all services"
	@echo "deploy-dev   - Deploy to dev environment"
	@echo "deploy-prod  - Deploy to production"
	@echo "clean        - Clean build artifacts"

install:
	cd backend && pip install -r requirements.txt
	cd worker && pip install -r requirements.txt
	cd frontend && npm install

dev:
	docker-compose up -d

test:
	cd backend && pytest
	cd worker && pytest
	cd frontend && npm test

build:
	cd backend && docker build -t aifilm-backend .
	cd worker && docker build -t aifilm-worker .
	cd frontend && npm run build

deploy-dev:
	./scripts/deploy/deploy-backend.sh dev
	./scripts/deploy/deploy-worker.sh dev
	./scripts/deploy/deploy-frontend.sh dev

deploy-prod:
	./scripts/deploy/deploy-backend.sh prod
	./scripts/deploy/deploy-worker.sh prod
	./scripts/deploy/deploy-frontend.sh prod

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	cd frontend && rm -rf .next node_modules
	cd backend && rm -rf build dist
```

#### `docker-compose.yml`
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: aifilmstudio_dev
      POSTGRES_USER: aifilm
      POSTGRES_PASSWORD: devpassword
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://aifilm:devpassword@postgres:5432/aifilmstudio_dev
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend:/app

  worker:
    build: ./worker
    environment:
      - DATABASE_URL=postgresql://aifilm:devpassword@postgres:5432/aifilmstudio_dev
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    volumes:
      - ./worker:/app
      - model_cache:/app/models

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/node_modules

volumes:
  postgres_data:
  redis_data:
  model_cache:
```

---

## Environment-Specific Terraform Variables

### `infrastructure/terraform/environments/dev/terraform.tfvars`
```hcl
# Tags
environment = "dev"
project     = "ai-film-studio"
owner       = "devops-team"

# VPC
vpc_cidr           = "10.0.0.0/16"
availability_zones = ["us-east-1a"]

# RDS
db_instance_class    = "db.t3.micro"
db_allocated_storage = 20
db_multi_az          = false

# ElastiCache
redis_node_type = "cache.t3.micro"
redis_num_nodes = 1

# EC2 GPU
gpu_instance_type = "g4dn.xlarge"
gpu_instance_count = 1

# ECS
ecs_desired_count = 1
ecs_min_count     = 1
ecs_max_count     = 2

# S3
enable_versioning = true
enable_encryption = true
```

### `infrastructure/terraform/environments/prod/terraform.tfvars`
```hcl
# Tags
environment = "prod"
project     = "ai-film-studio"
owner       = "ops-team"

# VPC
vpc_cidr           = "10.10.0.0/16"
availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]

# RDS
db_instance_class    = "db.r5.large"
db_allocated_storage = 500
db_multi_az          = true

# ElastiCache
redis_node_type = "cache.r5.large"
redis_num_nodes = 3

# EC2 GPU
gpu_instance_type = "g4dn.12xlarge"
gpu_instance_count = 4

# ECS
ecs_desired_count = 4
ecs_min_count     = 4
ecs_max_count     = 50

# S3
enable_versioning = true
enable_encryption = true
enable_replication = true
```

---

## 📝 Summary

This comprehensive file structure provides:

✅ **Clear separation of concerns** - Backend, Worker, Frontend, Infrastructure  
✅ **Scalable architecture** - Microservices, containers, IaC  
✅ **Complete CI/CD pipeline** - GitHub Actions workflows  
✅ **Environment management** - Dev, Sandbox, Staging, Production  
✅ **Documentation** - Architecture, API, Operations, Development  
✅ **Testing infrastructure** - Unit, Integration, E2E, Load tests  
✅ **Security** - Secrets management, IAM, encryption  
✅ **Monitoring** - CloudWatch, Prometheus, Grafana  
✅ **Disaster Recovery** - Backups, replication, rollback strategies  

---

**🎉 With this structure, your development team can start coding immediately with a well-organized, production-ready project!**

---

_Last Updated: 2025-01-01_  
_Version: 1.0.0_  
_Maintained by: AI-Empower-HQ-360_
