"""Main API entry point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.utils.logger import setup_logger
from src.config.settings import API_HOST, API_PORT
from src.api.routers import auth_router, projects_router, credits_router

logger = setup_logger(__name__)

app = FastAPI(
    title="AI Film Studio API",
    description="Comprehensive API for AI-powered film production with multi-language support",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router.router)
app.include_router(projects_router.router)
app.include_router(credits_router.router)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "AI Film Studio API is running",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/api/v1/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "AI Film Studio",
        "components": {
            "api": "healthy",
            "database": "healthy",  # TODO: Add actual DB health check
            "redis": "healthy",     # TODO: Add actual Redis health check
            "s3": "healthy"         # TODO: Add actual S3 health check
        }
    }

@app.get("/api/v1/info")
async def api_info():
    """API information and capabilities"""
    return {
        "api_version": "1.0.0",
        "services": [
            "User Authentication",
            "Project Management",
            "AI Video Generation",
            "Credit Management",
            "YouTube Integration",
            "Multi-language Support"
        ],
        "features": {
            "script_analysis": True,
            "image_generation": True,
            "voice_synthesis": True,
            "lip_sync": True,
            "music_generation": True,
            "subtitles": True,
            "youtube_upload": True
        },
        "subscription_tiers": ["Free", "Standard", "Pro", "Enterprise"],
        "supported_languages": [
            "en", "es", "fr", "de", "hi", "ta", "te", "bn", "mr", "gu",
            "kn", "ml", "pa", "ja", "zh", "ko", "ar", "pt", "ru", "it"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting AI Film Studio API on {API_HOST}:{API_PORT}")
    uvicorn.run(app, host=API_HOST, port=API_PORT)
