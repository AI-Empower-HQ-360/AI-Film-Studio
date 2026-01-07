# Copilot Coding Agent Instructions for AI Film Studio

## Repository Overview

AI Film Studio is a cloud-native platform that transforms text scripts into cinematic short films (30-90 seconds) using AI-powered image/video generation. This is a monorepo containing:

- **Python Backend (FastAPI)**: REST API for job orchestration, auth, and credits
- **Next.js Frontend**: React-based UI with TypeScript and Tailwind CSS
- **Infrastructure as Code**: Terraform for AWS deployment
- **GPU Worker Pipeline**: Python-based AI processing (Stable Diffusion XL, video composition)

**Size**: Medium repository with ~50 source files across multiple directories.

---

## Build & Development Commands

### Python Backend (Root Directory)

**Prerequisites**: Python 3.11+ (tested with 3.12.3)

```bash
# Install dependencies (ALWAYS run first)
pip install -r requirements.txt

# Additional required dependency (not in requirements.txt)
pip install httpx

# Run tests
python -m pytest tests/ -v

# Run linting
python -m flake8 src/ tests/

# Run type checking
python -m mypy src/

# Format code
python -m black src/ tests/

# Start development server
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Known Issues**:
- The `requirements.txt` is missing `httpx` which is required for `TestClient`. Always run `pip install httpx` after installing requirements.
- Source files have some whitespace and formatting issues that `flake8` will report. These are pre-existing and not critical.

### Next.js Frontend (frontend/ Directory)

**Prerequisites**: Node.js 18+ (tested with v20.19.6)

```bash
cd frontend

# Install dependencies (ALWAYS run first)
npm install

# Run linting
npm run lint

# Build for production (static export)
npm run build

# Start development server
npm run dev

# Start production server
npm run start
```

**Build Output**: Static files exported to `frontend/out/` directory (configured for S3/CloudFront deployment).

---

## Project Structure

```
/
├── src/                      # Python backend source
│   ├── api/
│   │   ├── __init__.py
│   │   └── main.py           # FastAPI app entry point
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py       # Configuration settings
│   ├── services/
│   │   └── __init__.py
│   └── utils/
│       ├── __init__.py
│       └── logger.py         # Logging utility
├── tests/
│   ├── __init__.py
│   └── test_api.py           # API tests
├── frontend/                 # Next.js frontend
│   ├── src/app/
│   │   ├── components/
│   │   │   └── LandingPage.tsx
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.mjs       # Static export config
│   └── .eslintrc.json
├── infrastructure/
│   └── terraform/
│       └── environments/
│           └── dev/
│               ├── main.tf   # Complete AWS infrastructure
│               └── variables.tf
├── docs/
│   ├── architecture/
│   │   └── system-design.md  # System architecture details
│   └── requirements/
│       ├── FRD.md            # Functional requirements
│       └── NFR.md            # Non-functional requirements
├── scripts/
│   └── setup.sh              # Development setup script
├── requirements.txt          # Python dependencies
├── setup.py                  # Python package setup
├── Dockerfile                # Container image build
├── .env.example              # Environment template
└── .gitignore
```

---

## Key Configuration Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies (FastAPI, PyTorch, etc.) |
| `frontend/package.json` | Frontend dependencies and npm scripts |
| `frontend/tsconfig.json` | TypeScript compiler configuration |
| `frontend/tailwind.config.ts` | Tailwind CSS customization |
| `frontend/.eslintrc.json` | ESLint rules (extends next/core-web-vitals) |
| `frontend/next.config.mjs` | Next.js config (static export enabled) |
| `infrastructure/terraform/environments/dev/main.tf` | AWS infrastructure (VPC, RDS, S3, ECS, CloudFront) |
| `.env.example` | Environment variables template |

---

## API Endpoints

The FastAPI backend exposes:

- `GET /` - Health check (returns `{"status": "healthy"}`)
- `GET /api/v1/health` - Detailed health check with version info

**Future endpoints** (per FRD):
- `/api/v1/auth/*` - Authentication
- `/api/v1/projects/*` - Project CRUD
- `/api/v1/generate/*` - AI film generation
- `/api/v1/jobs/*` - Job status tracking

---

## Testing Guidelines

### Python Tests
```bash
# Run all tests with verbose output
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ -v --cov=src --cov-report=html
```

### Frontend Tests
No test suite is currently configured. Use `npm run lint` for validation.

---

## Infrastructure Notes

- **Terraform version**: >= 1.5.0
- **AWS Provider**: ~> 5.0
- **Target region**: us-east-1 (configurable via `var.aws_region`)
- **Database**: PostgreSQL 15.4 on RDS (db.t3.micro for dev)
- **Container orchestration**: ECS Fargate for backend, GPU-enabled EC2 for workers
- **CDN**: CloudFront for frontend static assets

Terraform is configured with S3 backend for state management. Do not run `terraform apply` without proper AWS credentials and state bucket setup.

---

## Code Style & Conventions

### Python
- Use `black` for formatting
- Use `flake8` for linting  
- Use `mypy` for type checking
- Follow PEP 8 naming conventions
- Use `logging` module via `src/utils/logger.py`

### TypeScript/React
- Use ESLint with Next.js recommended rules
- Use Tailwind CSS for styling (no inline styles)
- Components in `frontend/src/app/components/`
- Use `@/*` path alias for imports (configured in tsconfig.json)

---

## Common Pitfalls to Avoid

1. **Missing httpx**: The `requirements.txt` is missing `httpx`. Always install it separately for testing.
2. **Python version mismatch**: `setup.py` specifies `python_requires=">=3.8"` but the codebase uses Python 3.11+ features.
3. **Test client compatibility**: There may be version conflicts between `starlette`, `httpx`, and `fastapi`. If tests fail with `TypeError`, check package versions.
4. **Frontend build artifacts**: `frontend/out/` and `frontend/.next/` are in `.gitignore` - don't commit them.
5. **Environment variables**: Copy `.env.example` to `.env` before running the backend.

---

## Validation Checklist

Before submitting changes:

- [ ] `pip install -r requirements.txt && pip install httpx` completes without errors
- [ ] `python -m flake8 src/` reports no new errors in changed files
- [ ] `cd frontend && npm install && npm run lint` passes
- [ ] `cd frontend && npm run build` completes successfully
- [ ] No secrets or credentials committed to code
- [ ] Changes follow existing code patterns and conventions

---

## Trust These Instructions

These instructions have been validated by running the actual commands. If something doesn't work as described, verify:
1. You're in the correct directory
2. Dependencies are installed
3. Python/Node.js versions match requirements

Only search for additional information if these instructions are incomplete or produce unexpected errors.
