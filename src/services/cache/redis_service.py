"""
Redis Cache Service
Handles ElastiCache Redis operations
"""
import os
import asyncio
import logging
import json
from typing import Optional, Dict, Any, List

try:
    import redis.asyncio as redis
    HAS_REDIS = True
except ImportError:
    HAS_REDIS = False
    redis = None

logger = logging.getLogger(__name__)


class CacheService:
    """Service for Redis cache operations"""
    
    def __init__(self, redis_url: Optional[str] = None):
        """
        Initialize cache service
        
        Args:
            redis_url: Redis connection URL
        """
        self.redis_url = redis_url or os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.client = None  # Will be set by tests or initialized on first use
    
    async def _get_client(self):
        """Get or create Redis client"""
        if self.client:
            return self.client
        
        if not HAS_REDIS:
            raise ValueError("redis not installed")
        
        self.client = await redis.from_url(self.redis_url)
        return self.client
    
    async def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        client = await self._get_client()
        
        try:
            value = await client.get(key)
            if value:
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value.decode("utf-8") if isinstance(value, bytes) else value
            return None
            
        except Exception as e:
            logger.error(f"Error getting from cache: {str(e)}")
            raise
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds
            
        Returns:
            True if successful
        """
        client = await self._get_client()
        
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            elif not isinstance(value, (str, bytes)):
                value = str(value)
            
            if ttl:
                await client.setex(key, ttl, value)
            else:
                await client.set(key, value)
            
            return True
            
        except Exception as e:
            logger.error(f"Error setting cache: {str(e)}")
            raise
    
    async def delete(self, key: str) -> bool:
        """
        Delete key from cache
        
        Args:
            key: Cache key
            
        Returns:
            True if successful
        """
        client = await self._get_client()
        
        try:
            result = await client.delete(key)
            return result > 0
            
        except Exception as e:
            logger.error(f"Error deleting from cache: {str(e)}")
            raise
    
    async def exists(self, key: str) -> bool:
        """
        Check if key exists
        
        Args:
            key: Cache key
            
        Returns:
            True if key exists
        """
        client = await self._get_client()
        
        try:
            result = await client.exists(key)
            return result > 0
            
        except Exception as e:
            logger.error(f"Error checking cache: {str(e)}")
            raise
    
    async def expire(self, key: str, ttl: int) -> bool:
        """
        Set expiration on key
        
        Args:
            key: Cache key
            ttl: Time to live in seconds
            
        Returns:
            True if successful
        """
        client = await self._get_client()
        
        try:
            result = await client.expire(key, ttl)
            return result
            
        except Exception as e:
            logger.error(f"Error setting expiration: {str(e)}")
            raise
    
    async def clear_pattern(self, pattern: str) -> int:
        """
        Clear all keys matching pattern
        
        Args:
            pattern: Key pattern (e.g., "user:*")
            
        Returns:
            Number of keys deleted
        """
        client = await self._get_client()
        
        try:
            keys = []
            async for key in client.scan_iter(match=pattern):
                keys.append(key)
            
            if keys:
                return await client.delete(*keys)
            return 0
            
        except Exception as e:
            logger.error(f"Error clearing pattern: {str(e)}")
            raise
