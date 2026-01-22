"""
Stability AI Service
Interface for Stability AI API (image and video generation)
"""
import os
import base64
from typing import Dict, Any, Optional

try:
    from stability_sdk import client
    from stability_sdk import generation
except ImportError:
    # For testing without stability_sdk package
    client = None
    generation = None


class StabilityService:
    """Service for interacting with Stability AI API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Stability AI service
        
        Args:
            api_key: Stability AI API key (defaults to STABILITY_AI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("STABILITY_AI_API_KEY", "")
        if not self.api_key:
            raise ValueError("Stability AI API key is required")
        
        # Initialize client (will be mocked in tests)
        self.client = None
    
    async def generate_image(
        self,
        prompt: str,
        style: str = "cinematic",
        width: int = 1024,
        height: int = 1024,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate image from text prompt
        
        Args:
            prompt: Image description
            style: Style preset
            width: Image width
            height: Image height
            **kwargs: Additional parameters
            
        Returns:
            Generated image data
        """
        if not self.client:
            # Initialize client if not already done
            self.client = client.StabilityInference(
                key=self.api_key,
                verbose=True
            )
        
        answers = self.client.generate(
            prompt=prompt,
            width=width,
            height=height,
            **kwargs
        )
        
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FINISH_REASON_SUCCESS:
                    return {
                        "base64": artifact.binary,
                        "seed": artifact.seed,
                        "mime_type": artifact.mime
                    }
        
        raise ValueError("Image generation failed")
    
    async def image_to_image(
        self,
        init_image: str,
        prompt: str,
        strength: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Transform image using text prompt
        
        Args:
            init_image: Path to initial image
            prompt: Transformation description
            strength: Transformation strength (0-1)
            **kwargs: Additional parameters
            
        Returns:
            Transformed image data
        """
        if not self.client:
            self.client = client.StabilityInference(
                key=self.api_key,
                verbose=True
            )
        
        # Read init image
        with open(init_image, "rb") as f:
            init_image_data = f.read()
        
        answers = self.client.generate(
            prompt=prompt,
            init_image=init_image_data,
            strength=strength,
            **kwargs
        )
        
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FINISH_REASON_SUCCESS:
                    return {
                        "base64": artifact.binary,
                        "seed": artifact.seed
                    }
        
        raise ValueError("Image-to-image transformation failed")
    
    async def generate_video(
        self,
        init_image: str,
        motion_bucket_id: int = 127,
        cfg_scale: float = 2.5,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate video from image
        
        Args:
            init_image: Path to initial image
            motion_bucket_id: Motion intensity (1-255)
            cfg_scale: Guidance scale
            **kwargs: Additional parameters
            
        Returns:
            Generation job details
        """
        if not self.client:
            self.client = client.StabilityInference(
                key=self.api_key,
                verbose=True
            )
        
        # Read init image
        with open(init_image, "rb") as f:
            init_image_data = f.read()
        
        # Generate video (this is a placeholder - actual API may differ)
        result = {
            "id": f"gen_{hash(init_image_data) % 10000}",
            "status": "processing"
        }
        
        return result
    
    async def get_video_status(self, generation_id: str) -> Dict[str, Any]:
        """
        Get video generation status
        
        Args:
            generation_id: Generation job ID
            
        Returns:
            Status information
        """
        # Placeholder implementation
        return {
            "status": "completed",
            "video_url": f"https://stability.ai/video/{generation_id}.mp4"
        }
