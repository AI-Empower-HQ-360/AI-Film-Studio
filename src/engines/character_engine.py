"""
Character Engine - Core Module
Characters are first-class assets with identity locking, versions, and consistency
"""
from typing import Optional, Dict, List, Any, Literal
try:
    from pydantic import BaseModel, Field
except ImportError:
    # Fallback for testing environments without pydantic
    class BaseModel:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    def Field(default=..., **kwargs):
        return default
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
    
    @property
    def name(self) -> str:
        """Shortcut to identity.name for compatibility"""
        return self.identity.name
    
    @property
    def id(self) -> str:
        """Alias for character_id for compatibility"""
        return self.character_id
    
    @property
    def appearance(self) -> Dict[str, Any]:
        """Get appearance from physical_attributes for compatibility"""
        return self.identity.physical_attributes
    
    @property
    def personality(self) -> Dict[str, Any]:
        """Get personality from metadata for compatibility"""
        return self.metadata.get('personality', {'traits': self.identity.personality_traits})
    
    @property
    def voice_id(self) -> Optional[str]:
        """Get voice_id from identity for compatibility"""
        return self.identity.voice_id
    
    def model_dump(self, **kwargs) -> Dict[str, Any]:
        """Override to include name in serialization"""
        data = super().model_dump(**kwargs)
        data['name'] = self.identity.name
        data['appearance'] = self.identity.physical_attributes
        return data

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


class Relationship(BaseModel):
    """Character relationship model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    character1_id: str
    character2_id: str
    type: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


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
        self.voice_parameters: Dict[str, Dict[str, Any]] = {}
        # Service dependencies for testing/mocking
        self.image_generator = None
        self.db = None
        self.ai_service = None
        self.voice_service = None
        self.voice_client = None
        self.llm_client = None
        self.storage_service = None
        self.llm_service = None
        self.relationships: Dict[str, List[Dict[str, Any]]] = {}
    
    def create_character(
        self,
        name: str,
        description: Optional[str] = None,
        mode: Optional[CharacterMode] = None,
        character_type: Optional[CharacterType] = None,
        physical_attributes: Optional[Dict[str, Any]] = None,
        personality_traits: Optional[List[str]] = None,
        cultural_context: Optional[str] = None,
        project_id: Optional[str] = None,
        brand_id: Optional[str] = None,
        appearance: Optional[Dict[str, Any]] = None,
        personality: Optional[Dict[str, Any]] = None,
        voice_id: Optional[str] = None,
        **kwargs
    ) -> Character:
        """
        Create a new character - first-class asset (synchronous)
        
        Args:
            name: Character name (required)
            description: Character description
            mode: Actor, Avatar, or Brand mode
            character_type: Photorealistic, Stylized, Animated, or Concept Art
            physical_attributes: Physical characteristics dict
            personality_traits: List of personality traits
            cultural_context: Cultural setting/context
            project_id: Associated project
            brand_id: For brand characters
            appearance: Alternative to physical_attributes (for compatibility)
            personality: Dict with personality info (for compatibility)
            voice_id: Voice ID for the character
            
        Returns:
            Created Character object
        """
        if not name:
            raise ValueError("Character name is required")
        
        character_id = str(uuid.uuid4())
        
        # Handle compatibility with appearance/physical_attributes
        attrs = physical_attributes or appearance or {}
        
        # Extract personality traits from dict if provided
        traits = personality_traits or []
        if personality and 'traits' in personality:
            traits = personality['traits']
        
        identity = CharacterIdentity(
            character_id=character_id,
            name=name,
            description=description or f"A character named {name}",
            physical_attributes=attrs,
            personality_traits=traits,
            cultural_context=cultural_context,
            voice_id=voice_id
        )
        
        character = Character(
            character_id=character_id,
            identity=identity,
            mode=mode or CharacterMode.AVATAR,
            character_type=character_type or CharacterType.PHOTOREALISTIC,
            project_id=project_id,
            brand_id=brand_id
        )
        
        self.characters[character_id] = character
        logger.info(f"Created character {character_id}: {name} ({character.mode.value} mode)")
        
        return character
    
    async def create_character_async(
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
        Create a new character - first-class asset (async version)
        
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
        return self.create_character(
            name=name,
            description=description,
            mode=mode,
            character_type=character_type,
            physical_attributes=physical_attributes,
            personality_traits=personality_traits,
            cultural_context=cultural_context,
            project_id=project_id,
            brand_id=brand_id
        )
    
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
    
    async def delete_character(self, character_id: str) -> bool:
        """
        Delete a character
        
        Args:
            character_id: ID of character to delete
            
        Returns:
            True if deleted successfully, False otherwise
        """
        if character_id not in self.characters:
            logger.warning(f"Character {character_id} not found for deletion")
            return False
        
        del self.characters[character_id]
        logger.info(f"Deleted character {character_id}")
        return True
    
    def delete(self, character_id: str) -> bool:
        """
        Delete a character (synchronous alias for delete_character)
        
        Args:
            character_id: ID of character to delete
            
        Returns:
            True if deleted successfully, False otherwise
        """
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(self.delete_character(character_id))
        except RuntimeError:
            # If no event loop, create a new one
            return asyncio.run(self.delete_character(character_id))
    
    async def clone_character(
        self,
        character_id: str,
        new_name: Optional[str] = None
    ) -> Character:
        """
        Clone a character with a new ID
        
        Args:
            character_id: ID of character to clone
            new_name: Optional new name for the clone
            
        Returns:
            Cloned Character object
        """
        if character_id not in self.characters:
            raise ValueError(f"Character {character_id} not found")
        
        original = self.characters[character_id]
        
        # Create new character ID
        new_character_id = str(uuid.uuid4())
        
        # Clone identity
        new_identity = CharacterIdentity(
            character_id=new_character_id,
            name=new_name or f"{original.identity.name} (Clone)",
            description=original.identity.description,
            physical_attributes=original.identity.physical_attributes.copy(),
            personality_traits=original.identity.personality_traits.copy(),
            cultural_context=original.identity.cultural_context,
            voice_id=original.identity.voice_id
        )
        
        # Create cloned character
        cloned_character = Character(
            character_id=new_character_id,
            identity=new_identity,
            mode=original.mode,
            character_type=original.character_type,
            brand_id=original.brand_id,
            project_id=original.project_id,
            consistency_lock=original.consistency_lock
        )
        
        # Clone versions
        for version in original.versions:
            cloned_version = CharacterVersion(
                version_id=str(uuid.uuid4()),
                character_id=new_character_id,
                version_type=version.version_type,
                visual=CharacterVisual(
                    image_url=version.visual.image_url,
                    s3_key=version.visual.s3_key,
                    version=version.visual.version,
                    pose=version.visual.pose,
                    lighting=version.visual.lighting,
                    emotion=version.visual.emotion,
                    wardrobe=version.visual.wardrobe,
                    makeup=version.visual.makeup,
                    aging=version.visual.aging,
                    metadata=version.visual.metadata.copy()
                ),
                scene_assignments=version.scene_assignments.copy(),
                created_by=version.created_by,
                notes=f"Cloned from {character_id}",
                is_active=version.is_active
            )
            cloned_character.add_version(cloned_version)
        
        self.characters[new_character_id] = cloned_character
        logger.info(f"Cloned character {character_id} to {new_character_id}")
        
        return cloned_character
    
    def clone(
        self,
        character_id: str,
        new_name: Optional[str] = None
    ) -> Character:
        """
        Clone a character (synchronous alias for clone_character)
        
        Args:
            character_id: ID of character to clone
            new_name: Optional new name for the clone
            
        Returns:
            Cloned Character object
        """
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(self.clone_character(character_id, new_name))
        except RuntimeError:
            # If no event loop, create a new one
            return asyncio.run(self.clone_character(character_id, new_name))
    
    async def generate_portrait(
        self,
        character: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate a portrait image for a character
        
        Args:
            character: Character dictionary or Character object
            
        Returns:
            Dictionary with image URL and metadata
        """
        character_id = character.get('id') or character.get('character_id', str(uuid.uuid4()))
        name = character.get('name', 'Unknown')
        
        logger.info(f"Generating portrait for character: {name}")
        
        # Use image_generator if available
        if self.image_generator:
            result = await self.image_generator.generate(prompt=f"Portrait of {name}")
            return result
        
        # Fallback to mock response
        image_url = f"https://{self.s3_bucket}.s3.amazonaws.com/portraits/{character_id}.png"
        
        return {
            "url": image_url,
            "character_id": character_id,
            "width": 1024,
            "height": 1024,
            "format": "png"
        }
    
    async def generate_variations(
        self,
        character: Dict[str, Any],
        num_variations: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Generate multiple variations of a character portrait
        
        Args:
            character: Character dictionary
            num_variations: Number of variations to generate
            
        Returns:
            List of image dictionaries
        """
        variations = []
        character_id = character.get('id') or character.get('character_id', str(uuid.uuid4()))
        
        for i in range(num_variations):
            variations.append({
                "url": f"https://{self.s3_bucket}.s3.amazonaws.com/portraits/{character_id}_v{i+1}.png",
                "variation_number": i + 1,
                "width": 1024,
                "height": 1024
            })
        
        logger.info(f"Generated {num_variations} variations for character {character_id}")
        return variations
    
    def update_appearance(
        self,
        character_or_id,
        appearance: Dict[str, Any]
    ) -> Character:
        """
        Update character appearance attributes
        
        Args:
            character_or_id: Character object or character ID string
            appearance: New appearance attributes
            
        Returns:
            Updated Character object
        """
        # Handle character ID string
        if isinstance(character_or_id, str):
            if character_or_id not in self.characters:
                raise ValueError(f"Character {character_or_id} not found")
            character = self.characters[character_or_id]
        else:
            character = character_or_id
            
        character.identity.physical_attributes.update(appearance)
        character.updated_at = datetime.utcnow()
        logger.info(f"Updated appearance for character {character.character_id}")
        return character
    
    def set_personality(
        self,
        character_or_id,
        personality: Dict[str, Any]
    ) -> Character:
        """
        Set character personality traits
        
        Args:
            character_or_id: Character object or character ID string
            personality: Personality configuration
            
        Returns:
            Updated Character object
        """
        # Handle character ID string
        if isinstance(character_or_id, str):
            if character_or_id not in self.characters:
                raise ValueError(f"Character {character_or_id} not found")
            character = self.characters[character_or_id]
        else:
            character = character_or_id
            
        if 'traits' in personality:
            character.identity.personality_traits = personality['traits']
        character.metadata['personality'] = personality
        character.updated_at = datetime.utcnow()
        logger.info(f"Set personality for character {character.character_id}")
        return character
    
    def analyze_personality(
        self,
        character: Character
    ) -> Dict[str, Any]:
        """
        Analyze character personality
        
        Args:
            character: Character object
            
        Returns:
            Personality analysis dictionary
        """
        return {
            "character_id": character.character_id,
            "name": character.identity.name,
            "traits": character.identity.personality_traits,
            "trait_count": len(character.identity.personality_traits),
            "analysis": {
                "dominant_trait": character.identity.personality_traits[0] if character.identity.personality_traits else None,
                "complexity": "high" if len(character.identity.personality_traits) > 3 else "low"
            }
        }
    
    def generate_backstory(
        self,
        character: Character
    ) -> str:
        """
        Generate a backstory for the character
        
        Args:
            character: Character object
            
        Returns:
            Generated backstory text
        """
        identity = character.identity
        traits = ", ".join(identity.personality_traits) if identity.personality_traits else "unique"
        
        backstory = (
            f"{identity.name} is a {traits} individual. "
            f"{identity.description} "
            f"Their journey began in circumstances that shaped who they are today."
        )
        
        logger.info(f"Generated backstory for character {character.character_id}")
        return backstory
    
    def assign_voice(
        self,
        character_or_id,
        voice_id: str
    ) -> Character:
        """
        Assign a voice ID to a character
        
        Args:
            character_or_id: Character object or character ID string
            voice_id: Voice synthesis voice ID
            
        Returns:
            Updated Character object
        """
        # Handle character ID string
        if isinstance(character_or_id, str):
            if character_or_id not in self.characters:
                raise ValueError(f"Character {character_or_id} not found")
            character = self.characters[character_or_id]
        else:
            character = character_or_id
            
        character.identity.voice_id = voice_id
        character.updated_at = datetime.utcnow()
        logger.info(f"Assigned voice {voice_id} to character {character.character_id}")
        return character
    
    def get_available_voices(self) -> List[Dict[str, Any]]:
        """
        Get list of available voices for characters
        
        Returns:
            List of available voice configurations
        """
        # Return a sample list of voices
        return [
            {"voice_id": "elevenlabs_adam", "name": "Adam", "gender": "male", "age_group": "adult"},
            {"voice_id": "elevenlabs_bella", "name": "Bella", "gender": "female", "age_group": "young_adult"},
            {"voice_id": "elevenlabs_charlie", "name": "Charlie", "gender": "male", "age_group": "teen"},
            {"voice_id": "elevenlabs_diana", "name": "Diana", "gender": "female", "age_group": "adult"},
        ]
    
    def voice_preview(
        self,
        voice_id: str,
        text: str = "Hello, this is a voice preview."
    ) -> Dict[str, Any]:
        """
        Get a preview of a voice
        
        Args:
            voice_id: Voice ID to preview
            text: Text to preview
            
        Returns:
            Preview information
        """
        return {
            "voice_id": voice_id,
            "text": text,
            "preview_url": f"https://{self.s3_bucket}.s3.amazonaws.com/previews/{voice_id}.mp3",
            "duration": 2.5
        }
    
    def generate_voice_preview(
        self,
        character_id: str,
        text: str = "Hello, this is a voice test."
    ) -> Dict[str, Any]:
        """
        Generate a voice preview for a character
        
        Args:
            character_id: Character ID
            text: Text to preview
            
        Returns:
            Preview information
        """
        return self.voice_preview(character_id, text)
    
    def save_character(self, character: Character) -> bool:
        """
        Save character to storage
        
        Args:
            character: Character object to save
            
        Returns:
            True if saved successfully
        """
        self.characters[character.character_id] = character
        character.updated_at = datetime.utcnow()
        # Use db if available for persistence
        if self.db:
            try:
                self.db.execute("INSERT INTO characters VALUES (%s)", character.character_id)
            except Exception:
                pass
        logger.info(f"Saved character {character.character_id}")
        return True
    
    def save(self, character: Character) -> bool:
        """
        Save character (alias for save_character for test compatibility)
        
        Args:
            character: Character object to save
            
        Returns:
            True if saved successfully
        """
        return self.save_character(character)
    
    def load(self, character_id: str) -> Optional[Character]:
        """
        Load character from storage
        
        Args:
            character_id: Character ID to load
            
        Returns:
            Character object or None if not found
        """
        # First check memory cache
        if character_id in self.characters:
            return self.characters[character_id]
        
        # Try to load from database if available
        if self.db:
            try:
                result = self.db.execute("SELECT * FROM characters WHERE id = %s", character_id)
                row = result.fetchone() if result else None
                if row:
                    # Create Character from db row
                    return Character(
                        character_id=row.get('id', character_id),
                        identity=CharacterIdentity(
                            character_id=row.get('id', character_id),
                            name=row.get('name', 'Unknown'),
                            description=row.get('description', '')
                        ),
                        mode=CharacterMode.AVATAR,
                        character_type=CharacterType.PHOTOREALISTIC
                    )
            except Exception as e:
                logger.warning(f"Database error loading character {character_id}: {e}")
        
        logger.warning(f"Character {character_id} not found")
        return None
    
    def set_pose(
        self,
        character_id: str,
        pose: str
    ) -> Optional[Character]:
        """
        Set character pose
        
        Args:
            character_id: Character ID
            pose: Pose description
            
        Returns:
            Updated Character object or None if not found
        """
        if character_id not in self.characters:
            logger.warning(f"Character {character_id} not found")
            return None
        
        character = self.characters[character_id]
        active_version = character.get_active_version()
        if active_version:
            active_version.visual.pose = pose
        character.updated_at = datetime.utcnow()
        logger.info(f"Set pose '{pose}' for character {character_id}")
        return character
    
    def set_expression(
        self,
        character_id: str,
        expression: str
    ) -> Optional[Character]:
        """
        Set character facial expression
        
        Args:
            character_id: Character ID
            expression: Expression/emotion
            
        Returns:
            Updated Character object or None if not found
        """
        if character_id not in self.characters:
            logger.warning(f"Character {character_id} not found")
            return None
        
        character = self.characters[character_id]
        active_version = character.get_active_version()
        if active_version:
            active_version.visual.emotion = expression
        character.updated_at = datetime.utcnow()
        logger.info(f"Set expression '{expression}' for character {character_id}")
        return character
    
    async def generate_animation_frames(
        self,
        character: Character,
        num_frames: int = 24
    ) -> List[Dict[str, Any]]:
        """
        Generate animation frames for a character
        
        Args:
            character: Character object
            num_frames: Number of frames to generate
            
        Returns:
            List of frame dictionaries
        """
        frames = []
        for i in range(num_frames):
            frames.append({
                "frame_number": i,
                "url": f"https://{self.s3_bucket}.s3.amazonaws.com/animation/{character.character_id}/frame_{i:04d}.png",
                "timestamp": i / 24.0
            })
        
        logger.info(f"Generated {num_frames} animation frames for character {character.character_id}")
        return frames
    
    async def generate_animation(
        self,
        character_id: str,
        animation_type: str = "walk",
        num_frames: int = 8
    ) -> List[Dict[str, Any]]:
        """
        Generate animation for a character (test-compatible wrapper)
        
        Args:
            character_id: Character ID
            animation_type: Type of animation (walk, run, idle, etc.)
            num_frames: Number of frames to generate
            
        Returns:
            List of frame dictionaries
        """
        if character_id not in self.characters:
            logger.warning(f"Character {character_id} not found")
            return []
        
        character = self.characters[character_id]
        frames = await self.generate_animation_frames(character, num_frames)
        
        # Add animation type metadata
        for frame in frames:
            frame["animation_type"] = animation_type
        
        logger.info(f"Generated {num_frames} {animation_type} animation frames for character {character_id}")
        return frames
    
    def create_relationship(
        self,
        character1_id: str,
        character2_id: str,
        relationship_type: str = None,
        **kwargs
    ) -> Relationship:
        """
        Create a relationship between two characters
        
        Args:
            character1_id: First character ID (or Character object)
            character2_id: Second character ID (or Character object)
            relationship_type: Type of relationship (friend, rival, family, etc.)
            
        Returns:
            Relationship object
        """
        # Handle if Character objects are passed instead of IDs
        if hasattr(character1_id, 'character_id'):
            character1_id = character1_id.character_id
        if hasattr(character2_id, 'character_id'):
            character2_id = character2_id.character_id
            
        rel_type = relationship_type or kwargs.get('type', 'unknown')
        
        relationship = Relationship(
            character1_id=character1_id,
            character2_id=character2_id,
            type=rel_type
        )
        
        # Store relationship
        if character1_id not in self.relationships:
            self.relationships[character1_id] = []
        self.relationships[character1_id].append(relationship.model_dump())
        
        if character2_id not in self.relationships:
            self.relationships[character2_id] = []
        self.relationships[character2_id].append(relationship.model_dump())
        
        # Also update character metadata if character exists
        if character1_id in self.characters:
            char1 = self.characters[character1_id]
            if "relationships" not in char1.metadata:
                char1.metadata["relationships"] = []
            char1.metadata["relationships"].append(relationship.model_dump())
        
        if character2_id in self.characters:
            char2 = self.characters[character2_id]
            if "relationships" not in char2.metadata:
                char2.metadata["relationships"] = []
            char2.metadata["relationships"].append(relationship.model_dump())
        
        logger.info(f"Created {rel_type} relationship between {character1_id} and {character2_id}")
        return relationship
    
    def get_relationships(self, character_id: str) -> List[Dict[str, Any]]:
        """
        Get all relationships for a character
        
        Args:
            character_id: Character ID
            
        Returns:
            List of relationships
        """
        # First check the relationships dict
        if character_id in self.relationships:
            return self.relationships[character_id]
        
        # Fall back to character metadata
        if character_id in self.characters:
            character = self.characters[character_id]
            return character.metadata.get("relationships", [])
        
        return []
    
    def to_dict(self, character: Character) -> Dict[str, Any]:
        """
        Convert character to dictionary (for serialization)
        
        Args:
            character: Character object
            
        Returns:
            Dictionary representation of character
        """
        data = character.model_dump()
        # Ensure name and id are included
        data['name'] = character.name
        data['id'] = character.id
        return data