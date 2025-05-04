# app/memory/manager.py

from typing import List, Dict
from app.db.sqlite_conn import get_db
from app.db.models import Message
from redis import asyncio as aioredis
from datetime import datetime
import json
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "app/db/memory.db")

class MemoryManager:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.redis = aioredis.from_url(REDIS_URL, decode_responses=True)

    async def save_message(self, role: str, content: str):
        message = {"role": role, "content": content, "timestamp": datetime.utcnow().isoformat()}
        await self.redis.rpush(self.session_id, json.dumps(message))
        async with get_db() as db:
            db.add(Message(session_id=self.session_id, role=role, content=content))
            await db.commit()

    async def get_messages(self, mode: str = "short", limit: int = 5) -> List[Dict]:
        try:
            redis_range = (-limit if mode == "short" else 0, -1)
            messages = await self.redis.lrange(self.session_id, *redis_range)
            return [json.loads(m) for m in messages]
        except Exception:
            async with get_db() as db:
                query = await db.execute(
                    f"""
                    SELECT role, content FROM messages
                    WHERE session_id = :session_id
                    ORDER BY timestamp DESC
                    LIMIT :limit
                    """,
                    {"session_id": self.session_id, "limit": limit if mode == "short" else 1000}
                )
                rows = query.fetchall()
                return [{"role": row[0], "content": row[1]} for row in rows[::-1]]

    async def reset(self):
        await self.redis.delete(self.session_id)
        async with get_db() as db:
            await db.execute(
                "DELETE FROM messages WHERE session_id = :session_id",
                {"session_id": self.session_id}
            )
            await db.commit()

    async def audit_summary(self) -> Dict:
        try:
            redis_count = await self.redis.llen(self.session_id)
        except:
            redis_count = -1

        async with get_db() as db:
            result = await db.execute(
                "SELECT COUNT(*) FROM messages WHERE session_id = :sid",
                {"sid": self.session_id}
            )
            sqlite_count = result.scalar()

        return {
            "session": self.session_id,
            "redis_count": redis_count,
            "sqlite_count": sqlite_count,
        }
