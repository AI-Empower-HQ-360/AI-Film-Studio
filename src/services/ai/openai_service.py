"""
OpenAI Service
Interface for OpenAI API interactions (GPT-4, DALL-E, embeddings)
"""
import os
from typing import List, Dict, Any, Optional, AsyncIterator

try:
    from openai import OpenAI
    from openai import AsyncOpenAI
except ImportError:
    # For testing without openai package
    OpenAI = None
    AsyncOpenAI = None


class OpenAIService:
    """Service for interacting with OpenAI API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenAI service
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        if not self.api_key and OpenAI is not None:
            raise ValueError("OpenAI API key is required")
        
        if OpenAI is not None:
            self.client = OpenAI(api_key=self.api_key) if self.api_key else None
            self.async_client = AsyncOpenAI(api_key=self.api_key) if self.api_key else None
        else:
            self.client = None
            self.async_client = None
    
    async def complete(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Complete chat conversation
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model to use (default: gpt-4o)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters
            
        Returns:
            Generated text content
        """
        response = await self.async_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        if not response.choices or not response.choices[0].message:
            raise ValueError("No response from OpenAI")
        
        return response.choices[0].message.content or ""
    
    async def stream_complete(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o",
        temperature: float = 0.7,
        **kwargs
    ) -> AsyncIterator[str]:
        """
        Stream chat completion
        
        Args:
            messages: List of message dicts
            model: Model to use
            temperature: Sampling temperature
            **kwargs: Additional parameters
            
        Yields:
            Text chunks as they're generated
        """
        if not self.async_client:
            raise ValueError("OpenAI client not initialized")
        
        stream = await self.async_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=True,
            **kwargs
        )
        
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    async def generate_image(
        self,
        prompt: str,
        model: str = "dall-e-3",
        size: str = "1024x1024",
        quality: str = "standard",
        n: int = 1,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate image using DALL-E
        
        Args:
            prompt: Image description
            model: Model to use (dall-e-2 or dall-e-3)
            size: Image size
            quality: Image quality (standard or hd)
            n: Number of images
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with image URL
        """
        if not self.async_client:
            raise ValueError("OpenAI client not initialized")
        
        response = await self.async_client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality=quality,
            n=n,
            **kwargs
        )
        
        if not response.data:
            raise ValueError("No image generated")
        
        img = response.data[0]
        return {
            "url": img.url,
            "revised_prompt": getattr(img, "revised_prompt", None)
        }
    
    async def create_embedding(
        self,
        text: str,
        model: str = "text-embedding-3-small",
        **kwargs
    ) -> List[float]:
        """
        Create text embedding
        
        Args:
            text: Text to embed
            model: Embedding model
            **kwargs: Additional parameters
            
        Returns:
            Embedding vector
        """
        if not self.async_client:
            raise ValueError("OpenAI client not initialized")
        
        response = await self.async_client.embeddings.create(
            model=model,
            input=text,
            **kwargs
        )
        
        if not response.data:
            raise ValueError("No embedding returned")
        
        return response.data[0].embedding
    
    async def create_embeddings_batch(
        self,
        texts: List[str],
        model: str = "text-embedding-3-small",
        **kwargs
    ) -> List[List[float]]:
        """
        Create embeddings for multiple texts
        
        Args:
            texts: List of texts to embed
            model: Embedding model
            **kwargs: Additional parameters
            
        Returns:
            List of embedding vectors
        """
        if not self.async_client:
            raise ValueError("OpenAI client not initialized")
        
        response = await self.async_client.embeddings.create(
            model=model,
            input=texts,
            **kwargs
        )
        
        return [item.embedding for item in response.data]
    
    async def create_image_variation(
        self,
        image_path: str,
        n: int = 1,
        size: str = "1024x1024",
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Create image variation
        
        Args:
            image_path: Path to source image
            n: Number of variations
            size: Image size
            **kwargs: Additional parameters
            
        Returns:
            List of variation dictionaries with URLs
        """
        if not self.async_client:
            raise ValueError("OpenAI client not initialized")
        
        with open(image_path, "rb") as f:
            response = await self.async_client.images.create_variation(
                image=f,
                n=n,
                size=size,
                **kwargs
            )
        
        if not response.data:
            raise ValueError("No variation generated")
        
        return [
            {"url": img.url}
            for img in response.data
        ]
