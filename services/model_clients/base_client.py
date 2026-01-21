"""Base client for image generation models"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import aiohttp
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class BaseModelClient(ABC):
    """Base class for all model clients"""
    
    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None):
        self.api_key = api_key
        self.endpoint = endpoint
    
    @abstractmethod
    async def generate_image(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate an image from prompt"""
        pass
    
    @abstractmethod
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """Validate generation parameters"""
        pass
    
    async def _make_request(
        self,
        url: str,
        method: str = "POST",
        headers: Optional[Dict[str, str]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to API"""
        if headers is None:
            headers = {}
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method, url, headers=headers, json=json_data
            ) as response:
                response.raise_for_status()
                return await response.json()
