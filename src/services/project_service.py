"""Project Service - Microservice for project management"""
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class ProjectStatus(str, Enum):
    """Project status enumeration"""
    DRAFT = "draft"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class ProjectService:
    """
    Project Service handles all project-related operations including:
    - Project CRUD operations
    - Project status tracking
    - Project metadata management
    - Version history
    """
    
    def __init__(self, db_session, s3_client):
        self.db = db_session
        self.s3 = s3_client
        
    async def create_project(
        self,
        user_id: str,
        title: str,
        script: str,
        settings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new project
        
        Args:
            user_id: User ID
            title: Project title (max 100 characters)
            script: Script text (max 500 words)
            settings: Optional project settings (voice, music, duration, etc.)
            
        Returns:
            Dict containing project_id, status, and created_at
        """
        project = {
            "user_id": user_id,
            "title": title,
            "script": script,
            "status": ProjectStatus.DRAFT,
            "settings": settings or {},
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        # TODO: Insert into database
        # project_id = await self.db.insert("projects", project)
        
        return {
            "project_id": "uuid-generated",
            "status": "draft",
            "created_at": datetime.now().isoformat()
        }
    
    async def list_projects(
        self,
        user_id: str,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List user's projects with pagination
        
        Args:
            user_id: User ID
            page: Page number (starts at 1)
            page_size: Number of projects per page
            status: Optional filter by status
            
        Returns:
            Dict containing projects list, total_count, and page info
        """
        # TODO: Fetch from database with pagination
        projects = [
            {
                "project_id": "uuid-1",
                "title": "My First Film",
                "status": "completed",
                "thumbnail": "https://s3.amazonaws.com/...",
                "created_at": datetime.now().isoformat()
            }
        ]
        
        return {
            "projects": projects,
            "total_count": 1,
            "page": page,
            "page_size": page_size
        }
    
    async def get_project(self, project_id: str, user_id: str) -> Dict[str, Any]:
        """
        Get project details
        
        Args:
            project_id: Project ID
            user_id: User ID (for authorization)
            
        Returns:
            Dict containing full project details
        """
        # TODO: Fetch from database
        return {
            "project_id": project_id,
            "user_id": user_id,
            "title": "My First Film",
            "script": "Once upon a time...",
            "status": "completed",
            "video_duration": 120,
            "video_url": "https://s3.amazonaws.com/...",
            "thumbnail_url": "https://s3.amazonaws.com/...",
            "subtitle_urls": {
                "en": "https://s3.amazonaws.com/.../subtitles_en.srt",
                "es": "https://s3.amazonaws.com/.../subtitles_es.srt"
            },
            "settings": {
                "voice": "adam",
                "music_genre": "cinematic",
                "duration_minutes": 2
            },
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
    
    async def update_project(
        self,
        project_id: str,
        user_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update project (only editable if status is "draft")
        
        Args:
            project_id: Project ID
            user_id: User ID (for authorization)
            updates: Dict of fields to update
            
        Returns:
            Dict with updated project info
        """
        # TODO: Check if project is in draft status
        # TODO: Update database
        
        return {
            "project_id": project_id,
            "updated_at": datetime.now().isoformat()
        }
    
    async def delete_project(
        self,
        project_id: str,
        user_id: str
    ) -> Dict[str, str]:
        """
        Soft delete a project
        
        Args:
            project_id: Project ID
            user_id: User ID (for authorization)
            
        Returns:
            Dict with status message
        """
        # TODO: Check if job is processing
        # TODO: Mark as deleted in database
        # TODO: Schedule S3 cleanup after 30 days
        
        return {"message": "Project deleted"}
    
    async def update_project_status(
        self,
        project_id: str,
        status: ProjectStatus,
        video_url: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        subtitle_urls: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Update project status (called by AI Job Service)
        
        Args:
            project_id: Project ID
            status: New status
            video_url: S3 URL of final video
            thumbnail_url: S3 URL of thumbnail
            subtitle_urls: Dict of language code to subtitle S3 URL
            
        Returns:
            Dict with updated status
        """
        updates = {
            "status": status,
            "updated_at": datetime.now()
        }
        
        if video_url:
            updates["video_url"] = video_url
        if thumbnail_url:
            updates["thumbnail_url"] = thumbnail_url
        if subtitle_urls:
            updates["subtitle_urls"] = subtitle_urls
            
        # TODO: Update database
        
        return {
            "project_id": project_id,
            "status": status.value,
            "updated_at": datetime.now().isoformat()
        }
