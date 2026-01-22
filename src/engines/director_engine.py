"""
Director Engine
Film direction, shot composition, camera movements, and cinematic storytelling
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid
import logging
import asyncio

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
                    elif field_value is None and key in ['director_id', 'shot_id', 'scene_id']:
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


# Shot Types
class ShotType:
    """Camera shot types"""
    EXTREME_WIDE = "extreme_wide"
    WIDE = "wide"
    FULL = "full"
    MEDIUM = "medium"
    MEDIUM_CLOSE = "medium_close"
    CLOSE = "close"
    EXTREME_CLOSE = "extreme_close"
    TWO_SHOT = "two_shot"
    OVER_SHOULDER = "over_shoulder"
    POINT_OF_VIEW = "point_of_view"
    DUTCH_ANGLE = "dutch_angle"
    BIRD_EYE = "bird_eye"
    WORM_EYE = "worm_eye"


# Camera Movements
class CameraMovement:
    """Camera movement types"""
    STATIC = "static"
    PAN = "pan"
    TILT = "tilt"
    ZOOM = "zoom"
    DOLLY = "dolly"
    TRACK = "track"
    CRANE = "crane"
    STEADICAM = "steadicam"
    HANDHELD = "handheld"
    ORBIT = "orbit"
    PUSH_IN = "push_in"
    PULL_OUT = "pull_out"


# Camera Angles
class CameraAngle:
    """Camera angle types"""
    EYE_LEVEL = "eye_level"
    HIGH_ANGLE = "high_angle"
    LOW_ANGLE = "low_angle"
    BIRD_EYE = "bird_eye"
    WORM_EYE = "worm_eye"
    DUTCH = "dutch"
    CANTED = "canted"


# Lighting Styles
class LightingStyle:
    """Lighting style types"""
    NATURAL = "natural"
    DRAMATIC = "dramatic"
    SOFT = "soft"
    HARD = "hard"
    HIGH_KEY = "high_key"
    LOW_KEY = "low_key"
    CHIAROSCURO = "chiaroscuro"
    GOLDEN_HOUR = "golden_hour"
    BLUE_HOUR = "blue_hour"
    STUDIO = "studio"


class ShotComposition(BaseModel):
    """Shot composition details"""
    shot_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    shot_type: str
    camera_angle: str
    camera_movement: str
    lighting_style: str
    framing: Optional[str] = None
    depth_of_field: Optional[str] = None
    focus_point: Optional[str] = None
    duration: Optional[float] = None
    transition: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SceneDirection(BaseModel):
    """Scene direction instructions"""
    scene_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    scene_number: int
    location: str
    time_of_day: str
    mood: str
    shots: List[ShotComposition] = Field(default_factory=list)
    blocking: Optional[str] = None  # Character positioning
    notes: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DirectorEngine:
    """
    Director Engine
    
    Handles:
    - Shot composition and camera work
    - Scene direction
    - Camera movements and angles
    - Lighting direction
    - Visual storytelling
    - Cinematic techniques
    """
    
    def __init__(self):
        self.scenes: Dict[str, SceneDirection] = {}
        self.shots: Dict[str, ShotComposition] = {}
        self.active_projects: Dict[str, Any] = {}
        # Initialize AI Framework
        try:
            from src.services.ai_framework import get_ai_framework
            self.ai_framework = get_ai_framework()
        except ImportError:
            self.ai_framework = None
            logger.warning("AI Framework not available, using fallback")
    
    def create_shot(
        self,
        shot_type: str,
        camera_angle: str = CameraAngle.EYE_LEVEL,
        camera_movement: str = CameraMovement.STATIC,
        lighting_style: str = LightingStyle.NATURAL,
        **kwargs
    ) -> ShotComposition:
        """
        Create a shot composition
        
        Args:
            shot_type: Type of shot (wide, close, etc.)
            camera_angle: Camera angle
            camera_movement: Camera movement type
            lighting_style: Lighting style
            **kwargs: Additional shot parameters
            
        Returns:
            ShotComposition object
        """
        shot = ShotComposition(
            shot_type=shot_type,
            camera_angle=camera_angle,
            camera_movement=camera_movement,
            lighting_style=lighting_style,
            framing=kwargs.get("framing"),
            depth_of_field=kwargs.get("depth_of_field"),
            focus_point=kwargs.get("focus_point"),
            duration=kwargs.get("duration"),
            transition=kwargs.get("transition"),
            metadata=kwargs.get("metadata", {})
        )
        
        self.shots[shot.shot_id] = shot
        return shot
    
    def create_scene_direction(
        self,
        scene_number: int,
        location: str,
        time_of_day: str,
        mood: str,
        shots: Optional[List[ShotComposition]] = None,
        **kwargs
    ) -> SceneDirection:
        """
        Create scene direction
        
        Args:
            scene_number: Scene number
            location: Scene location
            time_of_day: Time of day (morning, afternoon, evening, night)
            mood: Scene mood/atmosphere
            shots: List of shots in the scene
            **kwargs: Additional scene parameters
            
        Returns:
            SceneDirection object
        """
        scene = SceneDirection(
            scene_number=scene_number,
            location=location,
            time_of_day=time_of_day,
            mood=mood,
            shots=shots or [],
            blocking=kwargs.get("blocking"),
            notes=kwargs.get("notes"),
            metadata=kwargs.get("metadata", {})
        )
        
        self.scenes[scene.scene_id] = scene
        return scene
    
    def plan_shot_sequence(
        self,
        scene_description: str,
        character_count: int = 1,
        action_type: str = "dialogue"
    ) -> List[ShotComposition]:
        """
        Plan a sequence of shots for a scene
        
        Args:
            scene_description: Description of the scene
            character_count: Number of characters
            action_type: Type of action (dialogue, action, montage, etc.)
            
        Returns:
            List of shot compositions
        """
        shots = []
        
        if action_type == "dialogue":
            if character_count == 1:
                # Single character dialogue
                shots.append(self.create_shot(
                    shot_type=ShotType.MEDIUM_CLOSE,
                    camera_angle=CameraAngle.EYE_LEVEL,
                    camera_movement=CameraMovement.STATIC,
                    lighting_style=LightingStyle.SOFT
                ))
            elif character_count == 2:
                # Two character dialogue
                shots.append(self.create_shot(
                    shot_type=ShotType.TWO_SHOT,
                    camera_angle=CameraAngle.EYE_LEVEL,
                    camera_movement=CameraMovement.STATIC
                ))
                shots.append(self.create_shot(
                    shot_type=ShotType.OVER_SHOULDER,
                    camera_angle=CameraAngle.EYE_LEVEL,
                    camera_movement=CameraMovement.PAN
                ))
        elif action_type == "action":
            # Action sequence
            shots.append(self.create_shot(
                shot_type=ShotType.WIDE,
                camera_angle=CameraAngle.EYE_LEVEL,
                camera_movement=CameraMovement.TRACK,
                lighting_style=LightingStyle.DRAMATIC
            ))
            shots.append(self.create_shot(
                shot_type=ShotType.CLOSE,
                camera_angle=CameraAngle.LOW_ANGLE,
                camera_movement=CameraMovement.HANDHELD,
                lighting_style=LightingStyle.HARD
            ))
        
        return shots
    
    def get_supported_shot_types(self) -> List[Dict[str, Any]]:
        """Get list of supported shot types"""
        return [
            {"value": ShotType.EXTREME_WIDE, "label": "Extreme Wide Shot", "description": "Very wide establishing shot"},
            {"value": ShotType.WIDE, "label": "Wide Shot", "description": "Wide establishing shot"},
            {"value": ShotType.FULL, "label": "Full Shot", "description": "Full body shot"},
            {"value": ShotType.MEDIUM, "label": "Medium Shot", "description": "Waist-up shot"},
            {"value": ShotType.MEDIUM_CLOSE, "label": "Medium Close-up", "description": "Chest-up shot"},
            {"value": ShotType.CLOSE, "label": "Close-up", "description": "Face shot"},
            {"value": ShotType.EXTREME_CLOSE, "label": "Extreme Close-up", "description": "Detail shot"},
            {"value": ShotType.TWO_SHOT, "label": "Two Shot", "description": "Two characters in frame"},
            {"value": ShotType.OVER_SHOULDER, "label": "Over Shoulder", "description": "Over shoulder shot"},
            {"value": ShotType.POINT_OF_VIEW, "label": "Point of View", "description": "POV shot"},
            {"value": ShotType.DUTCH_ANGLE, "label": "Dutch Angle", "description": "Tilted camera"},
            {"value": ShotType.BIRD_EYE, "label": "Bird's Eye View", "description": "Top-down view"},
            {"value": ShotType.WORM_EYE, "label": "Worm's Eye View", "description": "Ground-level view"}
        ]
    
    def get_supported_camera_movements(self) -> List[Dict[str, Any]]:
        """Get list of supported camera movements"""
        return [
            {"value": CameraMovement.STATIC, "label": "Static", "description": "No movement"},
            {"value": CameraMovement.PAN, "label": "Pan", "description": "Horizontal rotation"},
            {"value": CameraMovement.TILT, "label": "Tilt", "description": "Vertical rotation"},
            {"value": CameraMovement.ZOOM, "label": "Zoom", "description": "Zoom in/out"},
            {"value": CameraMovement.DOLLY, "label": "Dolly", "description": "Forward/backward movement"},
            {"value": CameraMovement.TRACK, "label": "Track", "description": "Sideways movement"},
            {"value": CameraMovement.CRANE, "label": "Crane", "description": "Vertical movement"},
            {"value": CameraMovement.STEADICAM, "label": "Steadicam", "description": "Smooth handheld"},
            {"value": CameraMovement.HANDHELD, "label": "Handheld", "description": "Handheld camera"},
            {"value": CameraMovement.ORBIT, "label": "Orbit", "description": "Circular movement"},
            {"value": CameraMovement.PUSH_IN, "label": "Push In", "description": "Move closer"},
            {"value": CameraMovement.PULL_OUT, "label": "Pull Out", "description": "Move away"}
        ]
    
    def get_supported_camera_angles(self) -> List[Dict[str, Any]]:
        """Get list of supported camera angles"""
        return [
            {"value": CameraAngle.EYE_LEVEL, "label": "Eye Level", "description": "Natural eye level"},
            {"value": CameraAngle.HIGH_ANGLE, "label": "High Angle", "description": "Looking down"},
            {"value": CameraAngle.LOW_ANGLE, "label": "Low Angle", "description": "Looking up"},
            {"value": CameraAngle.BIRD_EYE, "label": "Bird's Eye", "description": "Directly above"},
            {"value": CameraAngle.WORM_EYE, "label": "Worm's Eye", "description": "Ground level"},
            {"value": CameraAngle.DUTCH, "label": "Dutch Angle", "description": "Tilted"},
            {"value": CameraAngle.CANTED, "label": "Canted", "description": "Off-axis"}
        ]
    
    def get_supported_lighting_styles(self) -> List[Dict[str, Any]]:
        """Get list of supported lighting styles"""
        return [
            {"value": LightingStyle.NATURAL, "label": "Natural", "description": "Natural lighting"},
            {"value": LightingStyle.DRAMATIC, "label": "Dramatic", "description": "High contrast"},
            {"value": LightingStyle.SOFT, "label": "Soft", "description": "Soft diffused light"},
            {"value": LightingStyle.HARD, "label": "Hard", "description": "Hard shadows"},
            {"value": LightingStyle.HIGH_KEY, "label": "High Key", "description": "Bright, low contrast"},
            {"value": LightingStyle.LOW_KEY, "label": "Low Key", "description": "Dark, high contrast"},
            {"value": LightingStyle.CHIAROSCURO, "label": "Chiaroscuro", "description": "Strong light/dark contrast"},
            {"value": LightingStyle.GOLDEN_HOUR, "label": "Golden Hour", "description": "Warm sunset light"},
            {"value": LightingStyle.BLUE_HOUR, "label": "Blue Hour", "description": "Cool twilight light"},
            {"value": LightingStyle.STUDIO, "label": "Studio", "description": "Controlled studio lighting"}
        ]
    
    def get_scene(self, scene_id: str) -> Optional[SceneDirection]:
        """Get scene direction by ID"""
        return self.scenes.get(scene_id)
    
    def get_shot(self, shot_id: str) -> Optional[ShotComposition]:
        """Get shot composition by ID"""
        return self.shots.get(shot_id)
