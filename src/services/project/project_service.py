"""
Project Service - Handles CRUD operations for film projects
"""
from typing import Optional, Dict, List
from datetime import datetime
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ProjectService:
    """Service for managing project operations"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    async def create_project(
        self,
        user_id: str,
        title: str,
        script: str,
        description: Optional[str] = None,
        style: str = "cinematic",
        target_duration: int = 60,
        settings: Optional[Dict] = None
    ) -> Dict:
        """
        Create a new film project
        
        Args:
            user_id: ID of the user creating the project
            title: Project title
            script: Film script text
            description: Optional project description
            style: Visual style (cinematic, anime, documentary, etc.)
            target_duration: Target video duration in seconds
            settings: Additional project settings
            
        Returns:
            Created project information
        """
        try:
            project_data = {
                "user_id": user_id,
                "title": title,
                "script": script,
                "description": description,
                "style": style,
                "target_duration": target_duration,
                "status": "draft",
                "settings": settings or {}
            }
            
            project_id = await self.db.insert("projects", project_data)
            
            logger.info(f"Project created: {project_id} by user {user_id}")
            
            project = await self.get_project(project_id)
            return project
            
        except Exception as e:
            logger.error(f"Error creating project: {str(e)}")
            raise
    
    async def get_project(self, project_id: str) -> Optional[Dict]:
        """Get project by ID"""
        try:
            projects = await self.db.query(
                "SELECT * FROM projects WHERE id = %s AND deleted_at IS NULL",
                (project_id,)
            )
            return projects[0] if projects else None
        except Exception as e:
            logger.error(f"Error fetching project: {str(e)}")
            raise
    
    async def get_user_projects(
        self,
        user_id: str,
        status: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[Dict]:
        """
        Get all projects for a user
        
        Args:
            user_id: User ID
            status: Optional status filter
            limit: Number of projects to return
            offset: Pagination offset
            
        Returns:
            List of projects
        """
        try:
            query = """
                SELECT * FROM projects 
                WHERE user_id = %s AND deleted_at IS NULL
            """
            params = [user_id]
            
            if status:
                query += " AND status = %s"
                params.append(status)
            
            query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            projects = await self.db.query(query, tuple(params))
            
            return projects
            
        except Exception as e:
            logger.error(f"Error fetching user projects: {str(e)}")
            raise
    
    async def update_project(
        self,
        project_id: str,
        user_id: str,
        updates: Dict
    ) -> Dict:
        """
        Update project information
        
        Args:
            project_id: Project ID
            user_id: User ID (for authorization)
            updates: Dictionary of fields to update
            
        Returns:
            Updated project information
        """
        try:
            # Verify ownership
            project = await self.get_project(project_id)
            if not project or project["user_id"] != user_id:
                raise ValueError("Project not found or unauthorized")
            
            # Only allow updates if project is in draft status
            if project["status"] not in ["draft", "failed"]:
                raise ValueError("Cannot edit project in current status")
            
            # Allowed fields for update
            allowed_fields = [
                "title", "script", "description", "style",
                "target_duration", "settings"
            ]
            
            # Filter updates
            filtered_updates = {
                k: v for k, v in updates.items() if k in allowed_fields
            }
            
            if not filtered_updates:
                raise ValueError("No valid fields to update")
            
            await self.db.update("projects", {"id": project_id}, filtered_updates)
            
            logger.info(f"Project updated: {project_id}")
            
            return await self.get_project(project_id)
            
        except Exception as e:
            logger.error(f"Error updating project: {str(e)}")
            raise
    
    async def delete_project(self, project_id: str, user_id: str) -> bool:
        """
        Soft delete a project
        
        Args:
            project_id: Project ID
            user_id: User ID (for authorization)
            
        Returns:
            True if successful
        """
        try:
            # Verify ownership
            project = await self.get_project(project_id)
            if not project or project["user_id"] != user_id:
                raise ValueError("Project not found or unauthorized")
            
            # Cannot delete if currently processing
            if project["status"] == "processing":
                raise ValueError("Cannot delete project while processing")
            
            # Soft delete
            await self.db.update(
                "projects",
                {"id": project_id},
                {"deleted_at": datetime.utcnow()}
            )
            
            logger.info(f"Project deleted: {project_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting project: {str(e)}")
            raise
    
    async def update_project_status(
        self,
        project_id: str,
        status: str,
        additional_updates: Optional[Dict] = None
    ) -> Dict:
        """
        Update project status
        
        Args:
            project_id: Project ID
            status: New status
            additional_updates: Additional fields to update
            
        Returns:
            Updated project
        """
        try:
            updates = {"status": status}
            
            if additional_updates:
                updates.update(additional_updates)
            
            # Set completed_at timestamp if status is completed
            if status == "completed":
                updates["completed_at"] = datetime.utcnow()
            
            await self.db.update("projects", {"id": project_id}, updates)
            
            logger.info(f"Project status updated: {project_id} -> {status}")
            
            return await self.get_project(project_id)
            
        except Exception as e:
            logger.error(f"Error updating project status: {str(e)}")
            raise
    
    async def get_project_count(self, user_id: str, status: Optional[str] = None) -> int:
        """Get count of user's projects"""
        try:
            query = "SELECT COUNT(*) FROM projects WHERE user_id = %s AND deleted_at IS NULL"
            params = [user_id]
            
            if status:
                query += " AND status = %s"
                params.append(status)
            
            result = await self.db.query(query, tuple(params))
            return result[0]["count"] if result else 0
            
        except Exception as e:
            logger.error(f"Error counting projects: {str(e)}")
            raise
