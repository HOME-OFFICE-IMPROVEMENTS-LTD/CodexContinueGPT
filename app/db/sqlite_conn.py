# app/db/sqlite_conn.py

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from contextlib import asynccontextmanager
import os

SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "app/db/memory.db")
SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///{SQLITE_DB_PATH}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

@asynccontextmanager
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
