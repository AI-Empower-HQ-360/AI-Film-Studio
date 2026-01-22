"""
Character Routes - API endpoints for character management
"""
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/characters", tags=["characters"])


class CharacterCreate(BaseModel):
    """Request model for creating a character"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    voice_id: Optional[str] = None
    appearance: Optional[Dict[str, Any]] = None


class CharacterResponse(BaseModel):
    """Response model for character"""
    character_id: str
    name: str
    description: Optional[str] = None
    voice_id: Optional[str] = None
    appearance: Optional[Dict[str, Any]] = None
    created_at: datetime


class CharacterService:
    """Service class for character operations"""
    
    def __init__(self):
        self.characters: Dict[str, Dict[str, Any]] = {}
    
    async def create_character(
        self, 
        name: str, 
        description: Optional[str] = None,
        voice_id: Optional[str] = None,
        appearance: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a new character"""
        character_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        character = {
            "character_id": character_id,
            "name": name,
            "description": description,
            "voice_id": voice_id,
            "appearance": appearance or {},
            "created_at": now,
        }
        
        self.characters[character_id] = character
        return character
    
    async def get_character(self, character_id: str) -> Optional[Dict[str, Any]]:
        """Get character by ID"""
        return self.characters.get(character_id)
    
    async def list_characters(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """List all characters with pagination"""
        all_characters = list(self.characters.values())
        return all_characters[skip:skip + limit]
    
    async def update_character(
        self, 
        character_id: str, 
        updates: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update a character"""
        if character_id not in self.characters:
            return None
        
        self.characters[character_id].update(updates)
        return self.characters[character_id]
    
    async def delete_character(self, character_id: str) -> bool:
        """Delete a character"""
        if character_id in self.characters:
            del self.characters[character_id]
            return True
        return False


# Global service instance
_character_service = CharacterService()


def get_character_service() -> CharacterService:
    """Dependency injection for character service"""
    return _character_service


@router.post("/", response_model=CharacterResponse)
async def create_character(
    character: CharacterCreate,
    service: CharacterService = Depends(get_character_service)
):
    """Create a new character"""
    result = await service.create_character(
        name=character.name,
        description=character.description,
        voice_id=character.voice_id,
        appearance=character.appearance
    )
    return result


@router.get("/{character_id}", response_model=CharacterResponse)
async def get_character(
    character_id: str,
    service: CharacterService = Depends(get_character_service)
):
    """Get a character by ID"""
    character = await service.get_character(character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character


@router.get("/", response_model=List[CharacterResponse])
async def list_characters(
    skip: int = 0,
    limit: int = 100,
    service: CharacterService = Depends(get_character_service)
):
    """List all characters"""
    return await service.list_characters(skip=skip, limit=limit)
