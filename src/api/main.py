"""Main API entry point"""
from fastapi import FastAPI
from src.utils.logger import setup_logger
from src.config.settings import API_HOST, API_PORT

logger = setup_logger(__name__)

app = FastAPI(
    title="AI Film Studio API",
    description="API for AI-powered film production tools",
    version="0.1.0"
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "AI Film Studio API is running", "status": "healthy"}

@app.get("/api/v1/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "service": "AI Film Studio"
    }

@app.get("/api/v1/home")
async def home_page():
    """Serve the main home page experience"""
    return {
        "page": "home",
        "title": "AI Film Studio",
        "subtitle": "Transform scripts into cinematic short films with AI",
        "primary_cta": "Start creating"
    }

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting API server on {API_HOST}:{API_PORT}")
    uvicorn.run(app, host=API_HOST, port=API_PORT)
