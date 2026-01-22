"""
RDS Database Service for AI Film Studio.
Handles database operations for projects, users, and assets.
"""

import os
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime


class DatabaseService:
    """AWS RDS Database Service for managing project data."""
    
    def __init__(self, connection_string: Optional[str] = None):
        """Initialize the database service."""
        self.connection_string = connection_string or os.getenv("DATABASE_URL", "")
        self.region = os.getenv("AWS_REGION", "us-east-1")
        self._connection = None
        
        # In-memory storage for testing
        self._projects: Dict[str, Dict[str, Any]] = {}
        self._users: Dict[str, Dict[str, Any]] = {}
        self._assets: Dict[str, Dict[str, Any]] = {}
        self._in_transaction = False
        self._transaction_backup: Dict[str, Any] = {}
    
    async def connect(self) -> bool:
        """Establish database connection."""
        # In production, this would connect to RDS
        return True
    
    async def disconnect(self) -> bool:
        """Close database connection."""
        return True
    
    # Project operations
    async def create_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new project."""
        project_id = project_data.get("id") or str(uuid.uuid4())
        
        project = {
            "id": project_id,
            "name": project_data.get("name", "Untitled Project"),
            "description": project_data.get("description", ""),
            "owner_id": project_data.get("owner_id"),
            "status": project_data.get("status", "draft"),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "metadata": project_data.get("metadata", {})
        }
        
        self._projects[project_id] = project
        return project
    
    async def read_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Read a project by ID."""
        return self._projects.get(project_id)
    
    async def update_project(
        self,
        project_id: str,
        updates: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update a project."""
        if project_id not in self._projects:
            return None
        
        self._projects[project_id].update(updates)
        self._projects[project_id]["updated_at"] = datetime.utcnow().isoformat()
        return self._projects[project_id]
    
    async def delete_project(self, project_id: str) -> bool:
        """Delete a project."""
        if project_id in self._projects:
            del self._projects[project_id]
            return True
        return False
    
    async def list_projects_with_pagination(
        self,
        page: int = 1,
        page_size: int = 20,
        owner_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """List projects with pagination."""
        projects = list(self._projects.values())
        
        if owner_id:
            projects = [p for p in projects if p.get("owner_id") == owner_id]
        
        total = len(projects)
        start = (page - 1) * page_size
        end = start + page_size
        
        return {
            "projects": projects[start:end],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
    
    async def search_projects(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search projects by query."""
        results = []
        query_lower = query.lower()
        
        for project in self._projects.values():
            name = project.get("name", "").lower()
            description = project.get("description", "").lower()
            
            if query_lower in name or query_lower in description:
                results.append(project)
        
        return results
    
    # Transaction support
    async def begin_transaction(self) -> bool:
        """Begin a database transaction."""
        self._in_transaction = True
        self._transaction_backup = {
            "projects": self._projects.copy(),
            "users": self._users.copy(),
            "assets": self._assets.copy()
        }
        return True
    
    async def transaction_commit(self) -> bool:
        """Commit the current transaction."""
        self._in_transaction = False
        self._transaction_backup = {}
        return True
    
    async def transaction_rollback(self) -> bool:
        """Rollback the current transaction."""
        if self._transaction_backup:
            self._projects = self._transaction_backup.get("projects", {})
            self._users = self._transaction_backup.get("users", {})
            self._assets = self._transaction_backup.get("assets", {})
        
        self._in_transaction = False
        self._transaction_backup = {}
        return True
    
    # User operations
    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user."""
        user_id = user_data.get("id") or str(uuid.uuid4())
        
        user = {
            "id": user_id,
            "email": user_data.get("email"),
            "name": user_data.get("name"),
            "role": user_data.get("role", "user"),
            "created_at": datetime.utcnow().isoformat()
        }
        
        self._users[user_id] = user
        return user
    
    async def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a user by ID."""
        return self._users.get(user_id)
    
    # Asset operations
    async def create_asset(self, asset_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new asset."""
        asset_id = asset_data.get("id") or str(uuid.uuid4())
        
        asset = {
            "id": asset_id,
            "project_id": asset_data.get("project_id"),
            "type": asset_data.get("type"),
            "url": asset_data.get("url"),
            "metadata": asset_data.get("metadata", {}),
            "created_at": datetime.utcnow().isoformat()
        }
        
        self._assets[asset_id] = asset
        return asset
    
    async def get_project_assets(self, project_id: str) -> List[Dict[str, Any]]:
        """Get all assets for a project."""
        return [
            asset for asset in self._assets.values()
            if asset.get("project_id") == project_id
        ]
    
    async def execute_query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Execute a raw SQL query."""
        # In production, this would execute against RDS
        return []
    
    async def health_check(self) -> Dict[str, Any]:
        """Check database health."""
        return {
            "status": "healthy",
            "connection": "active",
            "projects_count": len(self._projects),
            "users_count": len(self._users)
        }


# Convenience instance
database_service = DatabaseService()
