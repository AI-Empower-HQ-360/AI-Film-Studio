"""Main API entry point"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from src.utils.logger import setup_logger
from src.config.settings import API_HOST, API_PORT

logger = setup_logger(__name__)

app = FastAPI(
    title="AI Film Studio API",
    description="API for AI-powered film production tools",
    version="0.1.0"
)

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Mount static files
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

@app.get("/")
async def root():
    """Serve the home page"""
    return FileResponse(str(BASE_DIR / "templates" / "index.html"))

@app.get("/dashboard.html")
async def dashboard():
    """Serve the dashboard page"""
    return FileResponse(str(BASE_DIR / "templates" / "dashboard.html"))

@app.get("/script.html")
async def script():
    """Serve the script generator page"""
    return FileResponse(str(BASE_DIR / "templates" / "script.html"))

@app.get("/scenes.html")
async def scenes():
    """Serve the scenes manager page"""
    return FileResponse(str(BASE_DIR / "templates" / "scenes.html"))

@app.get("/render.html")
async def render():
    """Serve the video renderer page"""
    return FileResponse(str(BASE_DIR / "templates" / "render.html"))

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
