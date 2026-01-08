"""Leonardo.ai model client"""
from typing import Dict, Any, Optional
from services.model_clients.base_client import BaseModelClient
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class LeonardoClient(BaseModelClient):
    """Client for Leonardo.ai image generation"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            api_key=api_key,
            endpoint="https://cloud.leonardo.ai/api/rest/v1/generations"
        )
    
    async def generate_image(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        width: int = 1024,
        height: int = 576,
        num_images: int = 1,
        guidance_scale: float = 7.0,
        num_inference_steps: int = 30,
        model_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate image using Leonardo.ai"""
        logger.info("Generating image with Leonardo.ai")
        
        payload = {
            "prompt": prompt,
            "num_images": num_images,
            "width": width,
            "height": height,
            "guidance_scale": guidance_scale,
            "num_inference_steps": num_inference_steps,
        }
        
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt
        
        if model_id:
            payload["modelId"] = model_id
        
        # Support for LoRA
        if "lora" in kwargs:
            payload["lora"] = kwargs["lora"]
        
        # In production, this would make actual API call
        # For now, return mock response
        logger.info(f"Leonardo generation params: {payload}")
        
        return {
            "status": "success",
            "model": "leonardo",
            "prompt": prompt,
            "width": width,
            "height": height,
            "url": "placeholder_url.png"
        }
    
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """Validate Leonardo.ai parameters"""
        required = ["prompt"]
        return all(key in params for key in required)
