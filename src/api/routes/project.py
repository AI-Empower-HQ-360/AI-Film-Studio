"""Project service API routes"""
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from src.database.base import get_db
from src.database.models.user import User
from src.database.models.project import Project, ProjectStatus
from src.api.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectList
from src.utils.auth import get_current_user

router = APIRouter(prefix="/api/projects", tags=["Projects"])


@router.post("/create", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new project
    
    Request:
    - title: string
    - script: string
    - images: array of strings
    - voice: string
    - duration: integer (minutes)
    - music: string
    
    Response:
    - project_id: UUID
    - status: string
    """
    new_project = Project(
        user_id=current_user.id,
        title=project_data.title,
        script=project_data.script,
        images=project_data.images,
        voice=project_data.voice,
        duration=project_data.duration,
        music=project_data.music,
        status=ProjectStatus.PENDING
    )
    
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    return new_project


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get project details
    
    Response:
    - project details
    - status
    - video_url
    - subtitles_url
    """
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return project


@router.get("/", response_model=ProjectList)
async def list_projects(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List user's projects with pagination
    
    Query params:
    - page: integer (default 1)
    - per_page: integer (default 20, max 100)
    - status: string (optional filter)
    
    Response:
    - projects: array
    - total: integer
    - page: integer
    - per_page: integer
    """
    query = db.query(Project).filter(Project.user_id == current_user.id)
    
    # Apply status filter if provided
    if status_filter:
        query = query.filter(Project.status == status_filter)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * per_page
    projects = query.order_by(Project.created_at.desc()).offset(offset).limit(per_page).all()
    
    return {
        "projects": projects,
        "total": total,
        "page": page,
        "per_page": per_page
    }


@router.post("/{project_id}/regenerate", response_model=ProjectResponse)
async def regenerate_project(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Regenerate a project video
    
    Response:
    - status: string
    """
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Reset project status for regeneration
    project.status = ProjectStatus.PENDING
    db.commit()
    db.refresh(project)
    
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: UUID,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update project details
    
    Request:
    - title: string (optional)
    - script: string (optional)
    - images: array (optional)
    - voice: string (optional)
    - duration: integer (optional)
    - music: string (optional)
    """
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Update fields
    if project_data.title is not None:
        project.title = project_data.title
    if project_data.script is not None:
        project.script = project_data.script
    if project_data.images is not None:
        project.images = project_data.images
    if project_data.voice is not None:
        project.voice = project_data.voice
    if project_data.duration is not None:
        project.duration = project_data.duration
    if project_data.music is not None:
        project.music = project_data.music
    
    db.commit()
    db.refresh(project)
    
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a project
    
    Response:
    - 204 No Content
    """
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db.delete(project)
    db.commit()
    
    return None
