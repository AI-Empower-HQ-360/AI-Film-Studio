"""Location model for consistency tracking"""
from typing import Optional, Dict, Any, List
from pydantic import Field
from src.models import BaseDBModel


class Location(BaseDBModel):
    """Location model with visual consistency data"""
    name: str = Field(..., description="Location name")
    description: str = Field(..., description="Location description")
    location_type: str = Field(..., description="Type of location (interior, exterior, etc.)")
    
    # Visual attributes
    environment: Dict[str, Any] = Field(
        default_factory=dict,
        description="Environmental details (terrain, architecture, vegetation, etc.)"
    )
    atmosphere: Dict[str, Any] = Field(
        default_factory=dict,
        description="Atmospheric conditions (weather, time of day, season, mood)"
    )
    
    # Consistency data
    reference_images: List[str] = Field(
        default_factory=list,
        description="URLs or paths to reference images"
    )
    template_id: Optional[str] = Field(
        None,
        description="ID for location template/embedding"
    )
    
    # Time and weather variants
    time_of_day: str = Field(
        default="day",
        description="Default time: dawn, day, dusk, night"
    )
    weather: str = Field(
        default="clear",
        description="Default weather: clear, cloudy, rainy, foggy, snowy"
    )
    season: str = Field(
        default="summer",
        description="Season: spring, summer, autumn, winter"
    )
    
    # Metadata
    tags: List[str] = Field(
        default_factory=list,
        description="Tags for categorization"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Vrindavan Forest",
                "description": "Sacred forest with flower fields",
                "location_type": "exterior",
                "environment": {
                    "terrain": "flower field",
                    "vegetation": ["flowers", "trees"],
                    "features": ["paths", "streams"]
                },
                "atmosphere": {
                    "lighting": "golden hour",
                    "mood": "divine and peaceful"
                },
                "time_of_day": "dusk",
                "weather": "clear",
                "tags": ["sacred", "nature", "peaceful"]
            }
        }
