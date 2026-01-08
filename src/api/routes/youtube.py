"""YouTube integration service API routes"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.base import get_db
from src.database.models.user import User
from src.database.models.project import Project
from src.database.models.youtube import YouTubeIntegration, UploadStatus
from src.api.schemas.youtube import YouTubeUpload, YouTubeVideo, YouTubeVideoList
from src.utils.auth import get_current_user

router = APIRouter(prefix="/api/youtube", tags=["YouTube"])


@router.post("/upload", response_model=YouTubeVideo, status_code=status.HTTP_201_CREATED)
async def upload_to_youtube(
    upload_data: YouTubeUpload,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload project video to YouTube
    
    Request:
    - project_id: UUID
    - channel_id: string (optional)
    
    Response:
    - video_id: string
    - playlist_id: string
    - upload_status: string
    """
    # Verify project exists and belongs to user
    project = db.query(Project).filter(
        Project.id == upload_data.project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if project.status != "complete":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project video is not ready for upload"
        )
    
    # Create YouTube integration record
    youtube_integration = YouTubeIntegration(
        user_id=current_user.id,
        project_id=upload_data.project_id,
        channel_id=upload_data.channel_id,
        playlist_id=upload_data.playlist_id,
        upload_status=UploadStatus.PENDING
    )
    
    db.add(youtube_integration)
    db.commit()
    db.refresh(youtube_integration)
    
    # TODO: Implement actual YouTube upload logic using YouTube Data API
    # This would involve:
    # 1. OAuth authentication with YouTube
    # 2. Upload video file to YouTube
    # 3. Update youtube_integration with video_id
    # 4. Set upload_status to COMPLETE
    
    return youtube_integration


@router.get("/videos", response_model=YouTubeVideoList)
async def get_youtube_videos(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's YouTube videos
    
    Response:
    - Array of video objects with:
      - video_id: string
      - title: string
      - playlist_id: string
      - status: string
    """
    videos = db.query(YouTubeIntegration).filter(
        YouTubeIntegration.user_id == current_user.id
    ).order_by(YouTubeIntegration.created_at.desc()).all()
    
    return {
        "videos": videos,
        "total": len(videos)
    }


@router.get("/videos/{video_id}", response_model=YouTubeVideo)
async def get_youtube_video(
    video_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get specific YouTube video details
    
    Response:
    - video details
    """
    video = db.query(YouTubeIntegration).filter(
        YouTubeIntegration.id == video_id,
        YouTubeIntegration.user_id == current_user.id
    ).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="YouTube video not found"
        )
    
    return video
