"""Main API entry point"""
from fastapi import FastAPI
from src.utils.logger import setup_logger
from src.config.settings import API_HOST, API_PORT
from src.api.routes import router as workflow_router

logger = setup_logger(__name__)

app = FastAPI(
    title="AI Film Studio API",
    description="API for AI-powered film production tools - Fully Automated Workflow",
    version="0.1.0"
)

# Include workflow routes
app.include_router(workflow_router)

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

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting API server on {API_HOST}:{API_PORT}")
    uvicorn.run(app, host=API_HOST, port=API_PORT)
