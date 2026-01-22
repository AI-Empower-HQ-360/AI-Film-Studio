"""
Video Routes - API endpoints for video generation
"""
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/videos", tags=["videos"])


class VideoGenerateRequest(BaseModel):
    """Request model for video generation"""
    script: str = Field(..., min_length=1)
    character_ids: List[str] = Field(default_factory=list)
    duration: int = Field(default=30, ge=1, le=90)
    style: Optional[str] = None


class VideoResponse(BaseModel):
    """Response model for video"""
    video_id: str
    status: str
    url: Optional[str] = None
    duration: Optional[int] = None
    created_at: datetime


class VideoService:
    """Service class for video operations"""
    
    def __init__(self):
        self.videos: Dict[str, Dict[str, Any]] = {}
        self.jobs: Dict[str, Dict[str, Any]] = {}
    
    async def generate_video(
        self,
        script: str,
        character_ids: List[str] = None,
        duration: int = 30,
        style: Optional[str] = None
    ) -> Dict[str, Any]:
        """Start video generation job"""
        video_id = str(uuid.uuid4())
        job_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        video = {
            "video_id": video_id,
            "job_id": job_id,
            "script": script,
            "character_ids": character_ids or [],
            "duration": duration,
            "style": style,
            "status": "processing",
            "url": None,
            "created_at": now,
        }
        
        self.videos[video_id] = video
        self.jobs[job_id] = {"video_id": video_id, "status": "processing"}
        
        return video
    
    async def get_video(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Get video by ID"""
        return self.videos.get(video_id)
    
    async def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job status"""
        return self.jobs.get(job_id)
    
    async def list_videos(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """List all videos"""
        all_videos = list(self.videos.values())
        return all_videos[skip:skip + limit]
    
    async def cancel_job(self, job_id: str) -> bool:
        """Cancel a video generation job"""
        if job_id in self.jobs:
            self.jobs[job_id]["status"] = "cancelled"
            video_id = self.jobs[job_id].get("video_id")
            if video_id and video_id in self.videos:
                self.videos[video_id]["status"] = "cancelled"
            return True
        return False


# Global service instance
_video_service = VideoService()


def get_video_service() -> VideoService:
    """Dependency injection for video service"""
    return _video_service


@router.post("/generate", response_model=VideoResponse)
async def generate_video(
    request: VideoGenerateRequest,
    service: VideoService = Depends(get_video_service)
):
    """Generate a new video"""
    result = await service.generate_video(
        script=request.script,
        character_ids=request.character_ids,
        duration=request.duration,
        style=request.style
    )
    return result


@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(
    video_id: str,
    service: VideoService = Depends(get_video_service)
):
    """Get a video by ID"""
    video = await service.get_video(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


@router.get("/", response_model=List[VideoResponse])
async def list_videos(
    skip: int = 0,
    limit: int = 100,
    service: VideoService = Depends(get_video_service)
):
    """List all videos"""
    return await service.list_videos(skip=skip, limit=limit)


@router.get("/job/{job_id}")
async def get_job_status(
    job_id: str,
    service: VideoService = Depends(get_video_service)
):
    """Get video generation job status"""
    status = await service.get_job_status(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return status
