"""
Anthropic Service
Interface for Anthropic Claude API
"""
import os
from typing import List, Dict, Any, Optional, AsyncIterator

try:
    from anthropic import Anthropic, AsyncAnthropic
except ImportError:
    # For testing without anthropic package
    Anthropic = None
    AsyncAnthropic = None


class AnthropicService:
    """Service for interacting with Anthropic Claude API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Anthropic service
        
        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY", "")
        if not self.api_key and Anthropic is not None:
            raise ValueError("Anthropic API key is required")
        
        if Anthropic is not None:
            self.client = Anthropic(api_key=self.api_key) if self.api_key else None
            self.async_client = AsyncAnthropic(api_key=self.api_key) if self.api_key else None
        else:
            self.client = None
            self.async_client = None
    
    async def complete(
        self,
        messages: List[Dict[str, str]],
        model: str = "claude-3-sonnet-20240229",
        max_tokens: int = 1024,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Complete message conversation
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model to use
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            **kwargs: Additional parameters
            
        Returns:
            Generated text content
        """
        response = await self.async_client.messages.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs
        )
        
        if not response.content:
            raise ValueError("No response from Anthropic")
        
        # Extract text from content blocks
        text_parts = []
        for block in response.content:
            if block.type == "text":
                text_parts.append(block.text)
        
        return "".join(text_parts)
    
    async def stream_complete(
        self,
        messages: List[Dict[str, str]],
        model: str = "claude-3-sonnet-20240229",
        max_tokens: int = 1024,
        **kwargs
    ) -> AsyncIterator[str]:
        """
        Stream message completion
        
        Args:
            messages: List of message dicts
            model: Model to use
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters
            
        Yields:
            Text chunks as they're generated
        """
        async with self.async_client.messages.stream(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            **kwargs
        ) as stream:
            async for event in stream:
                if event.type == "content_block_delta":
                    if hasattr(event.delta, "text"):
                        yield event.delta.text
                elif event.type == "content_block_start":
                    if hasattr(event.content_block, "text"):
                        yield event.content_block.text
