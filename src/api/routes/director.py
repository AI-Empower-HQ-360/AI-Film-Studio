"""
Director Routes - API endpoints for film direction and shot composition
"""
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException
from src.engines.director_engine import DirectorEngine, ShotComposition, SceneDirection

router = APIRouter(prefix="/api/v1/director", tags=["director"])

# Global service instance
_director_engine = DirectorEngine()


@router.post("/shots", status_code=201)
async def create_shot(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a shot composition
    
    Request body:
    - shot_type: Type of shot (wide, close, etc.)
    - camera_angle: Camera angle (default: eye_level)
    - camera_movement: Camera movement (default: static)
    - lighting_style: Lighting style (default: natural)
    - framing: Optional framing details
    - depth_of_field: Optional depth of field
    - focus_point: Optional focus point
    - duration: Optional duration in seconds
    - transition: Optional transition type
    """
    try:
        shot = _director_engine.create_shot(
            shot_type=request.get("shot_type", ""),
            camera_angle=request.get("camera_angle", "eye_level"),
            camera_movement=request.get("camera_movement", "static"),
            lighting_style=request.get("lighting_style", "natural"),
            framing=request.get("framing"),
            depth_of_field=request.get("depth_of_field"),
            focus_point=request.get("focus_point"),
            duration=request.get("duration"),
            transition=request.get("transition"),
            metadata=request.get("metadata", {})
        )
        
        return {
            "shot_id": shot.shot_id,
            "shot_type": shot.shot_type,
            "camera_angle": shot.camera_angle,
            "camera_movement": shot.camera_movement,
            "lighting_style": shot.lighting_style,
            "status": "created"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create shot: {str(e)}")


@router.post("/scenes", status_code=201)
async def create_scene_direction(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create scene direction
    
    Request body:
    - scene_number: Scene number
    - location: Scene location
    - time_of_day: Time of day (morning, afternoon, evening, night)
    - mood: Scene mood/atmosphere
    - shots: Optional list of shot IDs
    - blocking: Optional character positioning
    - notes: Optional notes
    """
    try:
        scene = _director_engine.create_scene_direction(
            scene_number=request.get("scene_number", 1),
            location=request.get("location", ""),
            time_of_day=request.get("time_of_day", "day"),
            mood=request.get("mood", "neutral"),
            shots=request.get("shots", []),
            blocking=request.get("blocking"),
            notes=request.get("notes"),
            metadata=request.get("metadata", {})
        )
        
        return {
            "scene_id": scene.scene_id,
            "scene_number": scene.scene_number,
            "location": scene.location,
            "time_of_day": scene.time_of_day,
            "mood": scene.mood,
            "status": "created"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create scene: {str(e)}")


@router.post("/plan-sequence", status_code=200)
async def plan_shot_sequence(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Plan a sequence of shots for a scene
    
    Request body:
    - scene_description: Description of the scene
    - character_count: Number of characters (default: 1)
    - action_type: Type of action (dialogue, action, montage, etc.)
    """
    try:
        shots = _director_engine.plan_shot_sequence(
            scene_description=request.get("scene_description", ""),
            character_count=request.get("character_count", 1),
            action_type=request.get("action_type", "dialogue")
        )
        
        return {
            "shots": [
                {
                    "shot_id": shot.shot_id,
                    "shot_type": shot.shot_type,
                    "camera_angle": shot.camera_angle,
                    "camera_movement": shot.camera_movement,
                    "lighting_style": shot.lighting_style
                }
                for shot in shots
            ],
            "count": len(shots)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to plan sequence: {str(e)}")


@router.get("/options/shot-types")
async def get_shot_types() -> Dict[str, Any]:
    """Get list of supported shot types"""
    shot_types = _director_engine.get_supported_shot_types()
    return {"shot_types": shot_types, "count": len(shot_types)}


@router.get("/options/camera-movements")
async def get_camera_movements() -> Dict[str, Any]:
    """Get list of supported camera movements"""
    movements = _director_engine.get_supported_camera_movements()
    return {"movements": movements, "count": len(movements)}


@router.get("/options/camera-angles")
async def get_camera_angles() -> Dict[str, Any]:
    """Get list of supported camera angles"""
    angles = _director_engine.get_supported_camera_angles()
    return {"angles": angles, "count": len(angles)}


@router.get("/options/lighting-styles")
async def get_lighting_styles() -> Dict[str, Any]:
    """Get list of supported lighting styles"""
    styles = _director_engine.get_supported_lighting_styles()
    return {"styles": styles, "count": len(styles)}


@router.get("/scenes/{scene_id}")
async def get_scene(scene_id: str) -> Dict[str, Any]:
    """Get scene direction by ID"""
    scene = _director_engine.get_scene(scene_id)
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")
    
    return {
        "scene_id": scene.scene_id,
        "scene_number": scene.scene_number,
        "location": scene.location,
        "time_of_day": scene.time_of_day,
        "mood": scene.mood,
        "shots": [{"shot_id": s.shot_id, "shot_type": s.shot_type} for s in scene.shots],
        "blocking": scene.blocking,
        "notes": scene.notes
    }


@router.get("/shots/{shot_id}")
async def get_shot(shot_id: str) -> Dict[str, Any]:
    """Get shot composition by ID"""
    shot = _director_engine.get_shot(shot_id)
    if not shot:
        raise HTTPException(status_code=404, detail="Shot not found")
    
    return {
        "shot_id": shot.shot_id,
        "shot_type": shot.shot_type,
        "camera_angle": shot.camera_angle,
        "camera_movement": shot.camera_movement,
        "lighting_style": shot.lighting_style,
        "framing": shot.framing,
        "depth_of_field": shot.depth_of_field,
        "focus_point": shot.focus_point,
        "duration": shot.duration,
        "transition": shot.transition
    }
