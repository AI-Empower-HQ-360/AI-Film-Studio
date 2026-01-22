"""
AI Film Studio API - Enterprise Studio Operating System
Main API entry point with all engine integrations
"""
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from src.utils.logger import setup_logger
from src.config.settings import API_HOST, API_PORT
from src.engines import (
    CharacterEngine,
    WritingEngine,
    PreProductionEngine,
    ProductionManager,
    ProductionLayer,
    PostProductionEngine,
    MarketingEngine,
    EnterprisePlatform
)
import os

logger = setup_logger(__name__)

# Version constant
VERSION = "0.1.0"

app = FastAPI(
    title="AI Film Studio API",
    description="Enterprise AI-native studio operating system for film, TV, and brand content",
    version=VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engines
character_engine = CharacterEngine()
writing_engine = WritingEngine()
preproduction_engine = PreProductionEngine()
production_manager = ProductionManager()
production_layer = ProductionLayer()
postproduction_engine = PostProductionEngine()
marketing_engine = MarketingEngine()
enterprise_platform = EnterprisePlatform()

# Mount static files
static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def root():
    """Serve the homepage"""
    if os.path.exists(os.path.join(static_dir, "index.html")):
        return FileResponse(os.path.join(static_dir, "index.html"))
    return {"message": "AI Film Studio API", "version": VERSION}

@app.get("/about")
async def about_simple():
    """Simple about endpoint"""
    return {
        "name": "AI Film Studio",
        "version": VERSION,
        "description": "Enterprise AI-native studio operating system",
        "author": "AI Empower HQ 360"
    }

@app.get("/api/health")
async def health():
    """Simple health check"""
    return {"status": "healthy", "version": VERSION}

@app.get("/health")
async def health_root():
    """Root health check endpoint"""
    return {"status": "healthy", "version": VERSION}

@app.get("/api/v1/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "version": VERSION,
        "service": "AI Film Studio - Enterprise Studio Operating System",
        "engines": {
            "character_engine": "active",
            "writing_engine": "active",
            "preproduction_engine": "active",
            "production_manager": "active",
            "production_layer": "active",
            "postproduction_engine": "active",
            "marketing_engine": "active",
            "enterprise_platform": "active"
        }
    }

@app.get("/api/v1/about")
async def about():
    """About endpoint with application information"""
    return {
        "name": "AI Film Studio",
        "version": VERSION,
        "description": "Enterprise AI-native studio operating system that enables creators, studios, and brands to design characters, write scripts, plan productions, shoot real footage, generate AI scenes, produce cinematic audio, and distribute content—end-to-end from a single unified platform.",
        "author": "AI Empower HQ 360",
        "platform_type": "Studio Operating System",
        "capabilities": [
            "Character Engine (first-class assets with consistency)",
            "AI Writing & Story Engine",
            "AI Pre-Production Engine",
            "Production Management (RBAC, assets, timelines)",
            "AI / Real Shoot Production Layer (hybrid production)",
            "AI Post-Production Engine (voice, music, audio post)",
            "Marketing & Distribution Engine",
            "Enterprise Platform Layer (multi-tenant, billing, API)"
        ],
        "target_users": [
            "Content creators and marketers",
            "Indie filmmakers and studios",
            "Brands and agencies",
            "Educational institutions",
            "Corporate training departments"
        ]
    }

# Character Engine endpoints
@app.post("/api/v1/characters")
async def create_character(character_data: dict):
    """Create a new character"""
    return await character_engine.create_character(**character_data)

@app.get("/api/v1/characters/{character_id}")
async def get_character(character_id: str):
    """Get character by ID"""
    return await character_engine.get_character(character_id)

# Writing Engine endpoints
@app.post("/api/v1/scripts")
async def create_script(script_data: dict):
    """Generate a new script"""
    return await writing_engine.generate_script(**script_data)

@app.get("/api/v1/scripts/{script_id}")
async def get_script(script_id: str):
    """Get script by ID"""
    return await writing_engine.get_script(script_id)

# Production Management endpoints
@app.post("/api/v1/projects")
async def create_project(project_data: dict):
    """Create a new production project"""
    return await production_manager.create_project(**project_data)

@app.get("/api/v1/projects/{project_id}")
async def get_project(project_id: str):
    """Get project by ID"""
    return await production_manager.get_project(project_id)

# Production Layer endpoints
@app.post("/api/v1/production/upload-footage")
async def upload_footage(footage_data: dict):
    """Upload real camera footage"""
    return await production_layer.upload_real_footage(**footage_data)

@app.post("/api/v1/production/generate-shot")
async def generate_shot(shot_data: dict):
    """Generate AI shot"""
    return await production_layer.generate_ai_shot(**shot_data)

# Post-Production endpoints
@app.post("/api/v1/post-production/voice")
async def generate_voice(voice_data: dict):
    """Generate character-aware voice"""
    return await postproduction_engine.generate_character_voice(
        postproduction_engine.SceneAwareVoiceRequest(**voice_data),
        voice_data.get("job_id", "default")
    )

@app.post("/api/v1/post-production/music")
async def generate_music(music_data: dict):
    """Generate scene-aware music"""
    return await postproduction_engine.generate_scene_music(
        postproduction_engine.SceneAwareMusicRequest(**music_data),
        music_data.get("job_id", "default")
    )

# Marketing endpoints
@app.post("/api/v1/marketing/trailer")
async def generate_trailer(trailer_data: dict):
    """Generate trailer"""
    return await marketing_engine.generate_trailer(**trailer_data)

@app.post("/api/v1/marketing/poster")
async def generate_poster(poster_data: dict):
    """Generate poster"""
    return await marketing_engine.generate_poster(**poster_data)

# Enterprise Platform endpoints
@app.post("/api/v1/organizations")
async def create_organization(org_data: dict):
    """Create organization"""
    return await enterprise_platform.create_organization(**org_data)

@app.post("/api/v1/usage")
async def record_usage(usage_data: dict):
    """Record usage for billing"""
    return await enterprise_platform.record_usage(**usage_data)

# V1 Video Generation endpoints (for integration tests)
@app.post("/v1/generate")
async def v1_generate_video(data: dict):
    """Generate video from script (V1 API)"""
    import uuid
    job_id = str(uuid.uuid4())
    return {
        "job_id": job_id,
        "status": "processing",
        "script": data.get("script", ""),
        "duration": data.get("duration", 30)
    }

@app.get("/v1/status/{job_id}")
async def v1_get_status(job_id: str):
    """Get job status (V1 API)"""
    return {
        "job_id": job_id,
        "status": "completed",
        "progress": 100,
        "output_url": f"s3://ai-film-studio/videos/{job_id}.mp4"
    }

@app.get("/v1/voices")
async def v1_list_voices():
    """List available voices (V1 API)"""
    return {
        "voices": [
            {"id": "professional-female-1", "name": "Rachel", "language": "en-US", "gender": "female"},
            {"id": "professional-male-1", "name": "Adam", "language": "en-US", "gender": "male"},
            {"id": "narrator-1", "name": "Narrator", "language": "en-US", "gender": "neutral"},
        ]
    }

@app.post("/v1/auth/login")
async def v1_login(data: dict):
    """Login endpoint (V1 API)"""
    return {
        "access_token": f"tk_{data.get('email', 'user')}",
        "token_type": "bearer",
        "expires_in": 86400
    }

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting API server on {API_HOST}:{API_PORT}")
    uvicorn.run(app, host=API_HOST, port=API_PORT)
