# Copilot Instructions for AI Film Studio

## Project Overview

AI Film Studio is a cloud-native platform that transforms text scripts into cinematic short films (30-90 seconds) using AI-powered image/video generation and intelligent composition. This is an enterprise-grade application built with AWS cloud architecture, DevOps best practices, and production-ready monitoring.

## Technology Stack

### Backend
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **ORM**: SQLAlchemy with Alembic for migrations
- **Validation**: Pydantic
- **Authentication**: JWT

### Frontend
- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Query

### AI/ML Pipeline
- **Image Generation**: Stable Diffusion XL (SDXL)
- **Video Processing**: FFmpeg, MoviePy
- **ML Libraries**: PyTorch, Transformers

### Infrastructure
- **Cloud**: AWS (VPC, EC2, ECS/EKS, RDS, S3, SQS, CloudFront)
- **IaC**: Terraform
- **Orchestration**: Kubernetes (EKS)
- **Containers**: Docker

## Project Structure

```
ai-film-studio/
├── src/                   # Python backend source code
│   ├── api/               # FastAPI endpoints
│   ├── config/            # Configuration settings
│   ├── services/          # Business logic
│   └── utils/             # Utility functions
├── frontend/              # Next.js frontend application
│   └── src/app/           # React components and pages
├── tests/                 # Python unit tests
├── infrastructure/        # Terraform IaC
│   └── terraform/         # Terraform modules and environments
├── docs/                  # Documentation
├── scripts/               # Utility scripts
└── .github/workflows/     # CI/CD pipelines
```

## Build and Test Commands

### Backend (Python)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the API server
uvicorn src.api.main:app --reload

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=src --cov-report=term-missing

# Linting
flake8 src/ tests/
black --check src/ tests/
mypy src/
```

### Frontend (Next.js)
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Run linting
npm run lint
```

## Coding Conventions

### Python
- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Use `black` for code formatting
- Use `flake8` for linting
- Use `mypy` for type checking
- Write docstrings for all public functions and classes
- Use `async/await` for asynchronous operations in FastAPI

### TypeScript/React
- Use TypeScript for all new code
- Follow ESLint configuration (eslint-config-next)
- Use functional components with hooks
- Use Tailwind CSS for styling (no inline styles)
- Define types in `src/types/` directory

### Testing
- Write tests for all new features
- Use `pytest` for Python testing
- Place tests in the `tests/` directory
- Follow existing test patterns (see `tests/test_api.py`)

### Git Conventions
- Write descriptive commit messages
- Keep commits focused and atomic
- Reference issue numbers in commit messages when applicable

## Important Notes

- The backend API runs on port 8000 by default
- Environment variables are configured via `.env` files (see `.env.example`)
- The frontend uses Next.js 14 with the App Router
- Infrastructure is managed via Terraform in `infrastructure/terraform/`
- CI/CD is configured via GitHub Actions in `.github/workflows/`

## AI/ML Considerations

- GPU resources may be required for running AI models locally
- Model files (`.pth`, `.pt`, `.ckpt`) should not be committed to the repository
- Large files and datasets should be stored in S3, not in the repository
