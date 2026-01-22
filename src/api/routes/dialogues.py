"""
Dialogues Routes - API endpoints for dialogue generation and management
"""
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException
from src.engines.dialogues_engine import (
    DialoguesEngine,
    Conversation,
    DialogueLine,
    DialogueType,
    DialogueStyle
)

router = APIRouter(prefix="/api/v1/dialogues", tags=["dialogues"])

# Global service instance
_dialogues_engine = DialoguesEngine()


@router.post("/conversations", status_code=201)
async def create_conversation(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new conversation
    
    Request body:
    - participants: List of character IDs (required)
    - dialogue_type: Type of dialogue (default: conversation)
    - dialogue_style: Style of dialogue (default: casual)
    - scene_id: Associated scene ID (optional)
    - topic: Conversation topic (optional)
    - mood: Conversation mood (optional)
    """
    try:
        conversation = _dialogues_engine.create_conversation(
            participants=request.get("participants", []),
            dialogue_type=request.get("dialogue_type", DialogueType.CONVERSATION),
            dialogue_style=request.get("dialogue_style", DialogueStyle.CASUAL),
            scene_id=request.get("scene_id"),
            topic=request.get("topic"),
            mood=request.get("mood"),
            metadata=request.get("metadata", {})
        )
        
        return {
            "conversation_id": conversation.conversation_id,
            "participants": conversation.participants,
            "dialogue_type": conversation.dialogue_type,
            "dialogue_style": conversation.dialogue_style,
            "status": "created"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create conversation: {str(e)}")


@router.post("/conversations/{conversation_id}/lines", status_code=201)
async def add_dialogue_line(conversation_id: str, request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add a dialogue line to conversation
    
    Request body:
    - character_id: Character ID (required)
    - character_name: Character name (required)
    - text: Dialogue text (required)
    - emotion: Emotion (default: neutral)
    - tone: Optional tone
    - timing: Optional timing in scene
    - parenthetical: Optional parenthetical
    - subtext: Optional subtext
    - language: Language code (default: en)
    """
    try:
        line = _dialogues_engine.add_dialogue_line(
            conversation_id=conversation_id,
            character_id=request.get("character_id", ""),
            character_name=request.get("character_name", ""),
            text=request.get("text", ""),
            emotion=request.get("emotion", "neutral"),
            tone=request.get("tone"),
            timing=request.get("timing"),
            parenthetical=request.get("parenthetical"),
            subtext=request.get("subtext"),
            language=request.get("language", "en"),
            metadata=request.get("metadata", {})
        )
        
        return {
            "line_id": line.line_id,
            "character_id": line.character_id,
            "character_name": line.character_name,
            "text": line.text,
            "emotion": line.emotion,
            "status": "created"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add dialogue line: {str(e)}")


@router.post("/generate", status_code=200)
async def generate_dialogue(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate dialogue based on context
    
    Request body:
    - context: Scene or situation context (required)
    - character_name: Character name (required)
    - character_personality: Character personality traits (optional)
    - emotion: Emotion for the dialogue (default: neutral)
    - dialogue_style: Style of dialogue (default: casual)
    - max_length: Maximum dialogue length in words (optional)
    """
    try:
        dialogue = _dialogues_engine.generate_dialogue(
            context=request.get("context", ""),
            character_name=request.get("character_name", ""),
            character_personality=request.get("character_personality"),
            emotion=request.get("emotion", "neutral"),
            dialogue_style=request.get("dialogue_style", DialogueStyle.CASUAL),
            max_length=request.get("max_length")
        )
        
        return {
            "dialogue": dialogue,
            "character_name": request.get("character_name"),
            "emotion": request.get("emotion", "neutral"),
            "style": request.get("dialogue_style", DialogueStyle.CASUAL)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate dialogue: {str(e)}")


@router.post("/enhance", status_code=200)
async def enhance_dialogue(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enhance dialogue with emotion, tone, and cultural context
    
    Request body:
    - dialogue_text: Original dialogue (required)
    - emotion: Target emotion (default: neutral)
    - tone: Target tone (optional)
    - cultural_context: Cultural context (optional)
    """
    try:
        enhanced = _dialogues_engine.enhance_dialogue(
            dialogue_text=request.get("dialogue_text", ""),
            emotion=request.get("emotion", "neutral"),
            tone=request.get("tone"),
            cultural_context=request.get("cultural_context")
        )
        
        return {
            "original": request.get("dialogue_text"),
            "enhanced": enhanced,
            "emotion": request.get("emotion", "neutral"),
            "tone": request.get("tone")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to enhance dialogue: {str(e)}")


@router.get("/conversations/{conversation_id}/format", status_code=200)
async def format_dialogue_for_screenplay(conversation_id: str) -> Dict[str, Any]:
    """
    Format dialogue for screenplay format
    
    Returns:
    - formatted_lines: List of formatted dialogue elements
    """
    try:
        formatted = _dialogues_engine.format_dialogue_for_screenplay(conversation_id)
        return {
            "conversation_id": conversation_id,
            "formatted_lines": formatted,
            "count": len(formatted)
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to format dialogue: {str(e)}")


@router.get("/options/dialogue-types")
async def get_dialogue_types() -> Dict[str, Any]:
    """Get list of supported dialogue types"""
    types = _dialogues_engine.get_supported_dialogue_types()
    return {"dialogue_types": types, "count": len(types)}


@router.get("/options/dialogue-styles")
async def get_dialogue_styles() -> Dict[str, Any]:
    """Get list of supported dialogue styles"""
    styles = _dialogues_engine.get_supported_dialogue_styles()
    return {"dialogue_styles": styles, "count": len(styles)}


@router.get("/options/emotions")
async def get_emotions() -> Dict[str, Any]:
    """Get list of supported emotions"""
    emotions = _dialogues_engine.get_supported_emotions()
    return {"emotions": emotions, "count": len(emotions)}


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str) -> Dict[str, Any]:
    """Get conversation by ID"""
    conversation = _dialogues_engine.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return {
        "conversation_id": conversation.conversation_id,
        "scene_id": conversation.scene_id,
        "dialogue_type": conversation.dialogue_type,
        "dialogue_style": conversation.dialogue_style,
        "participants": conversation.participants,
        "lines": [
            {
                "line_id": l.line_id,
                "character_name": l.character_name,
                "text": l.text,
                "emotion": l.emotion,
                "timing": l.timing
            }
            for l in conversation.lines
        ],
        "topic": conversation.topic,
        "mood": conversation.mood,
        "created_at": conversation.created_at.isoformat()
    }


@router.get("/conversations")
async def list_conversations() -> Dict[str, Any]:
    """List all conversations"""
    conversations = _dialogues_engine.list_conversations()
    return {
        "conversations": [
            {
                "conversation_id": c.conversation_id,
                "dialogue_type": c.dialogue_type,
                "participant_count": len(c.participants),
                "line_count": len(c.lines)
            }
            for c in conversations
        ],
        "count": len(conversations)
    }
