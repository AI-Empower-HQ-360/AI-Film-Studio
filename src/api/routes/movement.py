"""
Movement Routes - API endpoints for character movements and animations
"""
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException
from src.engines.movement_engine import MovementEngine, Movement, Gesture, AnimationSequence

router = APIRouter(prefix="/api/v1/movement", tags=["movement"])

# Global service instance
_movement_engine = MovementEngine()


@router.post("/movements", status_code=201)
async def create_movement(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a character movement
    
    Request body:
    - character_id: Character ID (required)
    - movement_type: Type of movement (required)
    - duration: Movement duration in seconds (default: 1.0)
    - speed: Movement speed multiplier (default: 1.0)
    - start_position: Optional start position {x, y, z}
    - end_position: Optional end position {x, y, z}
    - easing: Optional easing type
    - body_language: Optional body language
    """
    try:
        movement = _movement_engine.create_movement(
            character_id=request.get("character_id", ""),
            movement_type=request.get("movement_type", ""),
            duration=request.get("duration", 1.0),
            speed=request.get("speed", 1.0),
            start_position=request.get("start_position"),
            end_position=request.get("end_position"),
            easing=request.get("easing"),
            body_language=request.get("body_language"),
            metadata=request.get("metadata", {})
        )
        
        return {
            "movement_id": movement.movement_id,
            "movement_type": movement.movement_type,
            "character_id": movement.character_id,
            "duration": movement.duration,
            "speed": movement.speed,
            "status": "created"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create movement: {str(e)}")


@router.post("/gestures", status_code=201)
async def create_gesture(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a hand gesture
    
    Request body:
    - character_id: Character ID (required)
    - gesture_type: Type of gesture (required)
    - hand: Which hand (left, right, both, default: both)
    - intensity: Gesture intensity (0.0-2.0, default: 1.0)
    - duration: Gesture duration in seconds (default: 1.0)
    - timing: Optional timing in scene
    """
    try:
        gesture = _movement_engine.create_gesture(
            character_id=request.get("character_id", ""),
            gesture_type=request.get("gesture_type", ""),
            hand=request.get("hand", "both"),
            intensity=request.get("intensity", 1.0),
            duration=request.get("duration", 1.0),
            timing=request.get("timing"),
            metadata=request.get("metadata", {})
        )
        
        return {
            "gesture_id": gesture.gesture_id,
            "gesture_type": gesture.gesture_type,
            "character_id": gesture.character_id,
            "hand": gesture.hand,
            "intensity": gesture.intensity,
            "duration": gesture.duration,
            "status": "created"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create gesture: {str(e)}")


@router.post("/animations", status_code=201)
async def create_animation_sequence(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create an animation sequence
    
    Request body:
    - character_id: Character ID (required)
    - movements: Optional list of movement IDs
    - gestures: Optional list of gesture IDs
    - body_language: Optional overall body language
    - animation_style: Animation style (default: realistic)
    """
    try:
        # Get movements and gestures by ID
        movements = []
        if request.get("movements"):
            for mov_id in request.get("movements", []):
                mov = _movement_engine.get_movement(mov_id)
                if mov:
                    movements.append(mov)
        
        gestures = []
        if request.get("gestures"):
            for gest_id in request.get("gestures", []):
                gest = _movement_engine.get_gesture(gest_id)
                if gest:
                    gestures.append(gest)
        
        animation = _movement_engine.create_animation_sequence(
            character_id=request.get("character_id", ""),
            movements=movements if movements else None,
            gestures=gestures if gestures else None,
            body_language=request.get("body_language"),
            animation_style=request.get("animation_style", "realistic"),
            metadata=request.get("metadata", {})
        )
        
        return {
            "animation_id": animation.animation_id,
            "character_id": animation.character_id,
            "movement_count": len(animation.movements),
            "gesture_count": len(animation.gestures),
            "duration": animation.duration,
            "body_language": animation.body_language,
            "animation_style": animation.animation_style,
            "status": "created"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create animation: {str(e)}")


@router.post("/plan-for-dialogue", status_code=200)
async def plan_movements_for_dialogue(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Plan movements and gestures for dialogue
    
    Request body:
    - character_id: Character ID (required)
    - dialogue_text: Dialogue text (required)
    - emotion: Emotion of the dialogue (default: neutral)
    """
    try:
        animation = _movement_engine.plan_movements_for_dialogue(
            character_id=request.get("character_id", ""),
            dialogue_text=request.get("dialogue_text", ""),
            emotion=request.get("emotion", "neutral")
        )
        
        return {
            "animation_id": animation.animation_id,
            "character_id": animation.character_id,
            "movements": [
                {
                    "movement_id": m.movement_id,
                    "movement_type": m.movement_type,
                    "duration": m.duration
                }
                for m in animation.movements
            ],
            "gestures": [
                {
                    "gesture_id": g.gesture_id,
                    "gesture_type": g.gesture_type,
                    "duration": g.duration
                }
                for g in animation.gestures
            ],
            "body_language": animation.body_language,
            "duration": animation.duration
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to plan movements: {str(e)}")


@router.get("/options/movements")
async def get_movements() -> Dict[str, Any]:
    """Get list of supported movement types"""
    movements = _movement_engine.get_supported_movements()
    return {"movements": movements, "count": len(movements)}


@router.get("/options/gestures")
async def get_gestures() -> Dict[str, Any]:
    """Get list of supported gesture types"""
    gestures = _movement_engine.get_supported_gestures()
    return {"gestures": gestures, "count": len(gestures)}


@router.get("/options/body-languages")
async def get_body_languages() -> Dict[str, Any]:
    """Get list of supported body language types"""
    body_languages = _movement_engine.get_supported_body_languages()
    return {"body_languages": body_languages, "count": len(body_languages)}


@router.get("/movements/{movement_id}")
async def get_movement(movement_id: str) -> Dict[str, Any]:
    """Get movement by ID"""
    movement = _movement_engine.get_movement(movement_id)
    if not movement:
        raise HTTPException(status_code=404, detail="Movement not found")
    
    return {
        "movement_id": movement.movement_id,
        "movement_type": movement.movement_type,
        "character_id": movement.character_id,
        "start_position": movement.start_position,
        "end_position": movement.end_position,
        "duration": movement.duration,
        "speed": movement.speed,
        "easing": movement.easing,
        "body_language": movement.body_language
    }


@router.get("/gestures/{gesture_id}")
async def get_gesture(gesture_id: str) -> Dict[str, Any]:
    """Get gesture by ID"""
    gesture = _movement_engine.get_gesture(gesture_id)
    if not gesture:
        raise HTTPException(status_code=404, detail="Gesture not found")
    
    return {
        "gesture_id": gesture.gesture_id,
        "gesture_type": gesture.gesture_type,
        "character_id": gesture.character_id,
        "hand": gesture.hand,
        "intensity": gesture.intensity,
        "duration": gesture.duration,
        "timing": gesture.timing
    }


@router.get("/animations/{animation_id}")
async def get_animation(animation_id: str) -> Dict[str, Any]:
    """Get animation sequence by ID"""
    animation = _movement_engine.get_animation(animation_id)
    if not animation:
        raise HTTPException(status_code=404, detail="Animation not found")
    
    return {
        "animation_id": animation.animation_id,
        "character_id": animation.character_id,
        "movement_count": len(animation.movements),
        "gesture_count": len(animation.gestures),
        "body_language": animation.body_language,
        "animation_style": animation.animation_style,
        "duration": animation.duration
    }
