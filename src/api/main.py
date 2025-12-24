"""Main API entry point"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from src.utils.logger import setup_logger
from src.config.settings import API_HOST, API_PORT, BASE_DIR

logger = setup_logger(__name__)

app = FastAPI(
    title="AI Film Studio API",
    description="API for AI-powered film production tools",
    version="0.1.0"
)

# Mount static files
static_dir = BASE_DIR / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Setup templates
templates_dir = BASE_DIR / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# ============================================================================
# PAGE ROUTES
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home/Landing page"""
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/create", response_class=HTMLResponse)
async def create_project_page(request: Request):
    """Script input page (Create Project)"""
    return templates.TemplateResponse("create.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard / User Home page"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/project/{project_id}", response_class=HTMLResponse)
async def project_page(request: Request, project_id: int):
    """Project details page"""
    return templates.TemplateResponse("project.html", {"request": request})

@app.get("/job/{job_id}", response_class=HTMLResponse)
async def job_progress_page(request: Request, job_id: int):
    """Job progress page"""
    return templates.TemplateResponse("job_progress.html", {"request": request})

@app.get("/video/{job_id}", response_class=HTMLResponse)
async def video_preview_page(request: Request, job_id: int):
    """Video preview page"""
    return templates.TemplateResponse("video.html", {"request": request})

@app.get("/credits", response_class=HTMLResponse)
async def credits_page(request: Request):
    """Credits/Billing page"""
    return templates.TemplateResponse("credits.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login/Signup page"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    """Signup page (redirects to login with signup tab)"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    """Settings page"""
    return templates.TemplateResponse("settings.html", {"request": request})

# ============================================================================
# API ROUTES (Mock endpoints for MVP)
# ============================================================================

@app.get("/api/v1/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "service": "AI Film Studio"
    }

# User endpoints
@app.get("/api/v1/user/credits")
async def get_user_credits():
    """Get user credit balance"""
    return {"balance": 150}

@app.get("/api/v1/user/stats")
async def get_user_stats():
    """Get user statistics"""
    return {
        "credits_remaining": 150,
        "projects_today": 2,
        "total_gpu_time": 450,
        "films_this_month": 12,
        "credits_used_this_month": 85,
        "total_duration_this_month": 720,
        "gpu_time_this_month": 1200,
        "daily_limit": 10,
        "films_today": 2,
        "active_jobs": 1,
        "max_concurrent": 3
    }

@app.get("/api/v1/user/profile")
async def get_user_profile():
    """Get user profile"""
    return {
        "name": "Demo User",
        "email": "demo@aifilmstudio.com",
        "bio": "AI Film enthusiast",
        "settings": {
            "notify_completion": True,
            "notify_failures": True,
            "notify_credits": True,
            "notify_newsletter": False
        },
        "webhook_url": ""
    }

@app.get("/api/v1/user/credit-history")
async def get_credit_history():
    """Get credit transaction history"""
    return [
        {
            "date": "2025-12-23T10:30:00Z",
            "type": "purchase",
            "description": "Purchased 100 credits",
            "amount": 100,
            "balance": 150
        },
        {
            "date": "2025-12-22T15:45:00Z",
            "type": "usage",
            "description": "Film generation - Sci-Fi Adventure",
            "amount": -7,
            "balance": 50
        },
        {
            "date": "2025-12-21T09:20:00Z",
            "type": "usage",
            "description": "Film generation - Fantasy Quest",
            "amount": -5,
            "balance": 57
        }
    ]

# Project endpoints
@app.post("/api/v1/projects")
async def create_project():
    """Create a new project"""
    return {
        "id": 1,
        "job_id": 1,
        "status": "queued",
        "message": "Project created successfully"
    }

@app.get("/api/v1/projects")
async def get_projects():
    """Get all user projects"""
    return [
        {
            "id": 1,
            "title": "Sci-Fi Adventure",
            "script": "A lone astronaut walks through a desolate alien landscape...",
            "style": "scifi",
            "duration": 60,
            "status": "completed",
            "created_at": "2025-12-23T10:00:00Z",
            "latest_job_id": 1
        },
        {
            "id": 2,
            "title": "Fantasy Quest",
            "script": "In a medieval kingdom, a young hero discovers a magical sword...",
            "style": "fantasy",
            "duration": 45,
            "status": "running",
            "created_at": "2025-12-24T08:30:00Z",
            "latest_job_id": 2
        }
    ]

@app.get("/api/v1/projects/{project_id}")
async def get_project(project_id: int):
    """Get project details"""
    return {
        "id": project_id,
        "title": "Sci-Fi Adventure",
        "script": "A lone astronaut walks through a desolate alien landscape. The twin suns set behind towering crystalline formations. She discovers an ancient artifact that begins to glow with mysterious energy.",
        "style": "scifi",
        "duration": 60,
        "narrator_voice": "female-soft",
        "music_mood": "mysterious",
        "created_at": "2025-12-23T10:00:00Z",
        "jobs": [
            {
                "id": 1,
                "status": "completed",
                "progress": 100,
                "created_at": "2025-12-23T10:00:00Z",
                "completed_at": "2025-12-23T10:05:30Z"
            }
        ]
    }

# Job endpoints
@app.get("/api/v1/jobs/{job_id}")
async def get_job(job_id: int):
    """Get job details"""
    return {
        "id": job_id,
        "project_id": 1,
        "project_title": "Sci-Fi Adventure",
        "status": "running",
        "progress": 65,
        "current_stage": "rendering_shots",
        "style": "scifi",
        "duration": 60,
        "resolution": "1920x1080",
        "created_at": "2025-12-24T01:00:00Z",
        "video_url": "/static/videos/demo1.mp4",
        "file_size": 15728640,
        "scenes": [
            {
                "description": "Astronaut walking on alien landscape",
                "status": "completed",
                "shots": [
                    {"status": "completed"},
                    {"status": "completed"}
                ]
            },
            {
                "description": "Twin suns setting behind crystals",
                "status": "running",
                "shots": [
                    {"status": "completed"},
                    {"status": "running"}
                ]
            },
            {
                "description": "Discovery of glowing artifact",
                "status": "queued",
                "shots": [
                    {"status": "queued"},
                    {"status": "queued"}
                ]
            }
        ]
    }

@app.post("/api/v1/jobs/{job_id}/cancel")
async def cancel_job(job_id: int):
    """Cancel a job"""
    return {"message": "Job cancelled successfully"}

@app.get("/api/v1/jobs/{job_id}/download")
async def get_download_url(job_id: int):
    """Get signed download URL"""
    return {"download_url": f"/static/videos/demo1.mp4"}

# Auth endpoints
@app.post("/api/v1/auth/login")
async def login():
    """User login"""
    return {
        "access_token": "demo_token_12345",
        "token_type": "bearer"
    }

@app.post("/api/v1/auth/signup")
async def signup():
    """User signup"""
    return {
        "access_token": "demo_token_12345",
        "token_type": "bearer"
    }

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting API server on {API_HOST}:{API_PORT}")
    uvicorn.run(app, host=API_HOST, port=API_PORT)
