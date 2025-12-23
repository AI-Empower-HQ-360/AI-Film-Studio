"""
Pydantic schemas for request/response validation.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# Authentication Schemas
class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    """Schema for token refresh."""
    refresh_token: str


class UserResponse(BaseModel):
    """Schema for user response."""
    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Project Schemas
class ProjectCreate(BaseModel):
    """Schema for project creation."""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None


class ProjectUpdate(BaseModel):
    """Schema for project update."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None


class ProjectResponse(BaseModel):
    """Schema for project response."""
    id: int
    name: str
    description: Optional[str]
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Job Schemas
class JobCreate(BaseModel):
    """Schema for job creation."""
    project_id: int
    script: str = Field(..., min_length=1)
    config: Optional[dict] = None


class JobUpdate(BaseModel):
    """Schema for job update."""
    status: Optional[str] = None
    progress: Optional[float] = Field(None, ge=0.0, le=100.0)


class JobResponse(BaseModel):
    """Schema for job response."""
    id: int
    project_id: int
    user_id: int
    script: str
    status: str
    progress: float
    estimated_cost: float
    actual_cost: float
    moderation_status: str
    moderation_score: Optional[float]
    output_url: Optional[str]
    signed_url: Optional[str]
    signed_url_expires_at: Optional[datetime]
    error_message: Optional[str]
    retry_count: int
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# Cost Schemas
class CostEstimate(BaseModel):
    """Schema for cost estimation."""
    estimated_cost: float
    breakdown: dict


# Signed URL Schemas
class SignedURLRequest(BaseModel):
    """Schema for signed URL request."""
    job_id: int


class SignedURLResponse(BaseModel):
    """Schema for signed URL response."""
    url: str
    expires_at: datetime
