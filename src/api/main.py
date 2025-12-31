"""Main API entry point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.utils.logger import setup_logger
from src.config.settings import API_HOST, API_PORT

# Import routers
from src.api.routes import (
    user_router,
    project_router,
    credit_router,
    youtube_router,
    ai_job_router
)

logger = setup_logger(__name__)

app = FastAPI(
    title="AI Film Studio API",
    description="API for AI-powered film production platform with comprehensive user management, project creation, credit system, YouTube integration, and AI job processing",
    version="1.0.0",
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

# Include routers
app.include_router(user_router)
app.include_router(project_router)
app.include_router(credit_router)
app.include_router(youtube_router)
app.include_router(ai_job_router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Film Studio API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/api/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "AI Film Studio API"
    }

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting AI Film Studio API server on {API_HOST}:{API_PORT}")
    uvicorn.run(app, host=API_HOST, port=API_PORT)
