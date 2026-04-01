import redis.asyncio as redis
from typing import Optional

class RedisClient:
    def __init__(self, url: str):
        self.url = url
        self._redis: Optional[redis.Redis] = None

    async def connect(self):
        self._redis = await redis.from_url(
            self.url,
            decode_responses=True,
            max_connections=10
        )

    async def close(self):
        if self._redis:
            await self._redis.close()

    @property
    def client(self) -> redis.Redis:
        if self._redis is None:
            raise RuntimeError("Redis not connected")
        return self._redis

    async def set_like(self, from_user: int, to_user: int, ttl: int) -> bool:
        """Сохраняет лайк. Возвращает True если встречный лайк уже существовал, иначе False"""
        key = f"like:{from_user}:{to_user}"
        reverse_key = f"like:{to_user}:{from_user}"


        lua_script = """
        local key = KEYS[1]
        local reverse_key = KEYS[2]
        local ttl = ARGV[1]
        if redis.call('EXISTS', reverse_key) == 1 then
            return 1
        else
            redis.call('SETEX', key, ttl, 1)
            return 0
        end
        """
        result = await self._redis.eval(lua_script, 2, key, reverse_key, ttl)
        return bool(result)

    async def delete_like(self, from_user: int, to_user: int):
        key = f"like:{from_user}:{to_user}"
        await self._redis.delete(key)