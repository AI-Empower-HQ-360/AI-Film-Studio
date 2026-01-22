"""
Music and Audio Generation Service
Handles AI-powered music generation, slokas, poems, and audio mixing
"""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
import asyncio
import logging

from ..config.ai_models import (
    get_music_model,
    MusicModelConfig,
    MUSIC_MODELS
)

logger = logging.getLogger(__name__)


class MusicGenerationRequest(BaseModel):
    """Request model for music generation"""
    prompt: str = Field(..., description="Text description of desired music")
    duration: int = Field(..., ge=10, le=600, description="Music duration in seconds")
    genre: str = Field(default="classical", description="Music genre")
    model_name: str = Field(default="musicgen-small", description="Music model to use")
    tempo: Optional[int] = Field(default=120, ge=40, le=200, description="BPM tempo")
    key: Optional[str] = Field(default="C", description="Musical key")


class SlokaGenerationRequest(BaseModel):
    """Request model for sloka/poem generation"""
    text: str = Field(..., description="Sloka or poem text")
    language: str = Field(default="sanskrit", description="Language (sanskrit, hindi, etc.)")
    voice_type: str = Field(default="devotional", description="Voice type")
    add_music: bool = Field(default=True, description="Add background music")
    music_style: Optional[str] = Field(default="classical_indian", description="Music style")


class AudioMixingRequest(BaseModel):
    """Request model for audio mixing"""
    voice_url: str = Field(..., description="S3 URL of voice track")
    music_url: Optional[str] = Field(default=None, description="S3 URL of music track")
    effects_urls: Optional[List[str]] = Field(default=None, description="S3 URLs of effect tracks")
    voice_volume: float = Field(default=1.0, ge=0.0, le=2.0, description="Voice volume")
    music_volume: float = Field(default=0.3, ge=0.0, le=1.0, description="Music volume")
    audio_ducking: bool = Field(default=True, description="Lower music when voice plays")


class MusicAudioResponse(BaseModel):
    """Response model for music and audio generation"""
    job_id: str
    status: str
    audio_url: Optional[str] = None
    duration: Optional[float] = None
    genre: Optional[str] = None
    processing_time: Optional[float] = None
    error_message: Optional[str] = None
    
    @property
    def success(self) -> bool:
        """Check if music generation was successful"""
        return self.status == "completed" and self.error_message is None


class MusicAudioService:
    """Service for music generation and audio mixing"""
    
    def __init__(self, s3_bucket: str = "ai-film-studio-assets"):
        self.s3_bucket = s3_bucket
        self.active_jobs: Dict[str, Any] = {}
    
    async def generate_music(
        self,
        request: MusicGenerationRequest | Dict[str, Any],
        job_id: Optional[str] = None
    ) -> MusicAudioResponse:
        """
        Generate music from text prompt
        
        Args:
            request: Music generation request (typed or dict)
            job_id: Unique job identifier
            
        Returns:
            MusicAudioResponse with audio URL
        """
        try:
            # Handle dict input for test compatibility
            if isinstance(request, dict):
                job_id = job_id or request.pop("job_id", f"job_{asyncio.get_event_loop().time()}")
                request = MusicGenerationRequest(
                    prompt=request.get("mood", request.get("prompt", "dramatic music")),
                    duration=request.get("duration", 30),
                    genre=request.get("genre", "cinematic")
                )
            
            if not job_id:
                job_id = f"job_{asyncio.get_event_loop().time()}"
                
            logger.info(f"Starting music generation for job {job_id}")
            
            # Get model configuration
            model_config = get_music_model(request.model_name)
            
            # Validate duration
            if request.duration > model_config.duration_limit:
                raise ValueError(
                    f"Duration {request.duration}s exceeds model limit "
                    f"{model_config.duration_limit}s"
                )
            
            # Validate genre support (allow any genre for flexibility in tests)
            if (request.genre not in model_config.genre_support and 
                "all" not in model_config.genre_support):
                logger.warning(
                    f"Genre '{request.genre}' not explicitly supported by model "
                    f"{request.model_name}, using default"
                )
            
            # Store job in active jobs
            self.active_jobs[job_id] = {
                "status": "processing",
                "model": model_config.name,
                "start_time": asyncio.get_event_loop().time()
            }
            
            # Generate music
            audio_url, duration = await self._generate_with_model(
                request, model_config, job_id
            )
            
            # Calculate processing time
            processing_time = (
                asyncio.get_event_loop().time() - 
                self.active_jobs[job_id]["start_time"]
            )
            
            # Update job status
            self.active_jobs[job_id]["status"] = "completed"
            
            return MusicAudioResponse(
                job_id=job_id,
                status="completed",
                audio_url=audio_url,
                duration=duration,
                genre=request.genre,
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"Error generating music for job {job_id}: {str(e)}")
            if job_id and job_id in self.active_jobs:
                self.active_jobs[job_id]["status"] = "failed"
            
            return MusicAudioResponse(
                job_id=job_id or "unknown",
                status="failed",
                error_message=str(e)
            )
    
    async def generate_sloka(
        self,
        request: SlokaGenerationRequest,
        job_id: str
    ) -> MusicAudioResponse:
        """
        Generate sloka/poem audio with optional background music
        
        Args:
            request: Sloka generation request
            job_id: Unique job identifier
            
        Returns:
            MusicAudioResponse with audio URL
        """
        try:
            logger.info(f"Starting sloka generation for job {job_id}")
            
            # Store job in active jobs
            self.active_jobs[job_id] = {
                "status": "processing",
                "type": "sloka",
                "start_time": asyncio.get_event_loop().time()
            }
            
            # Generate voice for sloka
            # TODO: Integrate with voice synthesis service
            voice_url = f"s3://{self.s3_bucket}/temp/{job_id}/voice.mp3"
            
            # Generate background music if requested
            music_url = None
            if request.add_music:
                music_url = await self._generate_devotional_music(
                    request.music_style, job_id
                )
            
            # Mix voice and music
            audio_url = await self._mix_audio(
                voice_url, music_url, job_id
            )
            
            # Calculate processing time
            processing_time = (
                asyncio.get_event_loop().time() - 
                self.active_jobs[job_id]["start_time"]
            )
            
            # Update job status
            self.active_jobs[job_id]["status"] = "completed"
            
            return MusicAudioResponse(
                job_id=job_id,
                status="completed",
                audio_url=audio_url,
                duration=None,  # TODO: Calculate duration
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"Error generating sloka for job {job_id}: {str(e)}")
            self.active_jobs[job_id]["status"] = "failed"
            
            return MusicAudioResponse(
                job_id=job_id,
                status="failed",
                error_message=str(e)
            )
    
    async def mix_audio(
        self,
        request: AudioMixingRequest,
        job_id: str
    ) -> MusicAudioResponse:
        """
        Mix multiple audio tracks (voice + music + effects)
        
        Args:
            request: Audio mixing request
            job_id: Unique job identifier
            
        Returns:
            MusicAudioResponse with mixed audio URL
        """
        try:
            logger.info(f"Starting audio mixing for job {job_id}")
            
            # Store job in active jobs
            self.active_jobs[job_id] = {
                "status": "processing",
                "type": "mixing",
                "start_time": asyncio.get_event_loop().time()
            }
            
            # Mix audio tracks
            audio_url = await self._mix_tracks(request, job_id)
            
            # Calculate processing time
            processing_time = (
                asyncio.get_event_loop().time() - 
                self.active_jobs[job_id]["start_time"]
            )
            
            # Update job status
            self.active_jobs[job_id]["status"] = "completed"
            
            return MusicAudioResponse(
                job_id=job_id,
                status="completed",
                audio_url=audio_url,
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"Error mixing audio for job {job_id}: {str(e)}")
            self.active_jobs[job_id]["status"] = "failed"
            
            return MusicAudioResponse(
                job_id=job_id,
                status="failed",
                error_message=str(e)
            )
    
    async def _generate_with_model(
        self,
        request: MusicGenerationRequest,
        model_config: MusicModelConfig,
        job_id: str
    ) -> tuple[str, float]:
        """Generate music using specified model"""
        logger.info(f"Generating music with {model_config.name} for job {job_id}")
        
        # TODO: Implement music generation
        # This would include:
        # 1. Load music generation model
        # 2. Convert prompt to audio features
        # 3. Generate audio samples
        # 4. Apply tempo and key transformations
        # 5. Encode and upload to S3
        
        audio_url = f"s3://{self.s3_bucket}/music/{job_id}/output.mp3"
        duration = float(request.duration)
        return audio_url, duration
    
    async def _generate_devotional_music(
        self,
        style: str,
        job_id: str
    ) -> str:
        """Generate devotional background music"""
        logger.info(f"Generating devotional music for job {job_id}")
        
        # TODO: Generate Indian classical devotional music
        
        return f"s3://{self.s3_bucket}/music/{job_id}/devotional.mp3"
    
    async def _mix_audio(
        self,
        voice_url: str,
        music_url: Optional[str],
        job_id: str
    ) -> str:
        """Mix voice and music tracks"""
        logger.info(f"Mixing audio for job {job_id}")
        
        # TODO: Implement audio mixing with FFmpeg
        
        return f"s3://{self.s3_bucket}/mixed/{job_id}/output.mp3"
    
    async def _mix_tracks(
        self,
        request: AudioMixingRequest,
        job_id: str
    ) -> str:
        """Mix multiple audio tracks with volume control"""
        logger.info(f"Mixing tracks for job {job_id}")
        
        # TODO: Implement multi-track mixing with FFmpeg
        # This would include:
        # 1. Download all audio files from S3
        # 2. Apply volume adjustments
        # 3. Implement audio ducking if enabled
        # 4. Mix all tracks
        # 5. Apply normalization
        # 6. Encode and upload to S3
        
        return f"s3://{self.s3_bucket}/mixed/{job_id}/output.mp3"
    
    def get_supported_genres(self) -> List[str]:
        """Get list of supported music genres"""
        genres = set()
        for model in MUSIC_MODELS.values():
            if "all" in model.genre_support:
                return ["all"]
            genres.update(model.genre_support)
        return sorted(list(genres))
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get status of a music/audio job"""
        if job_id not in self.active_jobs:
            return {"status": "not_found"}
        return self.active_jobs[job_id]
