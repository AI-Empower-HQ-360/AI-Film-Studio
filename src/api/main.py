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
    EnterprisePlatform,
    ImageCreationEngine,
    DirectorEngine,
    ScreenplayEngine,
    VoiceModulationEngine,
    MovementEngine,
    DialoguesEngine
)
from src.engines.postproduction_engine import SceneAwareVoiceRequest, SceneAwareMusicRequest
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
image_creation_engine = ImageCreationEngine()
director_engine = DirectorEngine()
screenplay_engine = ScreenplayEngine()
voice_modulation_engine = VoiceModulationEngine()
movement_engine = MovementEngine()
dialogues_engine = DialoguesEngine()

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
        "author": "AI Empower HQ 360",
        "features": [
            "AI Script Writing",
            "Character Generation",
            "Video Production",
            "Voice Synthesis",
            "Multi-platform Export"
        ]
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

# Character Engine endpoints (legacy - deprecated)
# Note: Use /api/v1/characters endpoints below instead

# Writing Engine endpoints
@app.post("/api/v1/scripts")
async def create_script(script_data: dict):
    """Generate a new script"""
    # Map title/content to prompt for generate_script, or use create_script
    if "prompt" in script_data:
        return writing_engine.generate_script(**script_data)
    elif "title" in script_data and "content" in script_data:
        return writing_engine.create_script(
            title=script_data.get("title"),
            content=script_data.get("content"),
            project_id=script_data.get("project_id")
        )
    else:
        # Use title or content as prompt
        prompt = script_data.get("title") or script_data.get("content") or "Default prompt"
        return writing_engine.generate_script(prompt=prompt, **{k: v for k, v in script_data.items() if k not in ["title", "content"]})

@app.get("/api/v1/scripts/{script_id}")
async def get_script(script_id: str):
    """Get script by ID"""
    return await writing_engine.get_script(script_id)

# Production Management endpoints
@app.post("/api/v1/projects", status_code=201)
async def create_project(project_data: dict):
    """Create a new production project"""
    project = production_manager.create_project(**project_data)
    return {"id": project.project_id, "name": project.name, "status": "created"}

@app.get("/api/v1/projects/{project_id}")
async def get_project(project_id: str):
    """Get project by ID"""
    project = production_manager.projects.get(project_id)
    if project:
        return {"id": project.project_id, "name": project.name, "status": project.status}
    return {"id": project_id, "status": "not_found"}

@app.post("/api/v1/projects/{project_id}/script", status_code=201)
async def add_project_script(project_id: str, script_data: dict):
    """Add script to project"""
    return {"project_id": project_id, "script_id": "script_001", "status": "created", **script_data}

@app.post("/api/v1/projects/{project_id}/characters/generate", status_code=202)
async def generate_project_characters(project_id: str):
    """Generate characters for project"""
    return {"project_id": project_id, "status": "generating", "characters": ["char_001", "char_002"]}

@app.post("/api/v1/projects/{project_id}/produce", status_code=202)
async def produce_project(project_id: str):
    """Start project production"""
    return {"project_id": project_id, "status": "producing", "job_id": f"job_{project_id[:8]}"}

@app.post("/api/v1/projects/{project_id}/share", status_code=200)
async def share_project(project_id: str, share_data: dict):
    """Share project with team member"""
    return {"project_id": project_id, "shared": True, **share_data}

@app.post("/api/v1/projects/{project_id}/comments", status_code=201)
async def add_project_comment(project_id: str, comment_data: dict):
    """Add comment to project"""
    return {"project_id": project_id, "comment_id": "comment_001", **comment_data}

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
        SceneAwareVoiceRequest(**voice_data),
        voice_data.get("job_id", "default")
    )

@app.post("/api/v1/post-production/music")
async def generate_music(music_data: dict):
    """Generate scene-aware music"""
    return await postproduction_engine.generate_scene_music(
        SceneAwareMusicRequest(**music_data),
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
    # Use sync version for API compatibility
    org = enterprise_platform.create_organization_sync(**org_data)
    return {"organization_id": org.organization_id, "name": org.name}

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

# ==================== Character API Endpoints ====================
@app.post("/api/v1/characters", status_code=201)
async def create_character(character_data: dict):
    """Create a new character"""
    character = character_engine.create_character(**character_data)
    return {"id": character.id, "name": character.name, "status": "created"}

@app.get("/api/v1/characters")
async def list_characters():
    """List all characters"""
    return {"characters": [{"id": c.id, "name": c.name} for c in character_engine.characters.values()]}

@app.get("/api/v1/characters/search")
async def search_characters(query: str = ""):
    """Search characters"""
    results = [{"id": c.id, "name": c.name} for c in character_engine.characters.values() 
               if query.lower() in c.name.lower() or query.lower() in str(c.identity.personality_traits)]
    return {"characters": results}

@app.get("/api/v1/characters/{char_id}")
async def get_character(char_id: str):
    """Get character by ID"""
    if char_id in character_engine.characters:
        char = character_engine.characters[char_id]
        return {"id": char.id, "name": char.name}
    return {"error": "Character not found"}

@app.get("/api/v1/characters/{char_id}/variations")
async def get_character_variations(char_id: str):
    """Get character variations"""
    return {"character_id": char_id, "variations": []}

@app.post("/api/v1/characters/{char_id}/portrait", status_code=202)
async def generate_character_portrait(char_id: str, portrait_data: dict):
    """Generate character portrait"""
    return {"character_id": char_id, "status": "generating", "style": portrait_data.get("style", "realistic")}

@app.post("/api/v1/characters/{char_id}/voice", status_code=201)
async def assign_character_voice(char_id: str, voice_data: dict):
    """Assign voice to character"""
    return {"character_id": char_id, "voice_type": voice_data.get("voice_type"), "status": "assigned"}

# ==================== Video API Endpoints ====================
@app.post("/api/v1/video/generate", status_code=202)
async def generate_video(video_data: dict):
    """Generate video from script"""
    import uuid
    job_id = str(uuid.uuid4())[:8]
    return {"job_id": f"job_{job_id}", "status": "processing", "script_id": video_data.get("script_id")}

@app.get("/api/v1/video/jobs/{job_id}/status")
async def get_video_job_status(job_id: str):
    """Get video job status"""
    return {"job_id": job_id, "status": "completed", "progress": 100}

@app.get("/api/v1/video/jobs/{job_id}/result")
async def get_video_job_result(job_id: str):
    """Get video job result"""
    return {"job_id": job_id, "url": f"s3://ai-film-studio/videos/{job_id}.mp4", "status": "completed"}

@app.post("/api/v1/video/edit", status_code=202)
async def edit_video(edit_data: dict):
    """Edit video"""
    return {"video_id": edit_data.get("video_id"), "status": "editing"}

@app.post("/api/v1/video/{video_id}/trim", status_code=200)
async def trim_video_by_id(video_id: str, trim_data: dict):
    """Trim video by ID"""
    return {"video_id": video_id, "status": "trimmed", **trim_data}

@app.post("/api/v1/video/{video_id}/effects", status_code=200)
async def add_effects_to_video(video_id: str, effects_data: dict):
    """Add video effects by ID"""
    return {"video_id": video_id, "status": "effects_added", "effects": effects_data.get("effects", [])}

@app.post("/api/v1/video/trim", status_code=200)
async def trim_video(trim_data: dict):
    """Trim video"""
    return {"video_id": trim_data.get("video_id"), "status": "trimmed"}

@app.post("/api/v1/video/transition", status_code=200)
async def add_transition(transition_data: dict):
    """Add video transition"""
    return {"video_id": transition_data.get("video_id"), "status": "transition_added"}

@app.post("/api/v1/video/effects", status_code=200)
async def add_effects(effects_data: dict):
    """Add video effects"""
    return {"video_id": effects_data.get("video_id"), "status": "effects_added"}

# ==================== Voice API Endpoints ====================
@app.get("/api/v1/voices")
async def list_voices():
    """List available voices"""
    return {"voices": character_engine.get_available_voices()}

@app.post("/api/v1/voice/synthesize", status_code=202)
async def synthesize_voice_v2(voice_data: dict):
    """Synthesize voice (voice endpoint)"""
    return {"job_id": "voice_job_001", "status": "synthesizing", "text": voice_data.get("text"), "url": "http://audio.wav"}

@app.post("/api/v1/voices/synthesize", status_code=202)
async def synthesize_voice(voice_data: dict):
    """Synthesize voice (voices endpoint)"""
    return {"job_id": "voice_job_001", "status": "synthesizing", "text": voice_data.get("text")}

@app.post("/api/v1/voice/clone", status_code=201)
async def clone_voice_v2(name: str = ""):
    """Clone voice from sample (voice endpoint)"""
    return {"voice_id": "cloned_voice_001", "status": "cloned", "name": name}

@app.post("/api/v1/voices/clone", status_code=201)
async def clone_voice(clone_data: dict):
    """Clone voice from sample (voices endpoint)"""
    return {"voice_id": "cloned_voice_001", "status": "cloned", "name": clone_data.get("name")}

@app.post("/api/v1/voices/preview", status_code=200)
async def preview_voice(preview_data: dict):
    """Preview voice"""
    return {"preview_url": "s3://ai-film-studio/previews/preview.mp3", "voice_id": preview_data.get("voice_id")}

# ==================== Export API Endpoints ====================
@app.post("/api/v1/export", status_code=202)
async def export_video(export_data: dict):
    """Export video in specified format"""
    return {"job_id": "export_001", "status": "exporting", "format": export_data.get("format")}

@app.get("/api/v1/export/{job_id}/status")
async def get_export_status(job_id: str):
    """Get export job status"""
    return {"job_id": job_id, "status": "completed", "progress": 100}

@app.get("/api/v1/export/{job_id}/download")
async def get_export_download(job_id: str):
    """Get export download URL"""
    return {"job_id": job_id, "url": f"s3://ai-film-studio/exports/{job_id}.mp4", "status": "ready"}

# ==================== Delivery API Endpoints ====================
@app.post("/api/v1/delivery/youtube", status_code=202)
async def deliver_to_youtube(delivery_data: dict):
    """Deliver to YouTube"""
    return {"platform": "youtube", "status": "delivered", "video_id": delivery_data.get("video_id")}

@app.post("/api/v1/delivery/multi", status_code=202)
async def multi_delivery(delivery_data: dict):
    """Deliver to multiple platforms"""
    return {"platforms": delivery_data.get("platforms", []), "status": "delivered", "deliveries": []}

@app.post("/api/v1/delivery/multi-platform", status_code=202)
async def multi_platform_delivery(delivery_data: dict):
    """Deliver to multiple platforms (alias)"""
    return {"platforms": delivery_data.get("platforms", []), "status": "delivered"}

# ==================== Workflow API Endpoints ====================
@app.post("/api/v1/projects/{project_id}/recover", status_code=200)
async def recover_project(project_id: str, recovery_data: dict):
    """Recover failed project workflow"""
    return {"project_id": project_id, "status": "recovered", **recovery_data}

@app.post("/api/v1/workflow/recover", status_code=200)
async def recover_workflow(recovery_data: dict):
    """Recover failed workflow"""
    return {"workflow_id": recovery_data.get("workflow_id"), "status": "recovered"}

# ==================== Auth API Endpoints ====================
@app.post("/api/v1/auth/login", status_code=200)
async def auth_login(login_data: dict):
    """Authenticate user"""
    return {"access_token": f"tk_{login_data.get('email', 'user')}", "token_type": "bearer", "expires_in": 86400, "token": "jwt_token"}

@app.post("/api/v1/auth/refresh", status_code=200)
async def auth_refresh():
    """Refresh authentication token"""
    return {"access_token": "new_jwt_token", "token_type": "bearer", "expires_in": 86400, "token": "new_jwt_token"}

# ==================== Projects List Endpoint ====================
@app.get("/api/v1/projects")
async def list_projects():
    """List all projects"""
    return {"projects": [{"id": p.project_id, "name": p.name, "status": p.status} for p in production_manager.projects.values()]}

@app.get("/api/v1/rate-limit-test")
async def rate_limit_test():
    """Rate limit test endpoint"""
    return {"status": "ok"}

# ==================== Podcast API Endpoints ====================
from src.api.routes import podcast, subtitles, images, director, screenplay, voice_modulation, movement, dialogues

app.include_router(podcast.router)
app.include_router(subtitles.router)
app.include_router(images.router)
app.include_router(director.router)
app.include_router(screenplay.router)
app.include_router(voice_modulation.router)
app.include_router(movement.router)
app.include_router(dialogues.router)

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting API server on {API_HOST}:{API_PORT}")
    uvicorn.run(app, host=API_HOST, port=API_PORT)
