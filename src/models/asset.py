"""Asset model for generated media"""
from typing import Optional, Dict, Any
from pydantic import Field
from src.models import BaseDBModel


class Asset(BaseDBModel):
    """Asset model for generated images, videos, and audio"""
    asset_type: str = Field(..., description="Type: image, video, audio")
    url: str = Field(..., description="URL or path to the asset")
    filename: str = Field(..., description="Asset filename")
    
    # Generation metadata
    prompt: Optional[str] = Field(
        None,
        description="Prompt used to generate the asset"
    )
    model: Optional[str] = Field(
        None,
        description="Model used for generation (e.g., SDXL, DALL-E)"
    )
    generation_params: Dict[str, Any] = Field(
        default_factory=dict,
        description="Generation parameters (seed, steps, cfg_scale, etc.)"
    )
    
    # Asset properties
    width: Optional[int] = Field(None, description="Width in pixels")
    height: Optional[int] = Field(None, description="Height in pixels")
    duration: Optional[float] = Field(None, description="Duration in seconds (for video/audio)")
    aspect_ratio: Optional[str] = Field(None, description="Aspect ratio (e.g., 16:9, 2.39:1)")
    
    # File metadata
    file_size: Optional[int] = Field(None, description="File size in bytes")
    mime_type: Optional[str] = Field(None, description="MIME type")
    
    # Linking
    shot_id: Optional[str] = Field(None, description="Associated shot ID")
    scene_id: Optional[str] = Field(None, description="Associated scene ID")
    
    # Status
    status: str = Field(
        default="generated",
        description="Status: pending, generating, generated, failed"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "asset_type": "image",
                "url": "s3://bucket/images/shot_001.png",
                "filename": "shot_001.png",
                "prompt": "Close-up of Radha and Krishna in flower field, cinematic",
                "model": "SDXL",
                "generation_params": {
                    "seed": 42,
                    "steps": 50,
                    "cfg_scale": 7.5
                },
                "width": 1024,
                "height": 576,
                "aspect_ratio": "16:9",
                "status": "generated"
            }
        }
