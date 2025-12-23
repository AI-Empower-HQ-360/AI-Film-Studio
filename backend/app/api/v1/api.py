"""API v1 router."""
from fastapi import APIRouter
from .endpoints import auth, projects, jobs

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
