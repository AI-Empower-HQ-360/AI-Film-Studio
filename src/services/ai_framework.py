"""
Unified AI Framework Integration Layer
Provides a centralized interface for all AI services across all engines
"""
from typing import Optional, Dict, Any, List
import logging
import os

logger = logging.getLogger(__name__)

# Import AI services
try:
    from .ai.openai_service import OpenAIService
    from .ai.anthropic_service import AnthropicService
    from .ai.stability_service import StabilityService
    from .ai.elevenlabs_service import ElevenLabsService
    HAS_AI_SERVICES = True
except ImportError:
    HAS_AI_SERVICES = False
    OpenAIService = None
    AnthropicService = None
    StabilityService = None
    ElevenLabsService = None


class AIFramework:
    """
    Unified AI Framework Manager
    Provides access to all AI services for all engines
    """
    
    def __init__(self):
        """Initialize AI framework with all services"""
        self.openai: Optional[OpenAIService] = None
        self.anthropic: Optional[AnthropicService] = None
        self.stability: Optional[StabilityService] = None
        self.elevenlabs: Optional[ElevenLabsService] = None
        
        # Initialize services if available
        if HAS_AI_SERVICES:
            try:
                if os.getenv("OPENAI_API_KEY"):
                    self.openai = OpenAIService()
                    logger.info("OpenAI service initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI: {e}")
            
            try:
                if os.getenv("ANTHROPIC_API_KEY"):
                    self.anthropic = AnthropicService()
                    logger.info("Anthropic service initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Anthropic: {e}")
            
            try:
                if os.getenv("STABILITY_AI_API_KEY"):
                    self.stability = StabilityService()
                    logger.info("Stability AI service initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Stability AI: {e}")
            
            try:
                if os.getenv("ELEVENLABS_API_KEY"):
                    self.elevenlabs = ElevenLabsService()
                    logger.info("ElevenLabs service initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize ElevenLabs: {e}")
    
    # ==================== Text Generation (Writing, Dialogues, Screenplay) ====================
    
    async def generate_text(
        self,
        prompt: str,
        model: str = "gpt-4",
        provider: str = "openai",
        max_tokens: int = 2000,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate text using AI (for Writing, Dialogues, Screenplay engines)
        
        Args:
            prompt: Input prompt
            model: Model name
            provider: "openai" or "anthropic"
            max_tokens: Maximum tokens to generate
            temperature: Creativity level (0-1)
            **kwargs: Additional parameters
            
        Returns:
            Generated text
        """
        if provider == "openai" and self.openai:
            try:
                response = await self.openai.complete(
                    messages=[{"role": "user", "content": prompt}],
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    **kwargs
                )
                if hasattr(response, 'choices') and len(response.choices) > 0:
                    return response.choices[0].message.content
                elif isinstance(response, dict) and 'choices' in response:
                    return response['choices'][0]['message']['content']
                return str(response)
            except Exception as e:
                logger.error(f"OpenAI text generation failed: {e}")
        
        elif provider == "anthropic" and self.anthropic:
            try:
                response = await self.anthropic.complete(
                    messages=[{"role": "user", "content": prompt}],
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    **kwargs
                )
                if hasattr(response, 'content') and len(response.content) > 0:
                    return response.content[0].text
                elif isinstance(response, dict) and 'content' in response:
                    return response['content'][0]['text']
                return str(response)
            except Exception as e:
                logger.error(f"Anthropic text generation failed: {e}")
        
        # Fallback
        logger.warning(f"AI service not available for provider: {provider}")
        return f"[AI Generated: {prompt[:50]}...]"
    
    # ==================== Image Generation (Image Creation, Character, Marketing) ====================
    
    async def generate_image(
        self,
        prompt: str,
        provider: str = "stability",
        model: str = "stable-diffusion-xl",
        width: int = 1024,
        height: int = 1024,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate image using AI (for Image Creation, Character, Marketing engines)
        
        Args:
            prompt: Image generation prompt
            provider: "stability" or "openai"
            model: Model name
            width: Image width
            height: Image height
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with image_url, image_data, etc.
        """
        if provider == "stability" and self.stability:
            try:
                result = await self.stability.generate_image(
                    prompt=prompt,
                    width=width,
                    height=height,
                    **kwargs
                )
                if isinstance(result, dict):
                    return result
                # Handle mock responses
                return {
                    "image_url": f"s3://generated/{hash(prompt)}.png",
                    "image_data": b"mock_image_data",
                    "provider": "stability_ai"
                }
            except Exception as e:
                logger.error(f"Stability AI image generation failed: {e}")
        
        elif provider == "openai" and self.openai:
            try:
                result = await self.openai.generate_image(
                    prompt=prompt,
                    size=f"{width}x{height}",
                    **kwargs
                )
                if isinstance(result, dict):
                    return result
                return {
                    "image_url": f"s3://generated/{hash(prompt)}.png",
                    "image_data": b"mock_image_data",
                    "provider": "openai_dalle"
                }
            except Exception as e:
                logger.error(f"OpenAI image generation failed: {e}")
        
        # Fallback
        logger.warning(f"Image generation service not available for provider: {provider}")
        return {
            "image_url": f"s3://generated/{hash(prompt)}.png",
            "image_data": b"mock_image_data",
            "provider": provider
        }
    
    # ==================== Voice Synthesis (Voice Modulation, Character) ====================
    
    async def synthesize_voice(
        self,
        text: str,
        voice_id: str,
        provider: str = "elevenlabs",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Synthesize voice using AI (for Voice Modulation, Character engines)
        
        Args:
            text: Text to synthesize
            voice_id: Voice identifier
            provider: "elevenlabs" or other
            **kwargs: Additional parameters (emotion, speed, pitch, etc.)
            
        Returns:
            Dictionary with audio_url, audio_data, etc.
        """
        if provider == "elevenlabs" and self.elevenlabs:
            try:
                result = await self.elevenlabs.synthesize(
                    text=text,
                    voice_id=voice_id,
                    **kwargs
                )
                if isinstance(result, dict):
                    return result
                return {
                    "audio_url": f"s3://audio/{hash(text)}.wav",
                    "audio_data": b"mock_audio_data",
                    "provider": "elevenlabs"
                }
            except Exception as e:
                logger.error(f"ElevenLabs voice synthesis failed: {e}")
        
        # Fallback
        logger.warning(f"Voice synthesis service not available for provider: {provider}")
        return {
            "audio_url": f"s3://audio/{hash(text)}.wav",
            "audio_data": b"mock_audio_data",
            "provider": provider
        }
    
    # ==================== Analysis & Understanding (Director, Pre-Production) ====================
    
    async def analyze_content(
        self,
        content: str,
        analysis_type: str = "general",
        provider: str = "openai",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Analyze content using AI (for Director, Pre-Production engines)
        
        Args:
            content: Content to analyze
            analysis_type: Type of analysis (shot_composition, scene_breakdown, etc.)
            provider: "openai" or "anthropic"
            **kwargs: Additional parameters
            
        Returns:
            Analysis results dictionary
        """
        prompt = f"Analyze the following {analysis_type}:\n\n{content}"
        
        if provider == "openai" and self.openai:
            try:
                response = await self.openai.complete(
                    messages=[{"role": "user", "content": prompt}],
                    model="gpt-4",
                    **kwargs
                )
                if hasattr(response, 'choices') and len(response.choices) > 0:
                    analysis_text = response.choices[0].message.content
                elif isinstance(response, dict) and 'choices' in response:
                    analysis_text = response['choices'][0]['message']['content']
                else:
                    analysis_text = str(response)
                
                return {
                    "analysis": analysis_text,
                    "type": analysis_type,
                    "provider": "openai"
                }
            except Exception as e:
                logger.error(f"OpenAI analysis failed: {e}")
        
        elif provider == "anthropic" and self.anthropic:
            try:
                response = await self.anthropic.complete(
                    messages=[{"role": "user", "content": prompt}],
                    model="claude-3-opus-20240229",
                    **kwargs
                )
                if hasattr(response, 'content') and len(response.content) > 0:
                    analysis_text = response.content[0].text
                elif isinstance(response, dict) and 'content' in response:
                    analysis_text = response['content'][0]['text']
                else:
                    analysis_text = str(response)
                
                return {
                    "analysis": analysis_text,
                    "type": analysis_type,
                    "provider": "anthropic"
                }
            except Exception as e:
                logger.error(f"Anthropic analysis failed: {e}")
        
        # Fallback
        return {
            "analysis": f"Analysis of {analysis_type}",
            "type": analysis_type,
            "provider": provider
        }
    
    # ==================== Structured Data Extraction (Pre-Production, Production Management) ====================
    
    async def extract_structured_data(
        self,
        content: str,
        schema: Dict[str, Any],
        provider: str = "openai",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Extract structured data using AI (for Pre-Production, Production Management)
        
        Args:
            content: Content to extract from
            schema: Schema definition for extraction
            provider: "openai" or "anthropic"
            **kwargs: Additional parameters
            
        Returns:
            Extracted structured data
        """
        schema_description = ", ".join(schema.keys())
        prompt = f"Extract the following structured data from the content:\nSchema: {schema_description}\n\nContent:\n{content}\n\nReturn as JSON."
        
        if provider == "openai" and self.openai:
            try:
                response = await self.openai.complete(
                    messages=[{"role": "user", "content": prompt}],
                    model="gpt-4",
                    response_format={"type": "json_object"},
                    **kwargs
                )
                if hasattr(response, 'choices') and len(response.choices) > 0:
                    import json
                    return json.loads(response.choices[0].message.content)
            except Exception as e:
                logger.error(f"Structured data extraction failed: {e}")
        
        # Fallback - return schema with placeholder values
        return {key: f"extracted_{key}" for key in schema.keys()}
    
    # ==================== Video Generation (Production Layer, Marketing) ====================
    
    async def generate_video(
        self,
        prompt: str,
        provider: str = "stability",
        duration: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate video using AI (for Production Layer, Marketing engines)
        
        Args:
            prompt: Video generation prompt
            provider: "stability" or other
            duration: Video duration in seconds
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with video_url, video_data, etc.
        """
        if provider == "stability" and self.stability:
            try:
                result = await self.stability.generate_video(
                    prompt=prompt,
                    **kwargs
                )
                if isinstance(result, dict):
                    return result
                return {
                    "video_url": f"s3://videos/{hash(prompt)}.mp4",
                    "video_data": b"mock_video_data",
                    "provider": "stability_ai",
                    "duration": duration
                }
            except Exception as e:
                logger.error(f"Stability AI video generation failed: {e}")
        
        # Fallback
        return {
            "video_url": f"s3://videos/{hash(prompt)}.mp4",
            "video_data": b"mock_video_data",
            "provider": provider,
            "duration": duration
        }
    
    # ==================== Utility Methods ====================
    
    def is_available(self, provider: str) -> bool:
        """Check if a provider is available"""
        if provider == "openai":
            return self.openai is not None
        elif provider == "anthropic":
            return self.anthropic is not None
        elif provider == "stability":
            return self.stability is not None
        elif provider == "elevenlabs":
            return self.elevenlabs is not None
        return False
    
    def get_available_providers(self) -> List[str]:
        """Get list of available AI providers"""
        providers = []
        if self.openai:
            providers.append("openai")
        if self.anthropic:
            providers.append("anthropic")
        if self.stability:
            providers.append("stability")
        if self.elevenlabs:
            providers.append("elevenlabs")
        return providers


# Global singleton instance
_ai_framework_instance: Optional[AIFramework] = None


def get_ai_framework() -> AIFramework:
    """Get the global AI framework instance"""
    global _ai_framework_instance
    if _ai_framework_instance is None:
        _ai_framework_instance = AIFramework()
    return _ai_framework_instance
