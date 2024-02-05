from redis import asyncio as aioredis


class RedisConnectionManager:
    def __init__(self):
        self.pool = None

    def init(self, dsn: str):
        self.pool = aioredis.from_url(dsn, encoding="utf-8", decode_responses=True)

    async def close(self):
        if self.pool is None:
            # pylint: disable=broad-exception-raised
            raise Exception("RedisConnectionManager is not initialized")
        await self.pool.close()
        self.pool = None


redismanager = RedisConnectionManager()
