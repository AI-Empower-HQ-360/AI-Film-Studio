from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class JobBase(BaseModel):
    """Base job schema"""
    project_id: str
    config: Optional[Dict[str, Any]] = None


class JobCreate(JobBase):
    """Job creation schema"""
    pass


class JobUpdate(BaseModel):
    """Job update schema"""
    status: Optional[str] = None
    progress: Optional[int] = None
    error_message: Optional[str] = None


class JobResponse(JobBase):
    """Job response schema"""
    id: str
    user_id: str
    status: str
    progress: int
    error_message: Optional[str] = None
    output_video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class JobStatusUpdate(BaseModel):
    """Job status update schema"""
    status: str
    progress: Optional[int] = None
    error_message: Optional[str] = None
