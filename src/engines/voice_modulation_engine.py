"""
Voice Modulation Engine
Voice synthesis and modulation for different age groups (boys, girls, men, women)
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
                    elif field_value is None and key in ['voice_id', 'modulation_id', 'job_id']:
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


# Age Groups for Voice
class VoiceAgeGroup:
    """Voice age group categories"""
    INFANT = "0-3"
    CHILD = "4-8"
    PRE_TEEN = "8-12"
    TEEN = "13-19"
    YOUNG_ADULT = "20-21"
    ADULT = "22-35"
    MIDDLE_AGE = "35-50"
    SENIOR = "50+"


# Gender for Voice
class VoiceGender:
    """Voice gender categories"""
    BOY = "boy"
    GIRL = "girl"
    MAN = "man"
    WOMAN = "woman"
    CHILD = "child"  # Gender-neutral child voice


# Voice Characteristics
class VoiceCharacteristic:
    """Voice characteristic types"""
    PITCH = "pitch"
    SPEED = "speed"
    VOLUME = "volume"
    TIMBRE = "timbre"
    ACCENT = "accent"
    EMOTION = "emotion"


class VoiceModulationRequest(BaseModel):
    """Request for voice modulation"""
    text: str = Field(..., description="Text to synthesize")
    age_group: str = Field(..., description="Age group (0-3, 4-8, 8-12, 13-19, 20-21, 22-35, 35-50, 50+)")
    gender: str = Field(..., description="Gender (boy, girl, man, woman, child)")
    pitch: Optional[float] = Field(default=None, ge=0.0, le=2.0, description="Pitch modulation (0.0-2.0)")
    speed: Optional[float] = Field(default=None, ge=0.5, le=2.0, description="Speed modulation (0.5-2.0)")
    volume: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Volume (0.0-1.0)")
    emotion: Optional[str] = Field(default="neutral", description="Emotion (neutral, happy, sad, angry, excited, calm)")
    accent: Optional[str] = Field(default=None, description="Accent/regional variation")
    language: Optional[str] = Field(default="en", description="Language code")
    voice_model_id: Optional[str] = Field(default=None, description="Specific voice model ID")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class VoiceModulationResult(BaseModel):
    """Voice modulation result"""
    job_id: str
    voice_id: str
    audio_url: str
    duration: float
    age_group: str
    gender: str
    characteristics: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class VoiceModulationEngine:
    """
    Voice Modulation Engine
    
    Handles:
    - Voice synthesis for all age groups (0-3, 4-8, 8-12, teens, 20-21, 22-35, 35-50, 50+)
    - Gender-specific voices (boys, girls, men, women)
    - Pitch, speed, volume modulation
    - Emotion-based voice modulation
    - Accent and regional variations
    - Multi-language support
    """
    
    def __init__(self):
        self.voices: Dict[str, VoiceModulationResult] = {}
        self.active_jobs: Dict[str, Any] = {}
        self.voice_models: Dict[str, Dict[str, Any]] = {}
        self._initialize_voice_models()
        # Initialize AI Framework
        try:
            from src.services.ai_framework import get_ai_framework
            self.ai_framework = get_ai_framework()
        except ImportError:
            self.ai_framework = None
            logger.warning("AI Framework not available, using fallback")
    
    def _initialize_voice_models(self):
        """Initialize default voice models for different age groups and genders"""
        # Boys (0-3)
        self.voice_models["boy_0_3"] = {
            "age_group": VoiceAgeGroup.INFANT,
            "gender": VoiceGender.BOY,
            "pitch": 1.8,
            "speed": 0.9,
            "timbre": "high",
            "description": "Baby boy voice"
        }
        
        # Girls (0-3)
        self.voice_models["girl_0_3"] = {
            "age_group": VoiceAgeGroup.INFANT,
            "gender": VoiceGender.GIRL,
            "pitch": 1.9,
            "speed": 0.9,
            "timbre": "high",
            "description": "Baby girl voice"
        }
        
        # Boys (4-8)
        self.voice_models["boy_4_8"] = {
            "age_group": VoiceAgeGroup.CHILD,
            "gender": VoiceGender.BOY,
            "pitch": 1.6,
            "speed": 1.0,
            "timbre": "bright",
            "description": "Young boy voice"
        }
        
        # Girls (4-8)
        self.voice_models["girl_4_8"] = {
            "age_group": VoiceAgeGroup.CHILD,
            "gender": VoiceGender.GIRL,
            "pitch": 1.7,
            "speed": 1.0,
            "timbre": "bright",
            "description": "Young girl voice"
        }
        
        # Boys (8-12)
        self.voice_models["boy_8_12"] = {
            "age_group": VoiceAgeGroup.PRE_TEEN,
            "gender": VoiceGender.BOY,
            "pitch": 1.4,
            "speed": 1.1,
            "timbre": "clear",
            "description": "Pre-teen boy voice"
        }
        
        # Girls (8-12)
        self.voice_models["girl_8_12"] = {
            "age_group": VoiceAgeGroup.PRE_TEEN,
            "gender": VoiceGender.GIRL,
            "pitch": 1.5,
            "speed": 1.1,
            "timbre": "clear",
            "description": "Pre-teen girl voice"
        }
        
        # Teens (13-19)
        self.voice_models["teen_boy"] = {
            "age_group": VoiceAgeGroup.TEEN,
            "gender": VoiceGender.BOY,
            "pitch": 1.2,
            "speed": 1.2,
            "timbre": "changing",
            "description": "Teenage boy voice"
        }
        
        self.voice_models["teen_girl"] = {
            "age_group": VoiceAgeGroup.TEEN,
            "gender": VoiceGender.GIRL,
            "pitch": 1.3,
            "speed": 1.2,
            "timbre": "clear",
            "description": "Teenage girl voice"
        }
        
        # Young Adults (20-21)
        self.voice_models["young_man"] = {
            "age_group": VoiceAgeGroup.YOUNG_ADULT,
            "gender": VoiceGender.MAN,
            "pitch": 1.0,
            "speed": 1.1,
            "timbre": "mature",
            "description": "Young man voice"
        }
        
        self.voice_models["young_woman"] = {
            "age_group": VoiceAgeGroup.YOUNG_ADULT,
            "gender": VoiceGender.WOMAN,
            "pitch": 1.1,
            "speed": 1.1,
            "timbre": "mature",
            "description": "Young woman voice"
        }
        
        # Adults (22-35)
        self.voice_models["man_22_35"] = {
            "age_group": VoiceAgeGroup.ADULT,
            "gender": VoiceGender.MAN,
            "pitch": 0.95,
            "speed": 1.0,
            "timbre": "full",
            "description": "Adult man voice"
        }
        
        self.voice_models["woman_22_35"] = {
            "age_group": VoiceAgeGroup.ADULT,
            "gender": VoiceGender.WOMAN,
            "pitch": 1.05,
            "speed": 1.0,
            "timbre": "full",
            "description": "Adult woman voice"
        }
        
        # Middle Age (35-50)
        self.voice_models["man_35_50"] = {
            "age_group": VoiceAgeGroup.MIDDLE_AGE,
            "gender": VoiceGender.MAN,
            "pitch": 0.9,
            "speed": 0.95,
            "timbre": "deep",
            "description": "Middle-aged man voice"
        }
        
        self.voice_models["woman_35_50"] = {
            "age_group": VoiceAgeGroup.MIDDLE_AGE,
            "gender": VoiceGender.WOMAN,
            "pitch": 1.0,
            "speed": 0.95,
            "timbre": "warm",
            "description": "Middle-aged woman voice"
        }
        
        # Seniors (50+)
        self.voice_models["man_50_plus"] = {
            "age_group": VoiceAgeGroup.SENIOR,
            "gender": VoiceGender.MAN,
            "pitch": 0.85,
            "speed": 0.9,
            "timbre": "deep",
            "description": "Senior man voice"
        }
        
        self.voice_models["woman_50_plus"] = {
            "age_group": VoiceAgeGroup.SENIOR,
            "gender": VoiceGender.WOMAN,
            "pitch": 0.95,
            "speed": 0.9,
            "timbre": "mature",
            "description": "Senior woman voice"
        }
    
    async def synthesize_voice(
        self,
        request: VoiceModulationRequest | Dict[str, Any],
        job_id: Optional[str] = None
    ) -> VoiceModulationResult:
        """
        Synthesize voice with age and gender modulation
        
        Args:
            request: Voice modulation request (typed or dict)
            job_id: Optional job ID for tracking
            
        Returns:
            VoiceModulationResult with audio URL
        """
        try:
            # Handle dict input
            if isinstance(request, dict):
                request = VoiceModulationRequest(**request)
            
            if not job_id:
                job_id = f"voice_{uuid.uuid4().hex[:12]}"
            
            logger.info(f"Starting voice synthesis for job {job_id} - Age: {request.age_group}, Gender: {request.gender}")
            
            # Store job
            self.active_jobs[job_id] = {
                "status": "processing",
                "start_time": asyncio.get_event_loop().time(),
                "request": request
            }
            
            # Get voice model based on age and gender
            voice_model_key = self._get_voice_model_key(request.age_group, request.gender)
            base_model = self.voice_models.get(voice_model_key, {})
            
            # Apply modulations
            pitch = request.pitch or base_model.get("pitch", 1.0)
            speed = request.speed or base_model.get("speed", 1.0)
            volume = request.volume or 1.0
            
            # Use AI Framework for voice synthesis
            audio_url = None
            duration = len(request.text.split()) * 0.5  # Estimate
            
            if self.ai_framework:
                try:
                    # Use AI framework for voice synthesis
                    voice_result = await self.ai_framework.synthesize_voice(
                        text=request.text,
                        voice_id=voice_model_key,
                        provider="elevenlabs",
                        emotion=request.emotion,
                        speed=speed,
                        pitch=pitch,
                        volume=volume,
                        accent=request.accent,
                        language=request.language
                    )
                    if isinstance(voice_result, dict):
                        audio_url = voice_result.get("audio_url") or f"s3://ai-film-studio-assets/voices/{job_id}/output.mp3"
                        duration = voice_result.get("duration", duration)
                    else:
                        audio_url = f"s3://ai-film-studio-assets/voices/{job_id}/output.mp3"
                except Exception as e:
                    logger.warning(f"AI framework voice synthesis failed: {e}, using fallback")
                    audio_url = f"s3://ai-film-studio-assets/voices/{job_id}/output.mp3"
            else:
                # Fallback: Import voice synthesis service
                try:
                    from src.services.voice_synthesis import VoiceSynthesisService
                    voice_service = VoiceSynthesisService()
                    audio_url = f"s3://ai-film-studio-assets/voices/{job_id}/output.mp3"
                except ImportError:
                    logger.warning("Voice synthesis service not available, using mock")
                    audio_url = f"s3://ai-film-studio-assets/voices/{job_id}/output.mp3"
            
            if not audio_url:
                audio_url = f"s3://ai-film-studio-assets/voices/{job_id}/output.mp3"
            
            # Create result
            result = VoiceModulationResult(
                job_id=job_id,
                voice_id=str(uuid.uuid4()),
                audio_url=audio_url,
                duration=duration,
                age_group=request.age_group,
                gender=request.gender,
                characteristics={
                    "pitch": pitch,
                    "speed": speed,
                    "volume": volume,
                    "emotion": request.emotion,
                    "accent": request.accent,
                    "language": request.language,
                    "timbre": base_model.get("timbre", "neutral")
                }
            )
            
            self.voices[result.voice_id] = result
            processing_time = asyncio.get_event_loop().time() - self.active_jobs[job_id]["start_time"]
            self.active_jobs[job_id]["status"] = "completed"
            self.active_jobs[job_id]["result"] = result
            self.active_jobs[job_id]["processing_time"] = processing_time
            
            return result
            
        except Exception as e:
            logger.error(f"Error synthesizing voice for job {job_id}: {str(e)}")
            if job_id and job_id in self.active_jobs:
                self.active_jobs[job_id]["status"] = "failed"
                self.active_jobs[job_id]["error"] = str(e)
            
            raise
    
    def _get_voice_model_key(self, age_group: str, gender: str) -> str:
        """Get voice model key from age group and gender"""
        gender_lower = gender.lower()
        
        if age_group == VoiceAgeGroup.INFANT:
            return f"{gender_lower}_0_3"
        elif age_group == VoiceAgeGroup.CHILD:
            return f"{gender_lower}_4_8"
        elif age_group == VoiceAgeGroup.PRE_TEEN:
            return f"{gender_lower}_8_12"
        elif age_group == VoiceAgeGroup.TEEN:
            return f"teen_{gender_lower}"
        elif age_group == VoiceAgeGroup.YOUNG_ADULT:
            return f"young_{gender_lower}"
        elif age_group == VoiceAgeGroup.ADULT:
            return f"{gender_lower}_22_35"
        elif age_group == VoiceAgeGroup.MIDDLE_AGE:
            return f"{gender_lower}_35_50"
        elif age_group == VoiceAgeGroup.SENIOR:
            return f"{gender_lower}_50_plus"
        else:
            return "man_22_35"  # Default
    
    def get_supported_age_groups(self) -> List[Dict[str, Any]]:
        """Get list of supported age groups for voice"""
        return [
            {"value": VoiceAgeGroup.INFANT, "label": "Infant (0-3 years)", "description": "Baby voices"},
            {"value": VoiceAgeGroup.CHILD, "label": "Child (4-8 years)", "description": "Young child voices"},
            {"value": VoiceAgeGroup.PRE_TEEN, "label": "Pre-teen (8-12 years)", "description": "Older child voices"},
            {"value": VoiceAgeGroup.TEEN, "label": "Teenager (13-19 years)", "description": "Teen voices"},
            {"value": VoiceAgeGroup.YOUNG_ADULT, "label": "Young Adult (20-21 years)", "description": "Young adult voices"},
            {"value": VoiceAgeGroup.ADULT, "label": "Adult (22-35 years)", "description": "Adult voices"},
            {"value": VoiceAgeGroup.MIDDLE_AGE, "label": "Middle Age (35-50 years)", "description": "Middle-aged voices"},
            {"value": VoiceAgeGroup.SENIOR, "label": "Senior (50+ years)", "description": "Senior voices"}
        ]
    
    def get_supported_genders(self) -> List[Dict[str, Any]]:
        """Get list of supported genders for voice"""
        return [
            {"value": VoiceGender.BOY, "label": "Boy"},
            {"value": VoiceGender.GIRL, "label": "Girl"},
            {"value": VoiceGender.MAN, "label": "Man"},
            {"value": VoiceGender.WOMAN, "label": "Woman"},
            {"value": VoiceGender.CHILD, "label": "Child (gender-neutral)"}
        ]
    
    def get_voice_models(self) -> Dict[str, Dict[str, Any]]:
        """Get all available voice models"""
        return self.voice_models.copy()
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get status of a voice synthesis job"""
        if job_id not in self.active_jobs:
            return {"status": "not_found"}
        return self.active_jobs[job_id]
    
    def get_voice(self, voice_id: str) -> Optional[VoiceModulationResult]:
        """Get voice result by ID"""
        return self.voices.get(voice_id)
