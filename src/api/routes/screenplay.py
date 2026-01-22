"""
Screenplay Routes - API endpoints for screenplay writing and formatting
"""
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException
from src.engines.screenplay_engine import ScreenplayEngine, Screenplay, Scene, ScreenplayElement

router = APIRouter(prefix="/api/v1/screenplay", tags=["screenplay"])

# Global service instance
_screenplay_engine = ScreenplayEngine()


@router.post("/create", status_code=201)
async def create_screenplay(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new screenplay
    
    Request body:
    - title: Screenplay title (required)
    - author: Author name (optional)
    - genre: Genre (optional)
    - logline: One-line summary (optional)
    """
    try:
        screenplay = _screenplay_engine.create_screenplay(
            title=request.get("title", ""),
            author=request.get("author"),
            genre=request.get("genre"),
            logline=request.get("logline")
        )
        
        return {
            "screenplay_id": screenplay.screenplay_id,
            "title": screenplay.title,
            "author": screenplay.author,
            "genre": screenplay.genre,
            "version": screenplay.version,
            "status": "created"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create screenplay: {str(e)}")


@router.post("/{screenplay_id}/scenes", status_code=201)
async def add_scene(screenplay_id: str, request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add a scene to screenplay
    
    Request body:
    - scene_heading: Scene heading (INT./EXT. LOCATION - TIME)
    - synopsis: Scene synopsis (optional)
    """
    try:
        scene = _screenplay_engine.add_scene(
            screenplay_id=screenplay_id,
            scene_heading=request.get("scene_heading", ""),
            synopsis=request.get("synopsis")
        )
        
        return {
            "scene_id": scene.scene_id,
            "scene_number": scene.scene_number,
            "scene_heading": scene.scene_heading,
            "status": "created"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add scene: {str(e)}")


@router.post("/scenes/{scene_id}/action", status_code=201)
async def add_action(scene_id: str, request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add action line to scene
    
    Request body:
    - action_text: Action description
    """
    try:
        element = _screenplay_engine.add_action(
            scene_id=scene_id,
            action_text=request.get("action_text", "")
        )
        
        return {
            "element_id": element.element_id,
            "element_type": element.element_type,
            "content": element.content,
            "status": "created"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add action: {str(e)}")


@router.post("/scenes/{scene_id}/dialogue", status_code=201)
async def add_dialogue(scene_id: str, request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add dialogue to scene
    
    Request body:
    - character_name: Character name (required)
    - dialogue_text: Dialogue text (required)
    - parenthetical: Parenthetical/emotion (optional)
    """
    try:
        element = _screenplay_engine.add_dialogue(
            scene_id=scene_id,
            character_name=request.get("character_name", ""),
            dialogue_text=request.get("dialogue_text", ""),
            parenthetical=request.get("parenthetical")
        )
        
        return {
            "element_id": element.element_id,
            "element_type": element.element_type,
            "character_name": element.character_name,
            "content": element.content,
            "status": "created"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add dialogue: {str(e)}")


@router.get("/{screenplay_id}/format", status_code=200)
async def format_screenplay(screenplay_id: str) -> Dict[str, Any]:
    """
    Format screenplay in industry standard format
    
    Returns:
    - formatted_text: Formatted screenplay text
    """
    try:
        formatted_text = _screenplay_engine.format_screenplay(screenplay_id)
        return {
            "screenplay_id": screenplay_id,
            "formatted_text": formatted_text
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to format screenplay: {str(e)}")


@router.get("/{screenplay_id}")
async def get_screenplay(screenplay_id: str) -> Dict[str, Any]:
    """Get screenplay by ID"""
    screenplay = _screenplay_engine.get_screenplay(screenplay_id)
    if not screenplay:
        raise HTTPException(status_code=404, detail="Screenplay not found")
    
    return {
        "screenplay_id": screenplay.screenplay_id,
        "title": screenplay.title,
        "author": screenplay.author,
        "genre": screenplay.genre,
        "version": screenplay.version,
        "logline": screenplay.logline,
        "scenes": [
            {
                "scene_id": s.scene_id,
                "scene_number": s.scene_number,
                "scene_heading": s.scene_heading,
                "element_count": len(s.elements)
            }
            for s in screenplay.scenes
        ],
        "characters": screenplay.characters,
        "created_at": screenplay.created_at.isoformat(),
        "updated_at": screenplay.updated_at.isoformat()
    }


@router.get("/")
async def list_screenplays() -> Dict[str, Any]:
    """List all screenplays"""
    screenplays = _screenplay_engine.list_screenplays()
    return {
        "screenplays": [
            {
                "screenplay_id": s.screenplay_id,
                "title": s.title,
                "author": s.author,
                "genre": s.genre,
                "scene_count": len(s.scenes)
            }
            for s in screenplays
        ],
        "count": len(screenplays)
    }
