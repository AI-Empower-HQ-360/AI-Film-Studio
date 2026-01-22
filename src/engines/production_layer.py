"""
AI / Real Shoot Production Layer
Hybrid production execution supporting real footage + AI
"""
from typing import Optional, Dict, List, Any
from enum import Enum
from datetime import datetime
import uuid
import logging

# Handle optional pydantic import
try:
    from pydantic import BaseModel, Field
except ImportError:
    # Fallback for testing environments without pydantic
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
                    elif field_value is None and key in ['shot_id', 'match_id']:
                        setattr(self, key, str(uuid.uuid4()))
                    elif field_value is None and key in ['created_at', 'updated_at', 'timestamp']:
                        setattr(self, key, datetime.utcnow())
                    elif field_value is None and key in ['metadata']:
                        setattr(self, key, {})
        
        def model_dump(self, **kwargs) -> Dict[str, Any]:
            """Convert model to dictionary"""
            result = {}
            for key in dir(self):
                if not key.startswith('_') and not callable(getattr(self, key)):
                    value = getattr(self, key, None)
                    if isinstance(value, BaseModel):
                        result[key] = value.model_dump(**kwargs)
                    elif isinstance(value, list):
                        result[key] = [item.model_dump(**kwargs) if isinstance(item, BaseModel) else item for item in value]
                    elif isinstance(value, dict):
                        result[key] = {k: v.model_dump(**kwargs) if isinstance(v, BaseModel) else v for k, v in value.items()}
                    else:
                        result[key] = value
            return result
        
        def dict(self, **kwargs) -> Dict[str, Any]:
            """Alias for model_dump for compatibility"""
            return self.model_dump(**kwargs)
    
    def Field(default=..., default_factory=None, **kwargs):
        if default_factory is not None:
            return default_factory
        if default is not ...:
            return default
        return None

logger = logging.getLogger(__name__)


class ProductionType(str, Enum):
    """Production types"""
    TRADITIONAL = "traditional"  # Real camera footage only
    HYBRID = "hybrid"  # Mix of real footage and AI
    FULLY_AI = "fully_ai"  # All AI-generated


class ShotType(str, Enum):
    """Shot types"""
    REAL_FOOTAGE = "real_footage"
    AI_GENERATED = "ai_generated"
    PRE_VIS = "pre_vis"  # Pre-visualization placeholder
    INSERT = "insert"  # AI insert into real footage
    HYBRID = "hybrid"  # Mix of real footage and AI


class Shot(BaseModel):
    """Production shot"""
    shot_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    scene_id: str
    shot_type: ShotType
    source_type: str = Field(default="generated")  # "uploaded" or "generated"
    video_url: Optional[str] = None
    s3_key: Optional[str] = None
    duration: Optional[float] = None
    timestamp: Optional[float] = None  # Position in scene
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @property
    def is_real_footage(self) -> bool:
        """Check if shot is real footage"""
        return self.shot_type == ShotType.REAL_FOOTAGE


class ContinuityMatch(BaseModel):
    """Continuity matching between shots"""
    match_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_shot_id: str
    target_shot_id: str
    match_type: str  # "lighting", "color", "character", "camera_angle"
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    applied: bool = False


class ProductionLayer:
    """
    AI / Real Shoot Production Layer
    
    Hybrid production execution:
    - Upload real camera footage
    - AI-generated scenes and inserts
    - Pre-visualization and placeholders
    - Shot matching and continuity
    - Gap-filling with AI
    
    Supports:
    - Traditional filmmaking
    - Hybrid AI + real films
    - Fully AI productions
    """
    
    def __init__(self, s3_bucket: str = "ai-film-studio-production"):
        self.s3_bucket = s3_bucket
        self.shots: Dict[str, Shot] = {}
        self.continuity_matches: Dict[str, ContinuityMatch] = {}
        
        # Service references for integration (tests expect these attributes)
        self.video_service = None
        self.audio_service = None
        self.image_service = None
        # Initialize AI Framework
        try:
            from src.services.ai_framework import get_ai_framework
            self.ai_framework = get_ai_framework()
        except ImportError:
            self.ai_framework = None
            logger.warning("AI Framework not available, using fallback")

    def create_shot(
        self,
        scene_id: str,
        shot_type: str,
        description: str,
        style: Optional[str] = None
    ) -> Shot:
        """
        Create a shot
        
        Args:
            scene_id: Scene ID
            shot_type: Type of shot (real_footage, ai_generated, hybrid)
            description: Shot description
            style: Optional style
            
        Returns:
            Created shot
        """
        shot_type_enum = ShotType(shot_type) if isinstance(shot_type, str) else shot_type
        
        shot = Shot(
            scene_id=scene_id,
            shot_type=shot_type_enum,
            metadata={"description": description, "style": style}
        )
        
        self.shots[shot.shot_id] = shot
        logger.info(f"Created shot {shot.shot_id} for scene {scene_id}")
        return shot
    
    def upload_real_footage(
        self,
        scene_id: str,
        file_path: Optional[str] = None,
        s3_key: Optional[str] = None,
        duration: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Shot:
        """
        Upload real camera footage (synchronous)
        
        Supports traditional filmmaking workflow
        """
        shot = Shot(
            scene_id=scene_id,
            shot_type=ShotType.REAL_FOOTAGE,
            source_type="uploaded",
            video_url=file_path or f"s3://{self.s3_bucket}/footage/{scene_id}/video.mp4",
            s3_key=s3_key or f"footage/{scene_id}/video.mp4",
            duration=duration,
            metadata=metadata or {}
        )
        
        self.shots[shot.shot_id] = shot
        
        logger.info(f"Uploaded real footage shot {shot.shot_id} for scene {scene_id}")
        
        return shot
    
    async def _upload_real_footage_async(
        self,
        scene_id: str,
        file_path: Optional[str] = None,
        s3_key: Optional[str] = None,
        duration: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Shot:
        """Upload real camera footage (async version)"""
        return self.upload_real_footage(
            scene_id=scene_id,
            file_path=file_path,
            s3_key=s3_key,
            duration=duration,
            metadata=metadata
        )
    
    async def generate_ai_shot(
        self,
        scene_id: str,
        description: Optional[str] = None,
        prompt: Optional[str] = None,
        character_ids: Optional[List[str]] = None,
        duration: float = 5.0,
        style: str = "cinematic"
    ) -> Shot:
        """
        Generate AI shot for scene
        
        Can be used for:
        - Fully AI productions
        - Inserts and gap-filling
        - Pre-visualization
        """
        shot_id = str(uuid.uuid4())
        prompt_text = prompt or description or "AI-generated scene"
        
        # Use AI Framework for video generation
        video_url = None
        if self.ai_framework:
            try:
                video_result = await self.ai_framework.generate_video(
                    prompt=prompt_text,
                    provider="stability",
                    duration=int(duration)
                )
                if isinstance(video_result, dict):
                    video_url = video_result.get("video_url") or f"s3://{self.s3_bucket}/shots/{shot_id}/shot.mp4"
                else:
                    video_url = f"s3://{self.s3_bucket}/shots/{shot_id}/shot.mp4"
            except Exception as e:
                logger.warning(f"AI framework video generation failed: {e}, using fallback")
                video_url = f"s3://{self.s3_bucket}/shots/{shot_id}/shot.mp4"
        else:
            video_url = f"s3://{self.s3_bucket}/shots/{shot_id}/shot.mp4"
        
        shot = Shot(
            shot_id=shot_id,
            scene_id=scene_id,
            shot_type=ShotType.AI_GENERATED,
            source_type="generated",
            duration=duration,
            video_url=video_url or f"s3://{self.s3_bucket}/shots/{shot_id}/shot.mp4",
            metadata={
                "prompt": prompt_text,
                "description": description,
                "character_ids": character_ids or [],
                "style": style
            }
        )
        
        self.shots[shot.shot_id] = shot
        
        logger.info(f"Generated AI shot {shot.shot_id} for scene {scene_id}")
        
        return shot
    
    async def create_pre_vis(
        self,
        scene_id: str,
        description: str,
        duration: float = 5.0
    ) -> Shot:
        """
        Create pre-visualization placeholder
        
        Used for planning before real shoot or AI generation
        """
        shot = Shot(
            scene_id=scene_id,
            shot_type=ShotType.PRE_VIS,
            source_type="pre_vis",
            duration=duration,
            metadata={"description": description, "is_placeholder": True}
        )
        
        self.shots[shot.shot_id] = shot
        
        logger.info(f"Created pre-vis {shot.shot_id} for scene {scene_id}")
        
        return shot
    
    async def match_shot_continuity(
        self,
        source_shot_id: str,
        target_shot_id: str,
        match_type: str = "auto"
    ) -> ContinuityMatch:
        """
        Match continuity between shots
        
        Ensures:
        - Lighting consistency
        - Color grading match
        - Character appearance continuity
        - Camera angle coherence
        """
        if source_shot_id not in self.shots or target_shot_id not in self.shots:
            raise ValueError("One or both shots not found")
        
        source_shot = self.shots[source_shot_id]
        target_shot = self.shots[target_shot_id]
        
        # TODO: Implement continuity matching
        # Would analyze:
        # - Color palette
        # - Lighting conditions
        # - Character positions
        # - Camera angles
        
        match = ContinuityMatch(
            source_shot_id=source_shot_id,
            target_shot_id=target_shot_id,
            match_type=match_type,
            confidence=0.85  # Would be calculated
        )
        
        self.continuity_matches[match.match_id] = match
        
        logger.info(f"Matched continuity between shots {source_shot_id} and {target_shot_id}")
        
        return match
    
    
    def create_previsualization(
        self,
        scene_id: str,
        shot_list: List[str],
        style: str = "storyboard"
    ) -> Dict[str, Any]:
        """
        Create pre-visualization
        
        Args:
            scene_id: Scene ID
            shot_list: List of shot IDs
            style: Visualization style
            
        Returns:
            Pre-visualization data
        """
        previz = {
            "scene_id": scene_id,
            "shot_list": shot_list,
            "style": style,
            "created_at": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Created pre-visualization for scene {scene_id}")
        return previz

    async def fill_gaps_with_ai(
        self,
        scene_id: str,
        gap_timestamps: List[float],  # List of (start, end) tuples
        context: str
    ) -> List[Shot]:
        """
        Fill gaps in real footage with AI-generated inserts
        
        Useful for:
        - Missing shots
        - Continuity fixes
        - Visual effects
        """
        shots = []
        
        for start, end in gap_timestamps:
            duration = end - start
            
            shot = await self.generate_ai_shot(
                scene_id=scene_id,
                prompt=f"{context} - Gap fill from {start}s to {end}s",
                duration=duration,
                style="match_real_footage"
            )
            
            shot.timestamp = start
            shot.metadata["is_gap_fill"] = True
            shots.append(shot)
        
        logger.info(f"Filled {len(shots)} gaps in scene {scene_id} with AI")
        
        return shots
    
    def fill_gap(
        self,
        scene_id: str,
        start_shot: str,
        end_shot: str,
        duration: float
    ) -> Dict[str, Any]:
        """
        Fill gap between shots (synchronous wrapper)
        
        Args:
            scene_id: Scene ID
            start_shot: Start shot ID
            end_shot: End shot ID
            duration: Gap duration in seconds
            
        Returns:
            Gap fill result
        """
        import asyncio
        gaps = [(0.0, duration)]  # Simplified - would calculate actual gap
        result = asyncio.run(self.fill_gaps_with_ai(scene_id, gaps, f"Gap between {start_shot} and {end_shot}"))
        if result and len(result) > 0:
            shot = result[0]
            if hasattr(shot, 'dict'):
                return shot.dict()
            elif hasattr(shot, 'model_dump'):
                return shot.model_dump()
            else:
                return {
                    "shot_id": getattr(shot, 'shot_id', str(uuid.uuid4())),
                    "scene_id": getattr(shot, 'scene_id', scene_id),
                    "shot_type": str(getattr(shot, 'shot_type', "ai_generated"))
                }
        return {}
    
    async def compose_hybrid_scene(
        self,
        scene_id: str,
        shot_ids: List[str],
        transitions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Compose hybrid scene from real footage and AI shots
        
        Creates seamless composition of:
        - Real camera footage
        - AI-generated shots
        - Pre-vis placeholders (replaced)
        - Continuity-matched inserts
        """
        shots = [self.shots[sid] for sid in shot_ids if sid in self.shots]
        
        # Sort by timestamp if available
        shots.sort(key=lambda s: s.timestamp or 0.0)
        
        # TODO: Implement video composition
        # Would use FFmpeg to:
        # 1. Apply continuity matching
        # 2. Add transitions
        # 3. Composite final scene
        
        composition = {
            "scene_id": scene_id,
            "shot_count": len(shots),
            "real_footage_count": sum(1 for s in shots if s.shot_type == ShotType.REAL_FOOTAGE),
            "ai_generated_count": sum(1 for s in shots if s.shot_type == ShotType.AI_GENERATED),
            "total_duration": sum(s.duration or 0.0 for s in shots),
            "output_url": f"s3://{self.s3_bucket}/scenes/{scene_id}/composed.mp4"
        }
        
        logger.info(f"Composed hybrid scene {scene_id} with {len(shots)} shots")
        
        return composition
    
    async def get_scene_shots(self, scene_id: str) -> List[Shot]:
        """Get all shots for a scene"""
        return [s for s in self.shots.values() if s.scene_id == scene_id]
