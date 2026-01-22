"""
Image Creation Routes - API endpoints for comprehensive image generation
"""
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
import uuid
from src.engines.image_creation_engine import (
    ImageCreationEngine,
    ImageGenerationRequest,
    AgeGroup,
    Gender,
    CulturalRegion,
    BodyType,
    DressType,
    LocationType,
    AnimalCategory
)

router = APIRouter(prefix="/api/v1/images", tags=["images"])

# Global service instance
_image_engine = ImageCreationEngine()


@router.post("/generate", status_code=202)
async def generate_image(
    request: Dict[str, Any],
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """
    Generate image(s) with comprehensive parameters
    
    Request body:
    - prompt: Base image description (required, unless character_type is provided)
    - age_group: Age group (0-3, 4-8, 8-12, 13-19, 20-21, 22-35, 35-50, 50+)
    - gender: Gender (boy, girl, man, woman, child, non_binary)
    - cultural_region: Cultural region (south_indian, chinese, american, etc.)
    - body_type: Body type (slim, average, athletic, curvy, etc.)
    - dress_type: Dress/clothing type (traditional, sari, casual, formal, etc.)
    - location: Location/setting (temple, beach, ocean, home, etc.)
    - animal_type: Animal type (if generating animal)
    - character_type: Character type (krishna, radha, shiva, etc.)
    - character_name: Name to overlay on image (optional)
    - name_meaning: Meaning of the name for overlay (optional)
    - accessories: List of accessories (crown, peacock_feather, jewelry, etc.)
    - pose: Pose (standing, sitting, playing_flute, etc.)
    - expression: Expression (smiling, serene, joyful, etc.)
    - include_name_overlay: Include name overlay on image (default: false)
    - style: Image style (realistic, artistic, cinematic, traditional)
    - resolution: Image resolution (default: 1024x1024)
    - num_images: Number of images to generate (1-4, default: 1)
    - seed: Random seed for reproducibility (optional)
    - negative_prompt: Things to avoid in image (optional)
    - cultural_context: Additional cultural context (optional)
    """
    try:
        job_id = f"img_{uuid.uuid4().hex[:12]}"
        
        # Convert dict to request model
        image_request = ImageGenerationRequest(
            prompt=request.get("prompt", ""),
            age_group=request.get("age_group"),
            gender=request.get("gender"),
            cultural_region=request.get("cultural_region"),
            body_type=request.get("body_type"),
            dress_type=request.get("dress_type"),
            location=request.get("location"),
            animal_type=request.get("animal_type"),
            character_type=request.get("character_type"),
            character_name=request.get("character_name"),
            name_meaning=request.get("name_meaning"),
            accessories=request.get("accessories"),
            pose=request.get("pose"),
            expression=request.get("expression"),
            include_name_overlay=request.get("include_name_overlay", False),
            style=request.get("style", "realistic"),
            resolution=request.get("resolution", "1024x1024"),
            num_images=request.get("num_images", 1),
            seed=request.get("seed"),
            negative_prompt=request.get("negative_prompt"),
            cultural_context=request.get("cultural_context")
        )
        
        # Start generation in background
        background_tasks.add_task(
            _image_engine.generate_image,
            image_request,
            job_id
        )
        
        return {
            "job_id": job_id,
            "status": "processing",
            "message": "Image generation started"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start image generation: {str(e)}")


@router.get("/status/{job_id}")
async def get_image_status(job_id: str) -> Dict[str, Any]:
    """
    Get the status of an image generation job
    
    Returns:
    - job_id: Job identifier
    - status: Job status (processing, completed, failed, not_found)
    - images: List of generated images with URLs (if completed)
    - prompt: Enhanced prompt used
    - processing_time: Processing time in seconds (if completed)
    - error_message: Error message (if failed)
    """
    status = _image_engine.get_job_status(job_id)
    
    if status.get("status") == "not_found":
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {
        "job_id": job_id,
        **status
    }


@router.get("/options/age-groups")
async def get_age_groups() -> Dict[str, Any]:
    """Get list of supported age groups"""
    age_groups = _image_engine.get_supported_age_groups()
    return {
        "age_groups": age_groups,
        "count": len(age_groups)
    }


@router.get("/options/genders")
async def get_genders() -> Dict[str, Any]:
    """Get list of supported gender options"""
    genders = _image_engine.get_supported_genders()
    return {
        "genders": genders,
        "count": len(genders)
    }


@router.get("/options/cultures")
async def get_cultures() -> Dict[str, Any]:
    """Get list of supported cultural regions"""
    cultures = _image_engine.get_supported_cultures()
    return {
        "cultures": cultures,
        "count": len(cultures)
    }


@router.get("/options/animals")
async def get_animals() -> Dict[str, Any]:
    """Get list of supported animal types"""
    animals = _image_engine.get_supported_animals()
    return {
        "animals": animals,
        "count": len(animals)
    }


@router.get("/options/body-types")
async def get_body_types() -> Dict[str, Any]:
    """Get list of supported body types"""
    body_types = _image_engine.get_supported_body_types()
    return {
        "body_types": body_types,
        "count": len(body_types)
    }


@router.get("/options/dress-types")
async def get_dress_types() -> Dict[str, Any]:
    """Get list of supported dress types"""
    dress_types = _image_engine.get_supported_dress_types()
    return {
        "dress_types": dress_types,
        "count": len(dress_types)
    }


@router.get("/options/character-types")
async def get_character_types() -> Dict[str, Any]:
    """Get list of supported character types"""
    character_types = _image_engine.get_supported_character_types()
    return {
        "character_types": character_types,
        "count": len(character_types)
    }


@router.get("/options/accessories")
async def get_accessories() -> Dict[str, Any]:
    """Get list of supported accessories"""
    accessories = _image_engine.get_supported_accessories()
    return {
        "accessories": accessories,
        "count": len(accessories)
    }


@router.get("/options/poses")
async def get_poses() -> Dict[str, Any]:
    """Get list of supported poses"""
    poses = _image_engine.get_supported_poses()
    return {
        "poses": poses,
        "count": len(poses)
    }


@router.get("/options/expressions")
async def get_expressions() -> Dict[str, Any]:
    """Get list of supported expressions"""
    expressions = _image_engine.get_supported_expressions()
    return {
        "expressions": expressions,
        "count": len(expressions)
    }


@router.get("/options/locations")
async def get_locations() -> Dict[str, Any]:
    """Get list of supported locations"""
    locations = _image_engine.get_supported_locations()
    return {
        "locations": locations,
        "count": len(locations)
    }


@router.get("/{image_id}")
async def get_image(image_id: str) -> Dict[str, Any]:
    """
    Get generated image by ID
    
    Returns:
    - image_id: Image identifier
    - url: Image URL (S3 or data URL)
    - prompt: Prompt used to generate
    - metadata: Image metadata (age_group, gender, cultural_region, etc.)
    - created_at: Creation timestamp
    """
    image = _image_engine.get_image(image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return {
        "image_id": image.image_id,
        "url": image.url,
        "prompt": image.prompt,
        "metadata": image.metadata,
        "created_at": image.created_at.isoformat()
    }
