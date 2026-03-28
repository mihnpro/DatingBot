import json
import logging
from typing import Optional, Any
import redis.asyncio as redis
from redis.asyncio import Redis

logger = logging.getLogger(__name__)


class RedisClient:
    def __init__(self):
        self.client: Optional[Redis] = None
        self.url: Optional[str] = None
    
    async def connect(self, url: Optional[str] = None):
        """Connect to Redis"""
        if not url:
            import os
            url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        
        self.url = url
        self.client = await redis.from_url(url, decode_responses=True)
        
        # Test connection
        await self.client.ping()
        logger.info("Connected to Redis")
    
    async def close(self):
        """Close Redis connection"""
        if self.client:
            await self.client.close()
            logger.info("Closed Redis connection")
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.client:
            return None
        
        value = await self.client.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None
    
    async def set(self, key: str, value: Any, ttl: int = 3600):
        """Set value in cache with TTL"""
        if not self.client:
            return
        
        if not isinstance(value, str):
            value = json.dumps(value)
        
        await self.client.setex(key, ttl, value)
    
    async def delete(self, key: str):
        """Delete value from cache"""
        if self.client:
            await self.client.delete(key)
    
    async def clear_pattern(self, pattern: str):
        """Clear all keys matching pattern"""
        if self.client:
            keys = await self.client.keys(pattern)
            if keys:
                await self.client.delete(*keys)


# Global instance
redis_client = RedisClient()