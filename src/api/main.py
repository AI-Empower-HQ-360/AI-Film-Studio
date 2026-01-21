"""Main API entry point"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from src.utils.logger import setup_logger
from src.config.settings import API_HOST, API_PORT
import os

# Import routers
from src.api.routes import (
    user_router,
    project_router,
    credit_router,
    youtube_router,
    ai_job_router
)

logger = setup_logger(__name__)

# Version constant
VERSION = "0.1.0"

app = FastAPI(
    title="AI Film Studio API",
    description="API for AI-powered film production platform with comprehensive user management, project creation, credit system, YouTube integration, and AI job processing",
    version=VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include routers
app.include_router(user_router)
app.include_router(project_router)
app.include_router(credit_router)
app.include_router(youtube_router)
app.include_router(ai_job_router)

@app.get("/")
async def root():
    """Serve the homepage"""
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": VERSION,
        "service": "AI Film Studio API"
    }

@app.get("/about")
async def about():
    """About endpoint with application information"""
    return {
        "name": "AI Film Studio",
        "version": VERSION,
        "description": "End-to-end AI Film Studio: script → scenes → shots → video → MP4",
        "author": "AI Empower HQ 360",
        "features": [
            "AI-powered script generation",
            "Scene and shot creation",
            "Video production pipeline",
            "MP4 export"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting AI Film Studio API server on {API_HOST}:{API_PORT}")
    uvicorn.run(app, host=API_HOST, port=API_PORT)
