"""DALL-E model client"""
from typing import Dict, Any, Optional
from services.model_clients.base_client import BaseModelClient
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class DALLEClient(BaseModelClient):
    """Client for DALL-E image generation"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            api_key=api_key,
            endpoint="https://api.openai.com/v1/images/generations"
        )
    
    async def generate_image(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        size: str = "1024x1024",
        quality: str = "standard",
        n: int = 1,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate image using DALL-E"""
        logger.info("Generating image with DALL-E")
        
        payload = {
            "prompt": prompt,
            "n": n,
            "size": size,
            "quality": quality,
        }
        
        # Note: DALL-E doesn't support negative prompts directly
        # They need to be incorporated into the main prompt
        if negative_prompt:
            payload["prompt"] = f"{prompt}, avoiding: {negative_prompt}"
        
        # In production, this would make actual API call
        # For now, return mock response
        logger.info(f"DALL-E generation params: {payload}")
        
        return {
            "status": "success",
            "model": "dall-e",
            "prompt": prompt,
            "size": size,
            "url": "placeholder_url.png"
        }
    
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """Validate DALL-E parameters"""
        required = ["prompt"]
        valid_sizes = ["256x256", "512x512", "1024x1024", "1024x1792", "1792x1024"]
        
        if not all(key in params for key in required):
            return False
        
        if "size" in params and params["size"] not in valid_sizes:
            return False
        
        return True
