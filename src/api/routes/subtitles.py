"""
Subtitle Routes - API endpoints for subtitle generation and management
"""
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
import uuid
from src.services.subtitle_multilang import (
    SubtitleMultilangService,
    SubtitleGenerationRequest,
    SubtitleTranslationRequest,
    BurnSubtitleRequest,
    SubtitleResponse
)

router = APIRouter(prefix="/api/v1/subtitles", tags=["subtitles"])

# Global service instance
_subtitle_service = SubtitleMultilangService()


@router.post("/generate", status_code=202)
async def generate_subtitles(
    request: Dict[str, Any],
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """
    Generate subtitles from audio using ASR
    
    Request body:
    - audio_url: S3 URL of audio file (required)
    - model_name: ASR model to use (default: whisper-large-v3)
    - source_language: Source language code (default: en)
    - output_format: Subtitle format - srt, vtt, or ass (default: srt)
    - speaker_diarization: Identify different speakers (default: false)
    - max_line_length: Max characters per line (default: 42, range: 20-80)
    - languages: List of languages to generate (optional, for multi-language)
    """
    try:
        job_id = f"subtitle_{uuid.uuid4().hex[:12]}"
        
        # Convert dict to request model
        subtitle_request = SubtitleGenerationRequest(
            audio_url=request.get("audio_url", ""),
            model_name=request.get("model_name", "whisper-large-v3"),
            source_language=request.get("source_language", "en"),
            output_format=request.get("output_format", "srt"),
            speaker_diarization=request.get("speaker_diarization", False),
            max_line_length=request.get("max_line_length", 42)
        )
        
        # Handle multi-language generation
        languages = request.get("languages", [])
        if languages:
            # Store languages for multi-language processing
            subtitle_request_dict = subtitle_request.dict() if hasattr(subtitle_request, 'dict') else {
                "audio_url": subtitle_request.audio_url,
                "model_name": subtitle_request.model_name,
                "source_language": subtitle_request.source_language,
                "output_format": subtitle_request.output_format,
                "speaker_diarization": subtitle_request.speaker_diarization,
                "max_line_length": subtitle_request.max_line_length,
                "languages": languages
            }
            # Start generation in background
            background_tasks.add_task(
                _subtitle_service.generate_subtitles,
                subtitle_request_dict,
                job_id
            )
        else:
            # Start generation in background
            background_tasks.add_task(
                _subtitle_service.generate_subtitles,
                subtitle_request,
                job_id
            )
        
        return {
            "job_id": job_id,
            "status": "processing",
            "message": "Subtitle generation started"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start subtitle generation: {str(e)}")


@router.post("/translate", status_code=202)
async def translate_subtitles(
    request: Dict[str, Any],
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """
    Translate subtitles to multiple languages
    
    Request body:
    - subtitle_url: S3 URL of source subtitle file (required)
    - target_languages: List of target language codes (required)
    - translation_service: Translation service (default: google-translate)
    - preserve_timing: Preserve original timestamps (default: true)
    """
    try:
        job_id = f"translate_{uuid.uuid4().hex[:12]}"
        
        # Convert dict to request model
        translate_request = SubtitleTranslationRequest(
            subtitle_url=request.get("subtitle_url", ""),
            target_languages=request.get("target_languages", []),
            translation_service=request.get("translation_service", "google-translate"),
            preserve_timing=request.get("preserve_timing", True)
        )
        
        # Start translation in background
        background_tasks.add_task(
            _subtitle_service.translate_subtitles,
            translate_request,
            job_id
        )
        
        return {
            "job_id": job_id,
            "status": "processing",
            "message": "Subtitle translation started"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start subtitle translation: {str(e)}")


@router.post("/burn", status_code=202)
async def burn_subtitles(
    request: Dict[str, Any],
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """
    Burn subtitles into video (hardcoded)
    
    Request body:
    - video_url: S3 URL of video file (required)
    - subtitle_url: S3 URL of subtitle file (required)
    - font_name: Font name (default: Arial)
    - font_size: Font size (default: 24, range: 12-72)
    - font_color: Font color (default: white)
    - background_color: Background color (default: black)
    - position: Subtitle position - top, bottom, or center (default: bottom)
    """
    try:
        job_id = f"burn_{uuid.uuid4().hex[:12]}"
        
        # Convert dict to request model
        burn_request = BurnSubtitleRequest(
            video_url=request.get("video_url", ""),
            subtitle_url=request.get("subtitle_url", ""),
            font_name=request.get("font_name", "Arial"),
            font_size=request.get("font_size", 24),
            font_color=request.get("font_color", "white"),
            background_color=request.get("background_color", "black"),
            position=request.get("position", "bottom")
        )
        
        # Start burning in background
        background_tasks.add_task(
            _subtitle_service.burn_subtitles,
            burn_request,
            job_id
        )
        
        return {
            "job_id": job_id,
            "status": "processing",
            "message": "Subtitle burning started"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start subtitle burning: {str(e)}")


@router.get("/status/{job_id}")
async def get_subtitle_status(job_id: str) -> Dict[str, Any]:
    """
    Get the status of a subtitle generation/translation/burning job
    
    Returns:
    - job_id: Job identifier
    - status: Job status (processing, completed, failed, not_found)
    - subtitle_urls: Dictionary mapping language codes to S3 URLs (if completed)
    - video_url: S3 URL of video with burned subtitles (if completed)
    - languages: List of language codes
    - processing_time: Processing time in seconds (if completed)
    - error_message: Error message (if failed)
    """
    status = _subtitle_service.get_job_status(job_id)
    
    if status.get("status") == "not_found":
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {
        "job_id": job_id,
        **status
    }


@router.get("/languages")
async def get_supported_languages(
    model_name: str = "whisper-large-v3"
) -> Dict[str, Any]:
    """
    Get list of supported languages for ASR
    
    Query parameters:
    - model_name: ASR model name (default: whisper-large-v3)
    
    Returns:
    - languages: List of supported language codes
    - model_name: Model name used
    """
    languages = _subtitle_service.get_supported_languages(model_name)
    return {
        "languages": languages,
        "model_name": model_name,
        "count": len(languages)
    }


@router.get("/formats")
async def get_supported_formats() -> Dict[str, Any]:
    """
    Get list of supported subtitle formats
    
    Returns:
    - formats: List of supported formats (srt, vtt, ass)
    """
    formats = _subtitle_service.get_supported_formats()
    return {
        "formats": formats,
        "count": len(formats)
    }


@router.get("/translation-services")
async def get_translation_services() -> Dict[str, Any]:
    """
    Get list of available translation services
    
    Returns:
    - services: List of translation services with provider and supported languages
    """
    services = _subtitle_service.get_translation_services()
    return {
        "services": services,
        "count": len(services)
    }
