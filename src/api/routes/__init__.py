"""API routes package initialization"""
from src.api.routes.user import router as user_router
from src.api.routes.project import router as project_router
from src.api.routes.credit import router as credit_router
from src.api.routes.youtube import router as youtube_router
from src.api.routes.ai_job import router as ai_job_router

__all__ = [
    "user_router",
    "project_router",
    "credit_router",
    "youtube_router",
    "ai_job_router"
]
