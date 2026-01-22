"""
Movement Engine
Character movements, animations, gestures, and body language
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
                    elif field_value is None and key in ['movement_id', 'animation_id', 'gesture_id']:
                        setattr(self, key, str(uuid.uuid4()))
                    elif field_value is None and key in ['created_at']:
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


# Movement Types
class MovementType:
    """Character movement types"""
    WALK = "walk"
    RUN = "run"
    SIT = "sit"
    STAND = "stand"
    JUMP = "jump"
    DANCE = "dance"
    FIGHT = "fight"
    EMBRACE = "embrace"
    BOW = "bow"
    WAVE = "wave"
    POINT = "point"
    CLAP = "clap"
    NOD = "nod"
    SHAKE_HEAD = "shake_head"
    TURN = "turn"
    LOOK = "look"
    REACH = "reach"
    PICK_UP = "pick_up"
    THROW = "throw"
    CATCH = "catch"


# Gesture Types
class GestureType:
    """Hand gesture types"""
    POINT = "point"
    WAVE = "wave"
    THUMBS_UP = "thumbs_up"
    PEACE = "peace"
    FIST = "fist"
    OPEN_HAND = "open_hand"
    CLAP = "clap"
    PRAY = "pray"
    NAMASTE = "namaste"
    SALUTE = "salute"
    SHAKE_HAND = "shake_hand"
    HIGH_FIVE = "high_five"
    HUG = "hug"
    KISS = "kiss"
    BLOW_KISS = "blow_kiss"


# Body Language
class BodyLanguage:
    """Body language types"""
    CONFIDENT = "confident"
    SHY = "shy"
    ANGRY = "angry"
    HAPPY = "happy"
    SAD = "sad"
    EXCITED = "excited"
    CALM = "calm"
    NERVOUS = "nervous"
    RELAXED = "relaxed"
    TENSE = "tense"
    OPEN = "open"
    CLOSED = "closed"
    DEFENSIVE = "defensive"
    AGGRESSIVE = "aggressive"


# Animation Styles
class AnimationStyle:
    """Animation style types"""
    REALISTIC = "realistic"
    STYLIZED = "stylized"
    CARTOON = "cartoon"
    ANIME = "anime"
    SMOOTH = "smooth"
    BOUNCY = "bouncy"
    RIGID = "rigid"
    FLUID = "fluid"


class Movement(BaseModel):
    """Character movement"""
    movement_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    movement_type: str
    character_id: str
    start_position: Optional[Dict[str, float]] = None  # x, y, z
    end_position: Optional[Dict[str, float]] = None
    duration: float = 1.0
    speed: float = 1.0
    easing: Optional[str] = None
    body_language: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Gesture(BaseModel):
    """Hand gesture"""
    gesture_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    gesture_type: str
    character_id: str
    hand: str = "both"  # left, right, both
    intensity: float = 1.0
    duration: float = 1.0
    timing: Optional[float] = None  # When in dialogue/action
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AnimationSequence(BaseModel):
    """Animation sequence for a character"""
    animation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    character_id: str
    movements: List[Movement] = Field(default_factory=list)
    gestures: List[Gesture] = Field(default_factory=list)
    body_language: Optional[str] = None
    animation_style: str = AnimationStyle.REALISTIC
    duration: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MovementEngine:
    """
    Movement Engine
    
    Handles:
    - Character movements (walk, run, sit, stand, etc.)
    - Hand gestures
    - Body language
    - Animation sequences
    - Movement timing and synchronization
    - Cultural gestures (namaste, etc.)
    """
    
    def __init__(self):
        self.movements: Dict[str, Movement] = {}
        self.gestures: Dict[str, Gesture] = {}
        self.animations: Dict[str, AnimationSequence] = {}
        # Initialize AI Framework
        try:
            from src.services.ai_framework import get_ai_framework
            self.ai_framework = get_ai_framework()
        except ImportError:
            self.ai_framework = None
            logger.warning("AI Framework not available, using fallback")
    
    def create_movement(
        self,
        character_id: str,
        movement_type: str,
        duration: float = 1.0,
        speed: float = 1.0,
        **kwargs
    ) -> Movement:
        """
        Create a character movement
        
        Args:
            character_id: Character ID
            movement_type: Type of movement
            duration: Movement duration in seconds
            speed: Movement speed multiplier
            **kwargs: Additional movement parameters
            
        Returns:
            Movement object
        """
        movement = Movement(
            movement_type=movement_type,
            character_id=character_id,
            start_position=kwargs.get("start_position"),
            end_position=kwargs.get("end_position"),
            duration=duration,
            speed=speed,
            easing=kwargs.get("easing"),
            body_language=kwargs.get("body_language"),
            metadata=kwargs.get("metadata", {})
        )
        
        self.movements[movement.movement_id] = movement
        return movement
    
    def create_gesture(
        self,
        character_id: str,
        gesture_type: str,
        hand: str = "both",
        intensity: float = 1.0,
        duration: float = 1.0,
        **kwargs
    ) -> Gesture:
        """
        Create a hand gesture
        
        Args:
            character_id: Character ID
            gesture_type: Type of gesture
            hand: Which hand (left, right, both)
            intensity: Gesture intensity (0.0-2.0)
            duration: Gesture duration in seconds
            **kwargs: Additional gesture parameters
            
        Returns:
            Gesture object
        """
        gesture = Gesture(
            gesture_type=gesture_type,
            character_id=character_id,
            hand=hand,
            intensity=intensity,
            duration=duration,
            timing=kwargs.get("timing"),
            metadata=kwargs.get("metadata", {})
        )
        
        self.gestures[gesture.gesture_id] = gesture
        return gesture
    
    def create_animation_sequence(
        self,
        character_id: str,
        movements: Optional[List[Movement]] = None,
        gestures: Optional[List[Gesture]] = None,
        body_language: Optional[str] = None,
        animation_style: str = AnimationStyle.REALISTIC,
        **kwargs
    ) -> AnimationSequence:
        """
        Create an animation sequence
        
        Args:
            character_id: Character ID
            movements: List of movements
            gestures: List of gestures
            body_language: Overall body language
            animation_style: Animation style
            **kwargs: Additional parameters
            
        Returns:
            AnimationSequence object
        """
        movements = movements or []
        gestures = gestures or []
        
        # Calculate total duration
        total_duration = max(
            sum(m.duration for m in movements),
            sum(g.duration for g in gestures),
            0.0
        )
        
        animation = AnimationSequence(
            character_id=character_id,
            movements=movements,
            gestures=gestures,
            body_language=body_language,
            animation_style=animation_style,
            duration=total_duration,
            metadata=kwargs.get("metadata", {})
        )
        
        self.animations[animation.animation_id] = animation
        return animation
    
    def plan_movements_for_dialogue(
        self,
        character_id: str,
        dialogue_text: str,
        emotion: str = "neutral"
    ) -> AnimationSequence:
        """
        Plan movements and gestures for dialogue
        
        Args:
            character_id: Character ID
            dialogue_text: Dialogue text
            emotion: Emotion of the dialogue
            
        Returns:
            AnimationSequence with appropriate movements
        """
        movements = []
        gestures = []
        
        # Add body language based on emotion
        body_language_map = {
            "happy": BodyLanguage.HAPPY,
            "sad": BodyLanguage.SAD,
            "angry": BodyLanguage.ANGRY,
            "excited": BodyLanguage.EXCITED,
            "calm": BodyLanguage.CALM,
            "nervous": BodyLanguage.NERVOUS
        }
        body_language = body_language_map.get(emotion, BodyLanguage.CALM)
        
        # Add gestures based on dialogue content
        words = dialogue_text.lower().split()
        if any(word in words for word in ["here", "there", "this", "that"]):
            gestures.append(self.create_gesture(
                character_id=character_id,
                gesture_type=GestureType.POINT,
                duration=1.0
            ))
        
        if any(word in words for word in ["hello", "hi", "greet"]):
            gestures.append(self.create_gesture(
                character_id=character_id,
                gesture_type=GestureType.WAVE,
                duration=1.5
            ))
        
        if any(word in words for word in ["yes", "agree", "okay"]):
            movements.append(self.create_movement(
                character_id=character_id,
                movement_type=MovementType.NOD,
                duration=0.5
            ))
        
        if any(word in words for word in ["no", "disagree"]):
            movements.append(self.create_movement(
                character_id=character_id,
                movement_type=MovementType.SHAKE_HEAD,
                duration=0.5
            ))
        
        return self.create_animation_sequence(
            character_id=character_id,
            movements=movements,
            gestures=gestures,
            body_language=body_language
        )
    
    def get_supported_movements(self) -> List[Dict[str, Any]]:
        """Get list of supported movement types"""
        return [
            {"value": MovementType.WALK, "label": "Walk", "description": "Walking movement"},
            {"value": MovementType.RUN, "label": "Run", "description": "Running movement"},
            {"value": MovementType.SIT, "label": "Sit", "description": "Sitting down"},
            {"value": MovementType.STAND, "label": "Stand", "description": "Standing up"},
            {"value": MovementType.JUMP, "label": "Jump", "description": "Jumping"},
            {"value": MovementType.DANCE, "label": "Dance", "description": "Dancing"},
            {"value": MovementType.FIGHT, "label": "Fight", "description": "Fighting"},
            {"value": MovementType.EMBRACE, "label": "Embrace", "description": "Hugging"},
            {"value": MovementType.BOW, "label": "Bow", "description": "Bowing"},
            {"value": MovementType.WAVE, "label": "Wave", "description": "Waving"},
            {"value": MovementType.POINT, "label": "Point", "description": "Pointing"},
            {"value": MovementType.CLAP, "label": "Clap", "description": "Clapping"},
            {"value": MovementType.NOD, "label": "Nod", "description": "Nodding head"},
            {"value": MovementType.SHAKE_HEAD, "label": "Shake Head", "description": "Shaking head"},
            {"value": MovementType.TURN, "label": "Turn", "description": "Turning"},
            {"value": MovementType.LOOK, "label": "Look", "description": "Looking"},
            {"value": MovementType.REACH, "label": "Reach", "description": "Reaching"},
            {"value": MovementType.PICK_UP, "label": "Pick Up", "description": "Picking up object"},
            {"value": MovementType.THROW, "label": "Throw", "description": "Throwing"},
            {"value": MovementType.CATCH, "label": "Catch", "description": "Catching"}
        ]
    
    def get_supported_gestures(self) -> List[Dict[str, Any]]:
        """Get list of supported gesture types"""
        return [
            {"value": GestureType.POINT, "label": "Point", "description": "Pointing gesture"},
            {"value": GestureType.WAVE, "label": "Wave", "description": "Waving gesture"},
            {"value": GestureType.THUMBS_UP, "label": "Thumbs Up", "description": "Thumbs up"},
            {"value": GestureType.PEACE, "label": "Peace", "description": "Peace sign"},
            {"value": GestureType.FIST, "label": "Fist", "description": "Fist"},
            {"value": GestureType.OPEN_HAND, "label": "Open Hand", "description": "Open hand"},
            {"value": GestureType.CLAP, "label": "Clap", "description": "Clapping"},
            {"value": GestureType.PRAY, "label": "Pray", "description": "Praying hands"},
            {"value": GestureType.NAMASTE, "label": "Namaste", "description": "Namaste gesture"},
            {"value": GestureType.SALUTE, "label": "Salute", "description": "Saluting"},
            {"value": GestureType.SHAKE_HAND, "label": "Shake Hand", "description": "Handshake"},
            {"value": GestureType.HIGH_FIVE, "label": "High Five", "description": "High five"},
            {"value": GestureType.HUG, "label": "Hug", "description": "Hugging"},
            {"value": GestureType.KISS, "label": "Kiss", "description": "Kissing"},
            {"value": GestureType.BLOW_KISS, "label": "Blow Kiss", "description": "Blowing kiss"}
        ]
    
    def get_supported_body_languages(self) -> List[Dict[str, Any]]:
        """Get list of supported body language types"""
        return [
            {"value": BodyLanguage.CONFIDENT, "label": "Confident"},
            {"value": BodyLanguage.SHY, "label": "Shy"},
            {"value": BodyLanguage.ANGRY, "label": "Angry"},
            {"value": BodyLanguage.HAPPY, "label": "Happy"},
            {"value": BodyLanguage.SAD, "label": "Sad"},
            {"value": BodyLanguage.EXCITED, "label": "Excited"},
            {"value": BodyLanguage.CALM, "label": "Calm"},
            {"value": BodyLanguage.NERVOUS, "label": "Nervous"},
            {"value": BodyLanguage.RELAXED, "label": "Relaxed"},
            {"value": BodyLanguage.TENSE, "label": "Tense"},
            {"value": BodyLanguage.OPEN, "label": "Open"},
            {"value": BodyLanguage.CLOSED, "label": "Closed"},
            {"value": BodyLanguage.DEFENSIVE, "label": "Defensive"},
            {"value": BodyLanguage.AGGRESSIVE, "label": "Aggressive"}
        ]
    
    def get_movement(self, movement_id: str) -> Optional[Movement]:
        """Get movement by ID"""
        return self.movements.get(movement_id)
    
    def get_gesture(self, gesture_id: str) -> Optional[Gesture]:
        """Get gesture by ID"""
        return self.gestures.get(gesture_id)
    
    def get_animation(self, animation_id: str) -> Optional[AnimationSequence]:
        """Get animation sequence by ID"""
        return self.animations.get(animation_id)
