"""
Character Engine - Core Module
Characters are first-class assets with identity locking, versions, and consistency
"""
from typing import Optional, Dict, List, Any, Literal
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)


class CharacterMode(str, Enum):
    """Character operating modes"""
    ACTOR = "actor"  # Real actor references, look tests
    AVATAR = "avatar"  # Fully AI actors for films, animation
    BRAND = "brand"  # Brand mascots, persistent characters


class CharacterType(str, Enum):
    """Character visual types"""
    PHOTOREALISTIC = "photorealistic"
    STYLIZED = "stylized"
    ANIMATED = "animated"
    CONCEPT_ART = "concept_art"


class CharacterVersionType(str, Enum):
    """Character version lifecycle"""
    CONCEPT = "concept"
    CASTING = "casting"
    FINAL = "final"
    ALTERNATE_TIMELINE = "alternate_timeline"


class CharacterIdentity(BaseModel):
    """Character identity metadata for consistency"""
    character_id: str
    name: str
    description: str
    physical_attributes: Dict[str, Any] = Field(default_factory=dict)
    personality_traits: List[str] = Field(default_factory=list)
    cultural_context: Optional[str] = None
    voice_id: Optional[str] = None  # Links to voice synthesis
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class CharacterVisual(BaseModel):
    """Character visual representation"""
    image_url: str
    s3_key: str
    version: str
    pose: Optional[str] = None
    lighting: Optional[str] = None
    emotion: Optional[str] = None
    wardrobe: Optional[str] = None
    makeup: Optional[str] = None
    aging: Optional[str] = None  # young, adult, elderly
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CharacterVersion(BaseModel):
    """Character version with history"""
    version_id: str
    character_id: str
    version_type: CharacterVersionType
    visual: CharacterVisual
    scene_assignments: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None
    notes: Optional[str] = None
    is_active: bool = True


class Character(BaseModel):
    """Complete character definition - first-class asset"""
    character_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    identity: CharacterIdentity
    mode: CharacterMode
    character_type: CharacterType
    versions: List[CharacterVersion] = Field(default_factory=list)
    active_version_id: Optional[str] = None
    brand_id: Optional[str] = None  # For brand characters
    project_id: Optional[str] = None
    consistency_lock: bool = True  # Enable identity locking
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def get_active_version(self) -> Optional[CharacterVersion]:
        """Get the currently active character version"""
        if not self.active_version_id:
            return None
        for version in self.versions:
            if version.version_id == self.active_version_id:
                return version
        return None

    def add_version(self, version: CharacterVersion) -> None:
        """Add a new character version"""
        self.versions.append(version)
        if version.is_active:
            self.active_version_id = version.version_id
        self.updated_at = datetime.utcnow()

    def get_version_by_type(self, version_type: CharacterVersionType) -> Optional[CharacterVersion]:
        """Get version by type"""
        for version in self.versions:
            if version.version_type == version_type:
                return version
        return None


class CharacterConsistencyConfig(BaseModel):
    """Configuration for character consistency across scenes"""
    identity_lock: bool = True
    pose_control: bool = True
    lighting_control: bool = True
    emotion_control: bool = True
    wardrobe_consistency: bool = True
    scene_continuity: bool = True


class CharacterEngine:
    """
    Character Engine - Core module for character management
    
    Enables:
    - Character creation (visual concept, photorealistic, stylized)
    - Identity locking across images, scenes, and video
    - Version management (concept → casting → final → alternate timelines)
    - Actor/Avatar/Brand modes
    - Scene-to-scene continuity
    """
    
    def __init__(self, s3_bucket: str = "ai-film-studio-characters"):
        self.s3_bucket = s3_bucket
        self.characters: Dict[str, Character] = {}
        self.consistency_config = CharacterConsistencyConfig()
    
    async def create_character(
        self,
        name: str,
        description: str,
        mode: CharacterMode,
        character_type: CharacterType,
        physical_attributes: Optional[Dict[str, Any]] = None,
        personality_traits: Optional[List[str]] = None,
        cultural_context: Optional[str] = None,
        project_id: Optional[str] = None,
        brand_id: Optional[str] = None
    ) -> Character:
        """
        Create a new character - first-class asset
        
        Args:
            name: Character name
            description: Character description
            mode: Actor, Avatar, or Brand mode
            character_type: Photorealistic, Stylized, Animated, or Concept Art
            physical_attributes: Physical characteristics dict
            personality_traits: List of personality traits
            cultural_context: Cultural setting/context
            project_id: Associated project
            brand_id: For brand characters
            
        Returns:
            Created Character object
        """
        character_id = str(uuid.uuid4())
        
        identity = CharacterIdentity(
            character_id=character_id,
            name=name,
            description=description,
            physical_attributes=physical_attributes or {},
            personality_traits=personality_traits or [],
            cultural_context=cultural_context
        )
        
        character = Character(
            character_id=character_id,
            identity=identity,
            mode=mode,
            character_type=character_type,
            project_id=project_id,
            brand_id=brand_id
        )
        
        self.characters[character_id] = character
        logger.info(f"Created character {character_id}: {name} ({mode.value} mode)")
        
        return character
    
    async def add_character_version(
        self,
        character_id: str,
        version_type: CharacterVersionType,
        image_url: str,
        s3_key: str,
        pose: Optional[str] = None,
        lighting: Optional[str] = None,
        emotion: Optional[str] = None,
        wardrobe: Optional[str] = None,
        makeup: Optional[str] = None,
        aging: Optional[str] = None,
        created_by: Optional[str] = None,
        notes: Optional[str] = None,
        is_active: bool = True
    ) -> CharacterVersion:
        """
        Add a new version to a character
        
        Supports: concept → casting → final → alternate timelines
        """
        if character_id not in self.characters:
            raise ValueError(f"Character {character_id} not found")
        
        character = self.characters[character_id]
        version_id = str(uuid.uuid4())
        
        visual = CharacterVisual(
            image_url=image_url,
            s3_key=s3_key,
            version=version_id,
            pose=pose,
            lighting=lighting,
            emotion=emotion,
            wardrobe=wardrobe,
            makeup=makeup,
            aging=aging
        )
        
        version = CharacterVersion(
            version_id=version_id,
            character_id=character_id,
            version_type=version_type,
            visual=visual,
            created_by=created_by,
            notes=notes,
            is_active=is_active
        )
        
        character.add_version(version)
        logger.info(f"Added version {version_id} ({version_type.value}) to character {character_id}")
        
        return version
    
    async def generate_character_image(
        self,
        character_id: str,
        prompt: str,
        scene_context: Optional[str] = None,
        pose: Optional[str] = None,
        lighting: Optional[str] = None,
        emotion: Optional[str] = None,
        wardrobe: Optional[str] = None
    ) -> CharacterVisual:
        """
        Generate character image with consistency locking
        
        Maintains character identity across different scenes and contexts
        """
        if character_id not in self.characters:
            raise ValueError(f"Character {character_id} not found")
        
        character = self.characters[character_id]
        
        # Build consistency-aware prompt
        consistency_prompt = self._build_consistency_prompt(
            character, prompt, scene_context, pose, lighting, emotion, wardrobe
        )
        
        # TODO: Integrate with image generation service
        # This would call Stable Diffusion, Midjourney, or DALL-E with character identity locked
        logger.info(f"Generating image for character {character_id} with consistency lock")
        
        # Placeholder - would generate actual image
        image_url = f"s3://{self.s3_bucket}/characters/{character_id}/generated_{uuid.uuid4()}.jpg"
        s3_key = f"characters/{character_id}/generated_{uuid.uuid4()}.jpg"
        
        visual = CharacterVisual(
            image_url=image_url,
            s3_key=s3_key,
            version=str(uuid.uuid4()),
            pose=pose,
            lighting=lighting,
            emotion=emotion,
            wardrobe=wardrobe
        )
        
        return visual
    
    def _build_consistency_prompt(
        self,
        character: Character,
        prompt: str,
        scene_context: Optional[str],
        pose: Optional[str],
        lighting: Optional[str],
        emotion: Optional[str],
        wardrobe: Optional[str]
    ) -> str:
        """Build prompt with character identity locked in"""
        identity = character.identity
        
        consistency_parts = [
            f"Character: {identity.name}",
            f"Description: {identity.description}",
        ]
        
        if identity.physical_attributes:
            attrs = ", ".join([f"{k}: {v}" for k, v in identity.physical_attributes.items()])
            consistency_parts.append(f"Physical: {attrs}")
        
        if identity.cultural_context:
            consistency_parts.append(f"Cultural context: {identity.cultural_context}")
        
        if scene_context:
            consistency_parts.append(f"Scene: {scene_context}")
        
        if pose:
            consistency_parts.append(f"Pose: {pose}")
        
        if lighting:
            consistency_parts.append(f"Lighting: {lighting}")
        
        if emotion:
            consistency_parts.append(f"Emotion: {emotion}")
        
        if wardrobe:
            consistency_parts.append(f"Wardrobe: {wardrobe}")
        
        consistency_parts.append(f"Action: {prompt}")
        
        return ", ".join(consistency_parts)
    
    async def get_character(self, character_id: str) -> Character:
        """Get character by ID"""
        if character_id not in self.characters:
            raise ValueError(f"Character {character_id} not found")
        return self.characters[character_id]
    
    async def list_characters(
        self,
        project_id: Optional[str] = None,
        mode: Optional[CharacterMode] = None,
        brand_id: Optional[str] = None
    ) -> List[Character]:
        """List characters with filters"""
        characters = list(self.characters.values())
        
        if project_id:
            characters = [c for c in characters if c.project_id == project_id]
        
        if mode:
            characters = [c for c in characters if c.mode == mode]
        
        if brand_id:
            characters = [c for c in characters if c.brand_id == brand_id]
        
        return characters
    
    async def link_character_to_voice(
        self,
        character_id: str,
        voice_id: str
    ) -> None:
        """Link character to voice synthesis voice ID"""
        if character_id not in self.characters:
            raise ValueError(f"Character {character_id} not found")
        
        self.characters[character_id].identity.voice_id = voice_id
        self.characters[character_id].updated_at = datetime.utcnow()
        logger.info(f"Linked character {character_id} to voice {voice_id}")
    
    async def assign_character_to_scene(
        self,
        character_id: str,
        version_id: str,
        scene_id: str
    ) -> None:
        """Assign character version to a specific scene"""
        if character_id not in self.characters:
            raise ValueError(f"Character {character_id} not found")
        
        character = self.characters[character_id]
        version = None
        
        for v in character.versions:
            if v.version_id == version_id:
                version = v
                break
        
        if not version:
            raise ValueError(f"Version {version_id} not found for character {character_id}")
        
        if scene_id not in version.scene_assignments:
            version.scene_assignments.append(scene_id)
            character.updated_at = datetime.utcnow()
            logger.info(f"Assigned character {character_id} version {version_id} to scene {scene_id}")
