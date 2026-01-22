"""
Screenplay Engine
Screenplay writing, formatting, and structure management
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid
import logging

# Handle optional pydantic import
try:
    from pydantic import BaseModel, Field
except ImportError:
    class BaseModel:
        def __init__(self, **kwargs):
            annotations = getattr(self.__class__, '__annotations__', {})
            for key, value in kwargs.items():
                setattr(self, key, value)
            for key, field_type in annotations.items():
                if not hasattr(self, key):
                    field_value = getattr(self.__class__, key, None)
                    if callable(field_value):
                        setattr(self, key, field_value())
                    elif field_value is None and key in ['screenplay_id', 'scene_id', 'element_id']:
                        setattr(self, key, str(uuid.uuid4()))
                    elif field_value is None and key in ['created_at', 'updated_at']:
                        setattr(self, key, datetime.utcnow())
                    elif field_value is None and key in ['metadata']:
                        setattr(self, key, {})
    
    def Field(default=..., default_factory=None, **kwargs):
        if default_factory is not None:
            return default_factory
        if default is not ...:
            return default
        return None

logger = logging.getLogger(__name__)


# Screenplay Elements
class ElementType:
    """Screenplay element types"""
    SCENE_HEADING = "scene_heading"
    ACTION = "action"
    CHARACTER = "character"
    DIALOGUE = "dialogue"
    PARENTHETICAL = "parenthetical"
    TRANSITION = "transition"
    SHOT = "shot"
    NOTE = "note"


class ScreenplayElement(BaseModel):
    """Individual screenplay element"""
    element_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    element_type: str
    content: str
    scene_number: Optional[int] = None
    character_name: Optional[str] = None
    order: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Scene(BaseModel):
    """Screenplay scene"""
    scene_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    scene_number: int
    scene_heading: str  # INT./EXT. LOCATION - TIME
    elements: List[ScreenplayElement] = Field(default_factory=list)
    synopsis: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Screenplay(BaseModel):
    """Complete screenplay"""
    screenplay_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    author: Optional[str] = None
    version: str = "1.0"
    scenes: List[Scene] = Field(default_factory=list)
    characters: List[str] = Field(default_factory=list)
    genre: Optional[str] = None
    logline: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ScreenplayEngine:
    """
    Screenplay Engine
    
    Handles:
    - Screenplay formatting (industry standard)
    - Scene structure
    - Dialogue formatting
    - Character management
    - Scene headings
    - Action lines
    - Transitions
    """
    
    def __init__(self):
        self.screenplays: Dict[str, Screenplay] = {}
        self.scenes: Dict[str, Scene] = {}
        # Initialize AI Framework
        try:
            from src.services.ai_framework import get_ai_framework
            self.ai_framework = get_ai_framework()
        except ImportError:
            self.ai_framework = None
            logger.warning("AI Framework not available, using fallback")
    
    def create_screenplay(
        self,
        title: str,
        author: Optional[str] = None,
        genre: Optional[str] = None,
        logline: Optional[str] = None
    ) -> Screenplay:
        """
        Create a new screenplay
        
        Args:
            title: Screenplay title
            author: Author name
            genre: Genre (drama, comedy, action, etc.)
            logline: One-line summary
            
        Returns:
            Screenplay object
        """
        screenplay = Screenplay(
            title=title,
            author=author,
            genre=genre,
            logline=logline
        )
        
        self.screenplays[screenplay.screenplay_id] = screenplay
        return screenplay
    
    def add_scene(
        self,
        screenplay_id: str,
        scene_heading: str,
        synopsis: Optional[str] = None
    ) -> Scene:
        """
        Add a scene to screenplay
        
        Args:
            screenplay_id: Screenplay ID
            scene_heading: Scene heading (INT./EXT. LOCATION - TIME)
            synopsis: Scene synopsis
            
        Returns:
            Scene object
        """
        screenplay = self.screenplays.get(screenplay_id)
        if not screenplay:
            raise ValueError(f"Screenplay {screenplay_id} not found")
        
        scene_number = len(screenplay.scenes) + 1
        scene = Scene(
            scene_number=scene_number,
            scene_heading=scene_heading,
            synopsis=synopsis
        )
        
        screenplay.scenes.append(scene)
        screenplay.updated_at = datetime.utcnow()
        self.scenes[scene.scene_id] = scene
        
        return scene
    
    def add_action(
        self,
        scene_id: str,
        action_text: str
    ) -> ScreenplayElement:
        """
        Add action line to scene
        
        Args:
            scene_id: Scene ID
            action_text: Action description
            
        Returns:
            ScreenplayElement
        """
        scene = self.scenes.get(scene_id)
        if not scene:
            raise ValueError(f"Scene {scene_id} not found")
        
        element = ScreenplayElement(
            element_type=ElementType.ACTION,
            content=action_text,
            scene_number=scene.scene_number,
            order=len(scene.elements)
        )
        
        scene.elements.append(element)
        return element
    
    def add_dialogue(
        self,
        scene_id: str,
        character_name: str,
        dialogue_text: Optional[str] = None,
        parenthetical: Optional[str] = None,
        generate: bool = False
    ) -> ScreenplayElement:
        """
        Add dialogue to scene
        
        Args:
            scene_id: Scene ID
            character_name: Character name
            dialogue_text: Dialogue text (optional if generate=True)
            parenthetical: Parenthetical (emotion/direction)
            generate: If True, generate dialogue using AI
            
        Returns:
            ScreenplayElement
        """
        scene = self.scenes.get(scene_id)
        if not scene:
            raise ValueError(f"Scene {scene_id} not found")
        
        # Generate dialogue using AI Framework if requested
        if generate and self.ai_framework and not dialogue_text:
            try:
                import asyncio
                prompt = f"Generate screenplay dialogue for {character_name}"
                if parenthetical:
                    prompt += f" ({parenthetical})"
                prompt += f" in scene: {scene.scene_heading}"
                if scene.synopsis:
                    prompt += f"\nScene context: {scene.synopsis}"
                
                try:
                    loop = asyncio.get_event_loop()
                    if not loop.is_running():
                        dialogue_text = loop.run_until_complete(
                            self.ai_framework.generate_text(
                                prompt=prompt,
                                provider="openai",
                                model="gpt-4",
                                max_tokens=200,
                                temperature=0.8
                            )
                        )
                except RuntimeError:
                    dialogue_text = asyncio.run(
                        self.ai_framework.generate_text(
                            prompt=prompt,
                            provider="openai",
                            model="gpt-4",
                            max_tokens=200,
                            temperature=0.8
                        )
                    )
            except Exception as e:
                logger.warning(f"AI framework dialogue generation failed: {e}, using provided text")
        
        if not dialogue_text:
            dialogue_text = "[Dialogue text required]"
        
        # Add character to screenplay if not exists
        screenplay = self._find_screenplay_by_scene(scene_id)
        if screenplay and character_name not in screenplay.characters:
            screenplay.characters.append(character_name)
        
        elements = []
        
        # Character name
        char_element = ScreenplayElement(
            element_type=ElementType.CHARACTER,
            content=character_name,
            scene_number=scene.scene_number,
            character_name=character_name,
            order=len(scene.elements)
        )
        elements.append(char_element)
        scene.elements.append(char_element)
        
        # Parenthetical (if provided)
        if parenthetical:
            parent_element = ScreenplayElement(
                element_type=ElementType.PARENTHETICAL,
                content=parenthetical,
                scene_number=scene.scene_number,
                character_name=character_name,
                order=len(scene.elements)
            )
            elements.append(parent_element)
            scene.elements.append(parent_element)
        
        # Dialogue
        dialogue_element = ScreenplayElement(
            element_type=ElementType.DIALOGUE,
            content=dialogue_text,
            scene_number=scene.scene_number,
            character_name=character_name,
            order=len(scene.elements)
        )
        elements.append(dialogue_element)
        scene.elements.append(dialogue_element)
        
        return dialogue_element
    
    def format_screenplay(self, screenplay_id: str) -> str:
        """
        Format screenplay in industry standard format
        
        Args:
            screenplay_id: Screenplay ID
            
        Returns:
            Formatted screenplay text
        """
        screenplay = self.screenplays.get(screenplay_id)
        if not screenplay:
            raise ValueError(f"Screenplay {screenplay_id} not found")
        
        lines = []
        
        # Title page
        lines.append(screenplay.title.upper())
        lines.append("")
        if screenplay.author:
            lines.append(f"by {screenplay.author}")
        lines.append("")
        lines.append("=" * 80)
        lines.append("")
        
        # Scenes
        for scene in screenplay.scenes:
            # Scene heading
            lines.append(scene.scene_heading.upper())
            lines.append("")
            
            # Elements
            for element in scene.elements:
                if element.element_type == ElementType.ACTION:
                    lines.append(element.content)
                    lines.append("")
                elif element.element_type == ElementType.CHARACTER:
                    lines.append(element.content.upper())
                elif element.element_type == ElementType.PARENTHETICAL:
                    lines.append(f"({element.content})")
                elif element.element_type == ElementType.DIALOGUE:
                    lines.append(element.content)
                    lines.append("")
                elif element.element_type == ElementType.TRANSITION:
                    lines.append(element.content.upper())
                    lines.append("")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def _find_screenplay_by_scene(self, scene_id: str) -> Optional[Screenplay]:
        """Find screenplay containing a scene"""
        for screenplay in self.screenplays.values():
            if any(s.scene_id == scene_id for s in screenplay.scenes):
                return screenplay
        return None
    
    def get_screenplay(self, screenplay_id: str) -> Optional[Screenplay]:
        """Get screenplay by ID"""
        return self.screenplays.get(screenplay_id)
    
    def get_scene(self, scene_id: str) -> Optional[Scene]:
        """Get scene by ID"""
        return self.scenes.get(scene_id)
    
    def list_screenplays(self) -> List[Screenplay]:
        """List all screenplays"""
        return list(self.screenplays.values())
