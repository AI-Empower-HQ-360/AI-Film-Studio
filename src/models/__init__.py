"""Database models for AI Film Studio"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class BaseDBModel(BaseModel):
    """Base model with common fields"""
    id: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True
