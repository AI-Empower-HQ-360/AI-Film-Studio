"""
Projects API endpoints.
"""
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends

from app.schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from app.core.security import get_current_user

router = APIRouter()

# Mock database for demonstration
mock_projects = {}
project_counter = 0


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new project."""
    global project_counter
    project_counter += 1
    
    project = {
        "id": project_counter,
        "name": project_data.name,
        "description": project_data.description,
        "user_id": int(current_user["user_id"]),
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
    
    mock_projects[project_counter] = project
    return ProjectResponse(**project)


@router.get("/", response_model=List[ProjectResponse])
async def list_projects(current_user: dict = Depends(get_current_user)):
    """List all projects for the current user."""
    user_id = int(current_user["user_id"])
    user_projects = [
        ProjectResponse(**p) 
        for p in mock_projects.values() 
        if p["user_id"] == user_id
    ]
    return user_projects


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific project."""
    project = mock_projects.get(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check ownership
    if project["user_id"] != int(current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this project"
        )
    
    return ProjectResponse(**project)


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update a project."""
    project = mock_projects.get(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check ownership
    if project["user_id"] != int(current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this project"
        )
    
    # Update fields
    if project_data.name is not None:
        project["name"] = project_data.name
    if project_data.description is not None:
        project["description"] = project_data.description
    
    project["updated_at"] = "2024-01-01T00:00:00"
    
    return ProjectResponse(**project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Delete a project."""
    project = mock_projects.get(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check ownership
    if project["user_id"] != int(current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this project"
        )
    
    del mock_projects[project_id]
    return None
