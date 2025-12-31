"""Main API entry point"""
from fastapi import FastAPI
from src.utils.logger import setup_logger
from src.config.settings import API_HOST, API_PORT, SALESFORCE_SYNC_ENABLED
from src.api.salesforce_routes import router as salesforce_router

logger = setup_logger(__name__)

app = FastAPI(
    title="AI Film Studio API",
    description="API for AI-powered film production tools with Salesforce CRM integration",
    version="0.1.0"
)

# Include Salesforce routes
if SALESFORCE_SYNC_ENABLED:
    app.include_router(salesforce_router)
    logger.info("Salesforce CRM integration enabled")

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
        "service": "AI Film Studio",
        "salesforce_enabled": SALESFORCE_SYNC_ENABLED
    }

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting API server on {API_HOST}:{API_PORT}")
    uvicorn.run(app, host=API_HOST, port=API_PORT)
