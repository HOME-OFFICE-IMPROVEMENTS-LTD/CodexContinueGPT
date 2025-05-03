import os
import redis.asyncio as redis

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
client = redis.from_url(redis_url, decode_responses=True)

async def save_message(session_id: str, message: str):
    await client.rpush(session_id, message)

async def get_messages(session_id: str, limit=5):
    return await client.lrange(session_id, -limit, -1)
