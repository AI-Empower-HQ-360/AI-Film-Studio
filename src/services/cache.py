"""
ElastiCache Service for AI Film Studio.
Handles caching for improved performance.
"""

import os
import json
import hashlib
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta


class CacheService:
    """AWS ElastiCache Service for caching."""
    
    def __init__(self, host: Optional[str] = None, port: int = 6379):
        """Initialize the cache service."""
        self.host = host or os.getenv("REDIS_HOST", "localhost")
        self.port = port or int(os.getenv("REDIS_PORT", "6379"))
        self.region = os.getenv("AWS_REGION", "us-east-1")
        self._client = None
        self._cache: Dict[str, Dict[str, Any]] = {}  # In-memory cache for testing
    
    @property
    def client(self):
        """Lazy load Redis client."""
        if self._client is None:
            try:
                import redis
                self._client = redis.Redis(
                    host=self.host,
                    port=self.port,
                    decode_responses=True
                )
            except ImportError:
                self._client = None
        return self._client
    
    async def get(self, key: str) -> Optional[Any]:
        """Get a value from cache."""
        if key in self._cache:
            entry = self._cache[key]
            if entry.get("expires_at"):
                if datetime.fromisoformat(entry["expires_at"]) < datetime.utcnow():
                    del self._cache[key]
                    return None
            return entry.get("value")
        
        if self.client:
            try:
                value = self.client.get(key)
                if value:
                    return json.loads(value)
            except Exception:
                pass
        
        return None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl_seconds: Optional[int] = None
    ) -> bool:
        """Set a value in cache."""
        expires_at = None
        if ttl_seconds:
            expires_at = (datetime.utcnow() + timedelta(seconds=ttl_seconds)).isoformat()
        
        self._cache[key] = {
            "value": value,
            "expires_at": expires_at,
            "created_at": datetime.utcnow().isoformat()
        }
        
        if self.client:
            try:
                serialized = json.dumps(value)
                if ttl_seconds:
                    self.client.setex(key, ttl_seconds, serialized)
                else:
                    self.client.set(key, serialized)
            except Exception:
                pass
        
        return True
    
    async def delete(self, key: str) -> bool:
        """Delete a key from cache."""
        if key in self._cache:
            del self._cache[key]
        
        if self.client:
            try:
                self.client.delete(key)
            except Exception:
                pass
        
        return True
    
    async def exists(self, key: str) -> bool:
        """Check if a key exists in cache."""
        if key in self._cache:
            entry = self._cache[key]
            if entry.get("expires_at"):
                if datetime.fromisoformat(entry["expires_at"]) < datetime.utcnow():
                    del self._cache[key]
                    return False
            return True
        
        if self.client:
            try:
                return bool(self.client.exists(key))
            except Exception:
                pass
        
        return False
    
    async def get_or_set(
        self,
        key: str,
        default_factory: callable,
        ttl_seconds: Optional[int] = None
    ) -> Any:
        """Get value from cache or set it using the factory."""
        value = await self.get(key)
        if value is not None:
            return value
        
        # Cache miss - generate value
        value = default_factory() if callable(default_factory) else default_factory
        await self.set(key, value, ttl_seconds)
        return value
    
    async def mget(self, keys: List[str]) -> Dict[str, Any]:
        """Get multiple values from cache."""
        results = {}
        for key in keys:
            value = await self.get(key)
            if value is not None:
                results[key] = value
        return results
    
    async def mset(
        self,
        items: Dict[str, Any],
        ttl_seconds: Optional[int] = None
    ) -> bool:
        """Set multiple values in cache."""
        for key, value in items.items():
            await self.set(key, value, ttl_seconds)
        return True
    
    async def incr(self, key: str, amount: int = 1) -> int:
        """Increment a counter in cache."""
        current = await self.get(key)
        new_value = (current or 0) + amount
        await self.set(key, new_value)
        return new_value
    
    async def decr(self, key: str, amount: int = 1) -> int:
        """Decrement a counter in cache."""
        return await self.incr(key, -amount)
    
    async def flush(self) -> bool:
        """Flush all cache entries."""
        self._cache.clear()
        
        if self.client:
            try:
                self.client.flushdb()
            except Exception:
                pass
        
        return True
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_keys = len(self._cache)
        expired = 0
        
        for entry in self._cache.values():
            if entry.get("expires_at"):
                if datetime.fromisoformat(entry["expires_at"]) < datetime.utcnow():
                    expired += 1
        
        return {
            "total_keys": total_keys,
            "active_keys": total_keys - expired,
            "expired_keys": expired,
            "memory_usage_bytes": sum(
                len(json.dumps(e.get("value", ""))) 
                for e in self._cache.values()
            )
        }
    
    def cache_key(self, *args, **kwargs) -> str:
        """Generate a cache key from arguments."""
        key_data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True)
        return hashlib.md5(key_data.encode()).hexdigest()
    
    async def health_check(self) -> Dict[str, Any]:
        """Check cache service health."""
        stats = await self.get_stats()
        return {
            "status": "healthy",
            "host": self.host,
            "port": self.port,
            "keys": stats["total_keys"],
            "connection": "active" if self.client else "local"
        }


# Convenience instance
cache_service = CacheService()
