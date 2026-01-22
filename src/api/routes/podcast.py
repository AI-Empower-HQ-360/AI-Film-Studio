"""
Podcast Routes - API endpoints for podcast-style video generation
"""
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
import uuid
import asyncio
from src.services.podcast_video import (
    PodcastVideoService,
    PodcastVideoRequest,
    PodcastVideoResponse,
    CharacterConfig,
    DialogueLine,
    PodcastLayout
)

router = APIRouter(prefix="/api/v1/podcast", tags=["podcast"])

# Global service instance
_podcast_service = PodcastVideoService()


@router.post("/generate", status_code=202)
async def generate_podcast_video(
    request: PodcastVideoRequest,
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """
    Generate a podcast-style video with multiple characters
    
    Request body:
    - title: Podcast episode title
    - characters: List of character configurations (2-4 characters)
    - dialogue: List of dialogue lines with character assignments
    - layout: Video layout type (split_screen_50_50, etc.)
    - background_style: Background style (studio, room, etc.)
    - add_lower_thirds: Whether to add character name overlays
    - add_background_music: Whether to add background music
    - duration: Target duration in seconds (optional)
    """
    try:
        job_id = f"podcast_{uuid.uuid4().hex[:12]}"
        
        # Start generation in background
        background_tasks.add_task(
            _podcast_service.generate_podcast_video,
            request,
            job_id
        )
        
        return {
            "job_id": job_id,
            "status": "processing",
            "message": "Podcast video generation started"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start podcast generation: {str(e)}")


@router.get("/status/{job_id}")
async def get_podcast_status(job_id: str) -> Dict[str, Any]:
    """
    Get the status of a podcast video generation job
    
    Returns:
    - status: Job status (processing, completed, failed, not_found)
    - video_url: S3 URL of generated video (if completed)
    - thumbnail_url: S3 URL of thumbnail (if completed)
    - duration: Video duration in seconds (if completed)
    - character_count: Number of characters
    - dialogue_count: Number of dialogue lines
    - processing_time: Processing time in seconds (if completed)
    - error_message: Error message (if failed)
    """
    status = _podcast_service.get_job_status(job_id)
    
    if status.get("status") == "not_found":
        raise HTTPException(status_code=404, detail="Job not found")
    
    # If job is in active_jobs, get full response
    if job_id in _podcast_service.active_jobs:
        job_data = _podcast_service.active_jobs[job_id]
        if job_data.get("status") == "completed":
            # Try to get full response from service
            # For now, return job data
            return {
                "job_id": job_id,
                "status": job_data.get("status", "processing"),
                "character_count": job_data.get("character_count", 0),
                **job_data
            }
    
    return {
        "job_id": job_id,
        "status": status.get("status", "processing"),
        **status
    }


@router.get("/layouts")
async def get_supported_layouts() -> Dict[str, Any]:
    """
    Get list of supported podcast video layouts
    
    Returns:
    - layouts: List of available layouts with descriptions
    """
    layouts = _podcast_service.get_supported_layouts()
    return {
        "layouts": layouts,
        "count": len(layouts)
    }


@router.get("/job/{job_id}/result")
async def get_podcast_result(job_id: str) -> Dict[str, Any]:
    """
    Get the final result of a completed podcast video generation job
    
    Returns:
    - job_id: Job identifier
    - status: Job status
    - video_url: S3 URL of generated video
    - thumbnail_url: S3 URL of thumbnail
    - duration: Video duration in seconds
    - character_count: Number of characters
    - dialogue_count: Number of dialogue lines
    - processing_time: Processing time in seconds
    """
    status = _podcast_service.get_job_status(job_id)
    
    if status.get("status") == "not_found":
        raise HTTPException(status_code=404, detail="Job not found")
    
    if status.get("status") != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Job not completed yet. Current status: {status.get('status')}"
        )
    
    # Return full result
    return {
        "job_id": job_id,
        **status
    }
