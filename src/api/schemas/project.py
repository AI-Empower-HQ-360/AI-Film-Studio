"""Project API schemas"""
from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    """Schema for creating a project"""
    title: str = Field(..., min_length=1, max_length=255)
    script: Optional[str] = None
    images: Optional[List[str]] = None
    voice: Optional[str] = None
    duration: Optional[int] = Field(None, ge=1, le=60)  # 1-60 minutes
    music: Optional[str] = None


class ProjectUpdate(BaseModel):
    """Schema for updating a project"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    script: Optional[str] = None
    images: Optional[List[str]] = None
    voice: Optional[str] = None
    duration: Optional[int] = Field(None, ge=1, le=60)
    music: Optional[str] = None


class ProjectResponse(BaseModel):
    """Schema for project response"""
    id: UUID
    user_id: UUID
    title: str
    script: Optional[str]
    images: Optional[Any]
    voice: Optional[str]
    duration: Optional[int]
    music: Optional[str]
    status: str
    video_url: Optional[str]
    subtitles_url: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectList(BaseModel):
    """Schema for list of projects"""
    projects: List[ProjectResponse]
    total: int
    page: int
    per_page: int
