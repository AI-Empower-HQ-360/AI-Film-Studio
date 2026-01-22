# Copilot Instructions for AI Film Studio

## Project Overview

AI Film Studio transforms text scripts into cinematic short films (30-90 seconds) using a **7-stage AI pipeline**: Script Analysis → Image Generation → Voice Synthesis → Lip-sync Animation → Music/Audio → Podcast Mode → Multilingual Subtitles. The system is **story and culturally context-aware**—the same characters generate different visuals based on script narrative, cultural settings, and character roles.

**Architecture**: Decoupled frontend (Next.js 14) + backend microservices (FastAPI Python) + GPU AI workers + AWS cloud infrastructure (S3, SQS, RDS, ECS/EKS). Deployments span 4 environments: `dev` → `sandbox` → `staging` → `main` (production).

## Critical Architecture Patterns

### AI Service Dependency Chain
All AI services in `src/services/` follow a **hierarchical dependency model**. Image generation MUST happen before video generation, which MUST precede lip-sync animation:
```python
# Example from video_generation.py and lipsync_animation.py
# 1. Script → Character images (using SDXL + cultural context)
# 2. Character images → Video frames (stable-video-diffusion)
# 3. Video + Audio → Lip-synced animation (wav2lip/sadtalker/fomm)
```

**Pattern**: All services inherit from `BaseService` pattern with:
- Pydantic request/response models (e.g., `VideoGenerationRequest`, `LipsyncAnimationResponse`)
- Async methods prefixed with `async def generate_*` or `async def _generate_with_*`
- Job tracking via `self.active_jobs: Dict[str, Any]`
- S3 integration via `self.s3_bucket` attribute

### Frontend Component Architecture
Components in `frontend/src/app/components/` use **multi-step wizard pattern**:
- `FilmCreationWizard.tsx`: 4-step wizard (Script → Settings → Preview → Export)
- State management: Local state + `projectData` partial objects
- Real-time updates via WebSocket connections (planned)
- See lines 1-50 in `FilmCreationWizard.tsx` for step orchestration pattern

### Configuration via Environment
**CRITICAL**: AI models configured via `.env` files, NOT hardcoded. See `.env.example` for:
- Model paths: `WAV2LIP_MODEL_PATH`, `FOMM_MODEL_PATH`, `SADTALKER_MODEL_PATH`
- API keys: `STABILITY_AI_API_KEY`, `ELEVENLABS_API_KEY`, `OPENAI_API_KEY`
- GPU settings: `GPU_DEVICE_ID`, `ENABLE_MIXED_PRECISION`

## Build and Test Commands

### Backend (Python)
```bash
# Install dependencies (includes PyTorch, diffusers, transformers)
pip install -r requirements.txt

# Run FastAPI server (port 8000)
uvicorn src.api.main:app --reload

# Tests
pytest tests/ -v --cov=src --cov-report=term-missing

# Linting (black, flake8, mypy required)
black --check src/ tests/
flake8 src/ tests/
mypy src/
```

### Frontend (Next.js)
```bash
cd frontend

npm install          # Install Next.js 14 + React 18 + Tailwind
npm run dev          # Dev server (port 3000)
npm run build        # Production build
npm run lint         # ESLint (eslint-config-next)
```

### Testing GPU-Dependent Code
**GPU-intensive services** (`video_generation.py`, `lipsync_animation.py`) require:
- CUDA-enabled GPU (g4dn.xlarge or higher for AWS)
- Set `WHISPER_DEVICE=cuda` and `GPU_DEVICE_ID=0` in `.env`
- Mock GPU calls in tests using `pytest` fixtures (see `tests/test_ai_services.py`)

## Project-Specific Conventions

### Python AI Services
1. **Async-first**: All AI generation methods are `async def`, use `await` for I/O
2. **Model config separation**: Import from `src.config.ai_models` (not inline)
3. **Pydantic validation**: All API inputs/outputs use Pydantic models with `Field()` descriptors
4. **Error handling**: Wrap model inference in try/except, return error in response model
5. **S3 patterns**: Generated assets stored in S3 with structure: `{bucket}/{job_id}/{asset_type}/{filename}`

Example from `video_generation.py` (lines 20-42):
```python
class VideoGenerationRequest(BaseModel):
    script: str = Field(..., description="Script or text prompt for video")
    character_images: List[str] = Field(..., description="S3 URLs of character images")
    duration: int = Field(..., ge=1, le=90, description="Video duration in seconds")
```

### TypeScript Frontend
1. **Type definitions**: Define in `frontend/src/types/`, import via `import type { ... }`
2. **Component state**: Use `useState` for local state, NOT Redux/Zustand
3. **File uploads**: Use `useRef<HTMLInputElement>` for file inputs (see `FilmCreationWizard.tsx` line 15)
4. **No inline styles**: All styling via Tailwind CSS classes

### Git Branch Workflow
**CRITICAL**: This project uses 4-branch strategy (see `docs/BRANCHING_STRATEGY.md`):
- `dev`: Active development, auto-deploys to Dev AWS
- `sandbox`: QA testing (Salesforce Sandbox integration)
- `staging`: Pre-production UAT, mirrors production
- `main`: Production only, merge from `staging` after full QA

**Never merge directly to `main`**. Flow: `dev` → `sandbox` → `staging` → `main`

## Documentation Deep Dives

When implementing features, reference these docs for context:
- **Image generation logic**: [`docs/architecture/image-generation-workflow.md`](docs/architecture/image-generation-workflow.md) — explains cultural context integration and character consistency
- **Full workflow**: [`docs/requirements/MASTER-WORKFLOW-ROADMAP.md`](docs/requirements/MASTER-WORKFLOW-ROADMAP.md) — 7-stage AI pipeline dependencies
- **System architecture**: [`docs/architecture/system-design.md`](docs/architecture/system-design.md) — AWS infrastructure, VPC, load balancers
- **Business context**: [`docs/INVESTOR_DEVELOPER_MASTER_BLUEPRINT.md`](docs/INVESTOR_DEVELOPER_MASTER_BLUEPRINT.md) — subscription model, credit system (3 credits = 1 min video)

## Integration Points

### AWS Services
- **S3**: Media storage (`ai-film-studio-assets` bucket), CloudFront CDN distribution
- **SQS**: Async job queue (`ai-film-studio-queue`) for GPU-intensive tasks
- **RDS**: PostgreSQL Multi-AZ for user data, projects, jobs
- **ECS/EKS**: Backend API containers + GPU worker pods

### External APIs
- **Video**: Stability AI (SDXL), RunwayML (Gen-2)
- **Voice**: ElevenLabs, OpenAI TTS, Azure Speech
- **Translation**: Google Translate API, DeepL
- **Subtitles**: Whisper ASR (`large-v3` model)

### Planned Integrations
- **Salesforce CRM**: User tracking, lead scoring (Sandbox → Production sync)
- **YouTube API**: Direct video publishing with metadata

## Common Pitfalls

1. **Model path errors**: Always use environment variables for model paths, not hardcoded strings
2. **Async confusion**: FastAPI routes are `async def`, but don't `await` sync functions
3. **GPU memory**: Monitor via `GPU_MEMORY_THRESHOLD` env var, clear cache between jobs
4. **S3 permissions**: Ensure IAM roles attached to ECS tasks, not hardcoded keys
5. **Type mismatches**: Frontend expects ISO timestamps, backend returns Unix timestamps (normalize in API layer)
