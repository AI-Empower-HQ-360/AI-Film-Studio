"""YouTube integration API schemas"""
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class YouTubeUpload(BaseModel):
    """Schema for YouTube upload request"""
    project_id: UUID
    channel_id: Optional[str] = None
    playlist_id: Optional[str] = None


class YouTubeVideo(BaseModel):
    """Schema for YouTube video response"""
    id: UUID
    project_id: UUID
    video_id: Optional[str]
    channel_id: Optional[str]
    playlist_id: Optional[str]
    upload_status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class YouTubeVideoList(BaseModel):
    """Schema for list of YouTube videos"""
    videos: List[YouTubeVideo]
    total: int
