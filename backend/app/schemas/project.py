from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProjectBase(BaseModel):
    """Base project schema"""
    title: str
    description: Optional[str] = None
    script: Optional[str] = None


class ProjectCreate(ProjectBase):
    """Project creation schema"""
    pass


class ProjectUpdate(BaseModel):
    """Project update schema"""
    title: Optional[str] = None
    description: Optional[str] = None
    script: Optional[str] = None


class ProjectResponse(ProjectBase):
    """Project response schema"""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
