"""
Project Routes - API endpoints for project management
"""
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/projects", tags=["projects"])


class ProjectCreate(BaseModel):
    """Request model for creating a project"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    organization_id: Optional[str] = None


class ProjectResponse(BaseModel):
    """Response model for project"""
    project_id: str
    name: str
    description: Optional[str] = None
    status: str = "draft"
    created_at: datetime
    updated_at: datetime


class ProjectService:
    """Service class for project operations"""
    
    def __init__(self):
        self.projects: Dict[str, Dict[str, Any]] = {}
    
    async def create_project(
        self, 
        name: str, 
        description: Optional[str] = None,
        organization_id: Optional[str] = None,
        created_by: str = "system"
    ) -> Dict[str, Any]:
        """Create a new project"""
        project_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        project = {
            "project_id": project_id,
            "name": name,
            "description": description,
            "organization_id": organization_id,
            "status": "draft",
            "created_by": created_by,
            "created_at": now,
            "updated_at": now,
        }
        
        self.projects[project_id] = project
        return project
    
    async def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get project by ID"""
        return self.projects.get(project_id)
    
    async def list_projects(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """List all projects with pagination"""
        all_projects = list(self.projects.values())
        return all_projects[skip:skip + limit]
    
    async def update_project(
        self, 
        project_id: str, 
        updates: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update a project"""
        if project_id not in self.projects:
            return None
        
        self.projects[project_id].update(updates)
        self.projects[project_id]["updated_at"] = datetime.utcnow()
        return self.projects[project_id]
    
    async def delete_project(self, project_id: str) -> bool:
        """Delete a project"""
        if project_id in self.projects:
            del self.projects[project_id]
            return True
        return False


# Global service instance
_project_service = ProjectService()


def get_project_service() -> ProjectService:
    """Dependency injection for project service"""
    return _project_service


@router.post("/", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    service: ProjectService = Depends(get_project_service)
):
    """Create a new project"""
    result = await service.create_project(
        name=project.name,
        description=project.description,
        organization_id=project.organization_id
    )
    return result


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    service: ProjectService = Depends(get_project_service)
):
    """Get a project by ID"""
    project = await service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    service: ProjectService = Depends(get_project_service)
):
    """List all projects"""
    return await service.list_projects(skip=skip, limit=limit)
