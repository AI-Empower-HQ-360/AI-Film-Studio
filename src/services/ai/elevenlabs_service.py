"""
ElevenLabs Service
Interface for ElevenLabs voice synthesis API
"""
import os
from typing import List, Dict, Any, Optional, AsyncIterator

try:
    from elevenlabs import ElevenLabs, VoiceSettings
except ImportError:
    # For testing without elevenlabs package
    ElevenLabs = None
    VoiceSettings = None


class ElevenLabsService:
    """Service for interacting with ElevenLabs API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize ElevenLabs service
        
        Args:
            api_key: ElevenLabs API key (defaults to ELEVENLABS_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY", "")
        if not self.api_key and ElevenLabs is not None:
            raise ValueError("ElevenLabs API key is required")
        
        if ElevenLabs is not None:
            self.client = ElevenLabs(api_key=self.api_key) if self.api_key else None
        else:
            self.client = None
    
    async def synthesize(
        self,
        text: str,
        voice_id: str,
        settings: Optional[Dict[str, Any]] = None,
        model_id: str = "eleven_multilingual_v2",
        **kwargs
    ) -> bytes:
        """
        Synthesize speech from text
        
        Args:
            text: Text to synthesize
            voice_id: Voice ID to use
            settings: Voice settings (stability, similarity_boost, etc.)
            model_id: Model to use
            **kwargs: Additional parameters
            
        Returns:
            Audio data as bytes
        """
        if not self.client:
            raise ValueError("ElevenLabs client not initialized")
        
        voice_settings = None
        if settings and VoiceSettings is not None:
            voice_settings = VoiceSettings(
                stability=settings.get("stability", 0.5),
                similarity_boost=settings.get("similarity_boost", 0.75),
                style=settings.get("style", 0.0),
                use_speaker_boost=settings.get("use_speaker_boost", True)
            )
        
        audio_generator = self.client.generate(
            text=text,
            voice=voice_id,
            model=model_id,
            voice_settings=voice_settings,
            **kwargs
        )
        
        # Collect all audio chunks
        audio_data = b""
        for chunk in audio_generator:
            audio_data += chunk
        
        return audio_data
    
    async def synthesize_stream(
        self,
        text: str,
        voice_id: str,
        model_id: str = "eleven_multilingual_v2",
        **kwargs
    ) -> AsyncIterator[bytes]:
        """
        Stream audio synthesis
        
        Args:
            text: Text to synthesize
            voice_id: Voice ID to use
            model_id: Model to use
            **kwargs: Additional parameters
            
        Yields:
            Audio chunks as bytes
        """
        if not self.client:
            raise ValueError("ElevenLabs client not initialized")
        
        audio_generator = self.client.generate(
            text=text,
            voice=voice_id,
            model=model_id,
            stream=True,
            **kwargs
        )
        
        for chunk in audio_generator:
            yield chunk
    
    async def list_voices(self) -> List[Dict[str, Any]]:
        """
        List all available voices
        
        Returns:
            List of voice dictionaries
        """
        if not self.client:
            raise ValueError("ElevenLabs client not initialized")
        
        voices = self.client.voices.get_all()
        
        # Handle both direct list and object with voices attribute
        if hasattr(voices, "voices"):
            voice_list = voices.voices
        elif isinstance(voices, list):
            voice_list = voices
        else:
            voice_list = [voices]
        
        return [
            {
                "voice_id": getattr(voice, "voice_id", str(voice)),
                "name": getattr(voice, "name", "Unknown"),
                "labels": getattr(voice, "labels", {}) or {},
                "description": getattr(voice, "description", None)
            }
            for voice in voice_list
        ]
    
    async def get_voice(self, voice_id: str) -> Dict[str, Any]:
        """
        Get voice details
        
        Args:
            voice_id: Voice ID
            
        Returns:
            Voice details dictionary
        """
        if not self.client:
            raise ValueError("ElevenLabs client not initialized")
        
        voice = self.client.voices.get(voice_id=voice_id)
        
        return {
            "voice_id": getattr(voice, "voice_id", voice_id),
            "name": getattr(voice, "name", "Unknown"),
            "labels": getattr(voice, "labels", {}) or {},
            "description": getattr(voice, "description", None)
        }
    
    async def clone_voice(
        self,
        name: str,
        samples: List[str],
        description: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Clone a voice from audio samples
        
        Args:
            name: Name for the cloned voice
            samples: List of audio file paths
            description: Voice description
            **kwargs: Additional parameters
            
        Returns:
            Cloned voice details
        """
        if not self.client:
            raise ValueError("ElevenLabs client not initialized")
        
        voice = self.client.clone(
            name=name,
            files=samples,
            description=description,
            **kwargs
        )
        
        return {
            "voice_id": getattr(voice, "voice_id", "cloned_voice"),
            "name": getattr(voice, "name", name)
        }
    
    async def instant_clone(
        self,
        name: str,
        sample: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Instant voice clone from single sample
        
        Args:
            name: Name for the cloned voice
            sample: Path to audio sample file
            **kwargs: Additional parameters
            
        Returns:
            Cloned voice details
        """
        if not self.client:
            raise ValueError("ElevenLabs client not initialized")
        
        # Use instant_clone if available, otherwise use regular clone
        if hasattr(self.client, "instant_clone"):
            voice = self.client.instant_clone(
                name=name,
                sample=sample,
                **kwargs
            )
        else:
            voice = self.client.clone(
                name=name,
                files=[sample],
                **kwargs
            )
        
        return {
            "voice_id": getattr(voice, "voice_id", "instant_cloned_voice"),
            "name": getattr(voice, "name", name)
        }
    
    async def isolate_voice(
        self,
        audio_path: str,
        **kwargs
    ) -> bytes:
        """
        Isolate voice from audio (remove background noise)
        
        Args:
            audio_path: Path to audio file
            **kwargs: Additional parameters
            
        Returns:
            Isolated audio data
        """
        if not self.client:
            raise ValueError("ElevenLabs client not initialized")
        
        # Read audio file
        with open(audio_path, "rb") as f:
            audio_data = f.read()
        
        # Use audio_isolation if available
        if hasattr(self.client, "audio_isolation"):
            return self.client.audio_isolation(audio_data, **kwargs)
        else:
            # Return original if method not available
            return audio_data
    
    async def delete_voice(self, voice_id: str) -> bool:
        """
        Delete a cloned voice
        
        Args:
            voice_id: Voice ID to delete
            
        Returns:
            True if successful
        """
        self.client.voices.delete(voice_id=voice_id)
        return True
