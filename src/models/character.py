"""Character model for consistency tracking"""
from typing import Optional, Dict, Any, List
from pydantic import Field
from src.models import BaseDBModel


class Character(BaseDBModel):
    """Character model with visual consistency data"""
    name: str = Field(..., description="Character name")
    description: str = Field(..., description="Character description")
    
    # Visual attributes
    appearance: Dict[str, Any] = Field(
        default_factory=dict,
        description="Physical appearance attributes (hair, eyes, build, etc.)"
    )
    attire: Dict[str, Any] = Field(
        default_factory=dict,
        description="Clothing and costume details"
    )
    
    # Consistency data
    reference_images: List[str] = Field(
        default_factory=list,
        description="URLs or paths to reference images"
    )
    embedding_id: Optional[str] = Field(
        None,
        description="ID for character embedding/LoRA"
    )
    seed: Optional[int] = Field(
        None,
        description="Seed for consistent generation"
    )
    
    # Metadata
    character_type: str = Field(
        default="main",
        description="Character type: main, supporting, background"
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Tags for categorization"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Radha",
                "description": "Divine character with traditional Indian attire",
                "appearance": {
                    "hair": "long black hair",
                    "eyes": "dark brown eyes",
                    "skin": "fair complexion",
                    "build": "graceful"
                },
                "attire": {
                    "style": "traditional Indian",
                    "colors": ["red", "gold"],
                    "jewelry": ["necklace", "bangles"]
                },
                "character_type": "main",
                "tags": ["divine", "traditional"]
            }
        }
