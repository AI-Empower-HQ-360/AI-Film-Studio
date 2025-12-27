"""Mock Redis service for testing"""
import fakeredis
from typing import Any, Optional


class MockRedisService:
    """Mock Redis service for testing"""
    
    def __init__(self):
        """Initialize mock Redis client"""
        self.client = fakeredis.FakeStrictRedis(decode_responses=True)
    
    def get(self, key: str) -> Optional[str]:
        """Get value from Redis"""
        return self.client.get(key)
    
    def set(self, key: str, value: Any, ex: Optional[int] = None) -> bool:
        """Set value in Redis with optional expiration"""
        return self.client.set(key, value, ex=ex)
    
    def delete(self, key: str) -> int:
        """Delete key from Redis"""
        return self.client.delete(key)
    
    def exists(self, key: str) -> bool:
        """Check if key exists in Redis"""
        return self.client.exists(key) > 0
    
    def expire(self, key: str, seconds: int) -> bool:
        """Set expiration on key"""
        return self.client.expire(key, seconds)
    
    def ttl(self, key: str) -> int:
        """Get time to live for key"""
        return self.client.ttl(key)
    
    def incr(self, key: str) -> int:
        """Increment value"""
        return self.client.incr(key)
    
    def decr(self, key: str) -> int:
        """Decrement value"""
        return self.client.decr(key)
    
    def hset(self, name: str, key: str, value: Any) -> int:
        """Set hash field"""
        return self.client.hset(name, key, value)
    
    def hget(self, name: str, key: str) -> Optional[str]:
        """Get hash field"""
        return self.client.hget(name, key)
    
    def hgetall(self, name: str) -> dict:
        """Get all hash fields"""
        return self.client.hgetall(name)
    
    def hdel(self, name: str, *keys) -> int:
        """Delete hash fields"""
        return self.client.hdel(name, *keys)
    
    def lpush(self, key: str, *values) -> int:
        """Push values to list"""
        return self.client.lpush(key, *values)
    
    def rpush(self, key: str, *values) -> int:
        """Push values to list from right"""
        return self.client.rpush(key, *values)
    
    def lpop(self, key: str) -> Optional[str]:
        """Pop value from list"""
        return self.client.lpop(key)
    
    def rpop(self, key: str) -> Optional[str]:
        """Pop value from list from right"""
        return self.client.rpop(key)
    
    def lrange(self, key: str, start: int, end: int) -> list:
        """Get range from list"""
        return self.client.lrange(key, start, end)
    
    def sadd(self, key: str, *values) -> int:
        """Add values to set"""
        return self.client.sadd(key, *values)
    
    def smembers(self, key: str) -> set:
        """Get all members of set"""
        return self.client.smembers(key)
    
    def srem(self, key: str, *values) -> int:
        """Remove values from set"""
        return self.client.srem(key, *values)
    
    def flushall(self) -> bool:
        """Clear all data"""
        return self.client.flushall()
    
    def flushdb(self) -> bool:
        """Clear current database"""
        return self.client.flushdb()
    
    def keys(self, pattern: str = "*") -> list:
        """Get keys matching pattern"""
        return self.client.keys(pattern)


# Example usage in tests:
# def test_redis_integration():
#     redis = MockRedisService()
#     
#     # Test basic operations
#     redis.set("key", "value")
#     assert redis.get("key") == "value"
#     
#     # Test expiration
#     redis.set("temp_key", "temp_value", ex=60)
#     assert redis.ttl("temp_key") > 0
#     
#     # Test hash operations
#     redis.hset("user:1", "name", "John")
#     redis.hset("user:1", "age", "30")
#     user_data = redis.hgetall("user:1")
#     assert user_data["name"] == "John"
#     
#     # Cleanup
#     redis.flushall()
