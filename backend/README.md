# AI Film Studio Backend

Backend microservices for AI Film Studio.

## Directory Structure

- `app/` - Main application code (formerly src/)
- `services/` - Microservices
  - `user-service/` - User management
  - `project-service/` - Project management
  - `credit-service/` - Credit/billing management
  - `ai-job-service/` - AI job orchestration
  - `youtube-service/` - YouTube integration
  - `admin-service/` - Admin panel
- `common/` - Shared utilities (logger, middleware)
- `queue/` - Redis / BullMQ job queue definitions
- `config/` - Environment config, secrets, JWT keys

## Getting Started

```bash
pip install -r ../requirements.txt
uvicorn app.api.main:app --reload
```
