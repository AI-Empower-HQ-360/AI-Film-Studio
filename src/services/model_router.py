"""Model router for AI image generation"""
from typing import Dict, Any, Optional, List
from enum import Enum


class ModelProvider(str, Enum):
    """Available model providers"""
    SDXL = "sdxl"
    STABLE_DIFFUSION = "stable-diffusion"
    DALLE = "dall-e"
    LEONARDO = "leonardo"
    MIDJOURNEY = "midjourney"
    CUSTOM_LORA = "custom-lora"
    REPLICATE = "replicate"
    RUNDIFFUSION = "rundiffusion"


class ModelRouter:
    """Routes prompts to appropriate image generation models"""
    
    def __init__(self):
        self.provider_capabilities = {
            ModelProvider.SDXL: {
                "styles": ["cinematic", "realistic", "painterly"],
                "max_resolution": (1024, 1024),
                "supports_lora": True,
                "supports_controlnet": True,
                "cost_per_image": 0.01,
            },
            ModelProvider.DALLE: {
                "styles": ["realistic", "artistic", "painterly"],
                "max_resolution": (1024, 1024),
                "supports_lora": False,
                "supports_controlnet": False,
                "cost_per_image": 0.02,
            },
            ModelProvider.LEONARDO: {
                "styles": ["cinematic", "anime", "realistic", "painterly"],
                "max_resolution": (1536, 1536),
                "supports_lora": True,
                "supports_controlnet": True,
                "cost_per_image": 0.015,
            },
            ModelProvider.STABLE_DIFFUSION: {
                "styles": ["cinematic", "anime", "realistic", "noir"],
                "max_resolution": (768, 768),
                "supports_lora": True,
                "supports_controlnet": True,
                "cost_per_image": 0.005,
            },
        }
        
        # Default provider preferences by style
        self.style_preferences = {
            "cinematic": [ModelProvider.SDXL, ModelProvider.LEONARDO],
            "anime": [ModelProvider.LEONARDO, ModelProvider.STABLE_DIFFUSION],
            "realistic": [ModelProvider.DALLE, ModelProvider.SDXL],
            "noir": [ModelProvider.STABLE_DIFFUSION, ModelProvider.SDXL],
            "painterly": [ModelProvider.LEONARDO, ModelProvider.DALLE],
        }
        
        # Fallback chain
        self.fallback_chain = [
            ModelProvider.SDXL,
            ModelProvider.STABLE_DIFFUSION,
            ModelProvider.LEONARDO,
            ModelProvider.DALLE,
        ]
    
    def select_model(
        self,
        style: str,
        resolution: tuple = (1024, 576),
        requires_lora: bool = False,
        requires_controlnet: bool = False,
        preferred_provider: Optional[ModelProvider] = None
    ) -> Dict[str, Any]:
        """Select the best model for the given requirements"""
        
        # If preferred provider specified and capable, use it
        if preferred_provider and self._is_provider_capable(
            preferred_provider, style, resolution, requires_lora, requires_controlnet
        ):
            return self._build_model_config(preferred_provider)
        
        # Try style preferences
        if style in self.style_preferences:
            for provider in self.style_preferences[style]:
                if self._is_provider_capable(
                    provider, style, resolution, requires_lora, requires_controlnet
                ):
                    return self._build_model_config(provider)
        
        # Try fallback chain
        for provider in self.fallback_chain:
            if self._is_provider_capable(
                provider, style, resolution, requires_lora, requires_controlnet
            ):
                return self._build_model_config(provider)
        
        # Default to SDXL if nothing else works
        return self._build_model_config(ModelProvider.SDXL)
    
    def _is_provider_capable(
        self,
        provider: ModelProvider,
        style: str,
        resolution: tuple,
        requires_lora: bool,
        requires_controlnet: bool
    ) -> bool:
        """Check if provider can handle the requirements"""
        if provider not in self.provider_capabilities:
            return False
        
        caps = self.provider_capabilities[provider]
        
        # Check style support
        if style not in caps["styles"]:
            return False
        
        # Check resolution
        max_width, max_height = caps["max_resolution"]
        if resolution[0] > max_width or resolution[1] > max_height:
            return False
        
        # Check LoRA support
        if requires_lora and not caps["supports_lora"]:
            return False
        
        # Check ControlNet support
        if requires_controlnet and not caps["supports_controlnet"]:
            return False
        
        return True
    
    def _build_model_config(self, provider: ModelProvider) -> Dict[str, Any]:
        """Build configuration for the selected model"""
        caps = self.provider_capabilities.get(provider, {})
        
        return {
            "provider": provider.value,
            "capabilities": caps,
            "endpoint": self._get_endpoint(provider),
            "default_params": self._get_default_params(provider),
        }
    
    def _get_endpoint(self, provider: ModelProvider) -> str:
        """Get API endpoint for provider"""
        endpoints = {
            ModelProvider.SDXL: "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
            ModelProvider.DALLE: "https://api.openai.com/v1/images/generations",
            ModelProvider.LEONARDO: "https://cloud.leonardo.ai/api/rest/v1/generations",
            ModelProvider.STABLE_DIFFUSION: "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image",
            ModelProvider.REPLICATE: "https://api.replicate.com/v1/predictions",
            ModelProvider.RUNDIFFUSION: "https://api.rundiffusion.com/v1/generate",
        }
        return endpoints.get(provider, "")
    
    def _get_default_params(self, provider: ModelProvider) -> Dict[str, Any]:
        """Get default parameters for provider"""
        defaults = {
            ModelProvider.SDXL: {
                "steps": 50,
                "cfg_scale": 7.5,
                "sampler": "DPMSolverMultistep",
            },
            ModelProvider.DALLE: {
                "n": 1,
                "size": "1024x1024",
                "quality": "standard",
            },
            ModelProvider.LEONARDO: {
                "num_images": 1,
                "guidance_scale": 7.0,
                "num_inference_steps": 30,
            },
            ModelProvider.STABLE_DIFFUSION: {
                "steps": 30,
                "cfg_scale": 7.0,
                "sampler": "K_DPMPP_2M",
            },
        }
        return defaults.get(provider, {})
    
    def get_fallback_provider(self, failed_provider: ModelProvider) -> Optional[ModelProvider]:
        """Get fallback provider if one fails"""
        try:
            idx = self.fallback_chain.index(failed_provider)
            if idx + 1 < len(self.fallback_chain):
                return self.fallback_chain[idx + 1]
        except ValueError:
            pass
        return None
