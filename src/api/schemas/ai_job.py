"""AI Job API schemas"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class VideoGenerateRequest(BaseModel):
    """Schema for video generation request"""
    project_id: UUID
    script: str
    images: Optional[List[str]] = None
    voice: Optional[str] = "neutral"
    duration: Optional[int] = Field(1, ge=1, le=60)
    music: Optional[str] = None


class AudioGenerateRequest(BaseModel):
    """Schema for audio generation request"""
    project_id: UUID
    text: str
    voice: Optional[str] = "neutral"
    language: Optional[str] = "en"


class LipSyncRequest(BaseModel):
    """Schema for lip sync request"""
    project_id: UUID
    video_url: str
    audio_url: str


class MusicGenerateRequest(BaseModel):
    """Schema for music generation request"""
    project_id: UUID
    prompt: str
    duration: Optional[int] = Field(30, ge=10, le=300)  # 10 seconds to 5 minutes
    style: Optional[str] = "cinematic"


class JobResponse(BaseModel):
    """Schema for job creation response"""
    job_id: UUID
    status: str
    estimated_time: Optional[str] = "3-5 minutes"


class JobStatusResponse(BaseModel):
    """Schema for job status response"""
    job_id: UUID
    project_id: UUID
    status: str
    progress: Optional[int] = 0  # 0-100
    current_step: Optional[str] = None
    result_url: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
