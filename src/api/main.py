"""Main API entry point"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from datetime import datetime, timedelta
from src.utils.logger import setup_logger
from src.config.settings import API_HOST, API_PORT

logger = setup_logger(__name__)

app = FastAPI(
    title="AI Film Studio API",
    description="API for AI-powered film production tools",
    version="0.1.0"
)

# Mount static files
BASE_DIR = Path(__file__).resolve().parent.parent.parent
static_dir = BASE_DIR / "static"
templates_dir = BASE_DIR / "templates"

if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the home page"""
    index_file = templates_dir / "index.html"
    if index_file.exists():
        return index_file.read_text()
    return "<h1>AI Film Studio API is running</h1>"

@app.get("/api/v1/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "service": "AI Film Studio"
    }

@app.get("/api/v1/data/home")
async def get_home_data():
    """Get data for the home page dashboard"""
    # TODO: Replace with actual database queries when DB is implemented
    # For now, we return sample data for demonstration
    now = datetime.now()
    return {
        "stats": {
            "total_projects": 12,
            "completed_projects": 8,
            "processing_projects": 3,
            "api_status": "online"
        },
        "recent_activity": [
            {
                "title": "Project 'Summer Adventure' completed",
                "description": "Video successfully exported to MP4",
                "timestamp": (now - timedelta(minutes=5)).isoformat()
            },
            {
                "title": "New project 'Documentary 2025' created",
                "description": "Script uploaded and ready for processing",
                "timestamp": (now - timedelta(hours=2)).isoformat()
            },
            {
                "title": "Scene generation completed",
                "description": "15 scenes generated for 'Mystery Night'",
                "timestamp": (now - timedelta(hours=4)).isoformat()
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting API server on {API_HOST}:{API_PORT}")
    uvicorn.run(app, host=API_HOST, port=API_PORT)
