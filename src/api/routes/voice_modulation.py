"""
Voice Modulation Routes - API endpoints for voice synthesis with age and gender modulation
"""
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
import uuid
from src.engines.voice_modulation_engine import (
    VoiceModulationEngine,
    VoiceModulationRequest,
    VoiceAgeGroup,
    VoiceGender
)

router = APIRouter(prefix="/api/v1/voice-modulation", tags=["voice-modulation"])

# Global service instance
_voice_modulation_engine = VoiceModulationEngine()


@router.post("/synthesize", status_code=202)
async def synthesize_voice(
    request: Dict[str, Any],
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """
    Synthesize voice with age and gender modulation
    
    Request body:
    - text: Text to synthesize (required)
    - age_group: Age group (0-3, 4-8, 8-12, 13-19, 20-21, 22-35, 35-50, 50+)
    - gender: Gender (boy, girl, man, woman, child)
    - pitch: Pitch modulation (0.0-2.0, optional)
    - speed: Speed modulation (0.5-2.0, optional)
    - volume: Volume (0.0-1.0, optional)
    - emotion: Emotion (neutral, happy, sad, angry, excited, calm, optional)
    - accent: Accent/regional variation (optional)
    - language: Language code (default: en)
    - voice_model_id: Specific voice model ID (optional)
    """
    try:
        job_id = f"voice_{uuid.uuid4().hex[:12]}"
        
        # Convert dict to request model
        voice_request = VoiceModulationRequest(
            text=request.get("text", ""),
            age_group=request.get("age_group", ""),
            gender=request.get("gender", ""),
            pitch=request.get("pitch"),
            speed=request.get("speed"),
            volume=request.get("volume"),
            emotion=request.get("emotion", "neutral"),
            accent=request.get("accent"),
            language=request.get("language", "en"),
            voice_model_id=request.get("voice_model_id"),
            metadata=request.get("metadata", {})
        )
        
        # Start synthesis in background
        background_tasks.add_task(
            _voice_modulation_engine.synthesize_voice,
            voice_request,
            job_id
        )
        
        return {
            "job_id": job_id,
            "status": "processing",
            "message": "Voice synthesis started"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start voice synthesis: {str(e)}")


@router.get("/status/{job_id}")
async def get_voice_status(job_id: str) -> Dict[str, Any]:
    """
    Get the status of a voice synthesis job
    
    Returns:
    - job_id: Job identifier
    - status: Job status (processing, completed, failed, not_found)
    - voice_id: Voice ID (if completed)
    - audio_url: Audio URL (if completed)
    - duration: Audio duration in seconds (if completed)
    - characteristics: Voice characteristics (if completed)
    - error_message: Error message (if failed)
    """
    status = _voice_modulation_engine.get_job_status(job_id)
    
    if status.get("status") == "not_found":
        raise HTTPException(status_code=404, detail="Job not found")
    
    result = status.get("result")
    if result:
        return {
            "job_id": job_id,
            "status": status.get("status"),
            "voice_id": result.voice_id,
            "audio_url": result.audio_url,
            "duration": result.duration,
            "age_group": result.age_group,
            "gender": result.gender,
            "characteristics": result.characteristics,
            "processing_time": status.get("processing_time")
        }
    
    return {
        "job_id": job_id,
        "status": status.get("status"),
        **status
    }


@router.get("/options/age-groups")
async def get_age_groups() -> Dict[str, Any]:
    """Get list of supported age groups for voice"""
    age_groups = _voice_modulation_engine.get_supported_age_groups()
    return {"age_groups": age_groups, "count": len(age_groups)}


@router.get("/options/genders")
async def get_genders() -> Dict[str, Any]:
    """Get list of supported genders for voice"""
    genders = _voice_modulation_engine.get_supported_genders()
    return {"genders": genders, "count": len(genders)}


@router.get("/options/voice-models")
async def get_voice_models() -> Dict[str, Any]:
    """Get all available voice models"""
    models = _voice_modulation_engine.get_voice_models()
    return {"voice_models": models, "count": len(models)}


@router.get("/voices/{voice_id}")
async def get_voice(voice_id: str) -> Dict[str, Any]:
    """Get voice result by ID"""
    voice = _voice_modulation_engine.get_voice(voice_id)
    if not voice:
        raise HTTPException(status_code=404, detail="Voice not found")
    
    return {
        "voice_id": voice.voice_id,
        "job_id": voice.job_id,
        "audio_url": voice.audio_url,
        "duration": voice.duration,
        "age_group": voice.age_group,
        "gender": voice.gender,
        "characteristics": voice.characteristics,
        "created_at": voice.created_at.isoformat()
    }
