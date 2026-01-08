"""Main API entry point"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.utils.logger import setup_logger
from src.config.settings import API_HOST, API_PORT
import os

logger = setup_logger(__name__)

# Version constant
VERSION = "0.1.0"

app = FastAPI(
    title="AI Film Studio API",
    description="API for AI-powered film production tools",
    version=VERSION
)

# Mount static files
static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def root():
    """Serve the homepage"""
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/api/v1/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "version": VERSION,
        "service": "AI Film Studio"
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
    logger.info(f"Starting API server on {API_HOST}:{API_PORT}")
    uvicorn.run(app, host=API_HOST, port=API_PORT)
