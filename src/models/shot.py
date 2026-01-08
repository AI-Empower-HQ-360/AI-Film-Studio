"""Shot model for film production"""
from typing import Optional, Dict, Any, List
from pydantic import Field
from src.models import BaseDBModel


class Shot(BaseDBModel):
    """Shot model with metadata for image/video generation"""
    scene_id: str = Field(..., description="Parent scene ID")
    shot_number: int = Field(..., description="Shot number in sequence")
    
    # Shot composition
    shot_type: str = Field(
        ...,
        description="Shot type: wide, medium, close-up, extreme-close-up, over-the-shoulder"
    )
    camera_angle: str = Field(
        default="eye-level",
        description="Camera angle: eye-level, high-angle, low-angle, bird's-eye, worm's-eye"
    )
    camera_movement: str = Field(
        default="static",
        description="Camera movement: static, pan, tilt, dolly, zoom, tracking"
    )
    framing: str = Field(
        default="center",
        description="Framing composition: center, rule-of-thirds, golden-ratio"
    )
    
    # Content
    description: str = Field(..., description="Shot description")
    dialogue: Optional[str] = Field(None, description="Dialogue in this shot")
    action: Optional[str] = Field(None, description="Action happening in shot")
    
    # Visual elements
    characters: List[str] = Field(
        default_factory=list,
        description="Character IDs in this shot"
    )
    location_id: Optional[str] = Field(None, description="Location ID")
    
    # Style and mood
    style: str = Field(
        default="cinematic",
        description="Visual style: cinematic, anime, noir, realistic, etc."
    )
    lighting: str = Field(
        default="natural",
        description="Lighting: natural, golden-hour, blue-hour, dramatic, soft, etc."
    )
    mood: str = Field(
        default="neutral",
        description="Emotional mood of the shot"
    )
    
    # Timing
    duration: float = Field(default=3.0, description="Duration in seconds")
    
    # Assets
    image_asset_id: Optional[str] = Field(None, description="Generated keyframe image asset ID")
    video_asset_id: Optional[str] = Field(None, description="Generated video asset ID")
    audio_asset_id: Optional[str] = Field(None, description="Generated audio asset ID")
    
    # Generation metadata
    prompt: Optional[str] = Field(None, description="Generated prompt for this shot")
    
    class Config:
        json_schema_extra = {
            "example": {
                "scene_id": "scene_001",
                "shot_number": 1,
                "shot_type": "close-up",
                "camera_angle": "eye-level",
                "camera_movement": "static",
                "description": "Radha and Krishna walking through flower field",
                "characters": ["char_radha", "char_krishna"],
                "location_id": "loc_vrindavan",
                "style": "cinematic",
                "lighting": "golden-hour",
                "mood": "romantic and divine",
                "duration": 5.0
            }
        }
