# app/db/init_db.py

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.db.models import Base
import os

SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "app/db/memory.db")
DATABASE_URL = f"sqlite+aiosqlite:///{SQLITE_DB_PATH}"

engine = create_async_engine(DATABASE_URL, future=True, echo=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())
