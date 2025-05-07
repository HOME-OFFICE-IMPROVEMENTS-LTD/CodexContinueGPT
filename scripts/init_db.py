import asyncio
import os

from sqlalchemy.ext.asyncio import create_async_engine
from app.db.models import Base

db_path = os.getenv("SQLITE_DB_PATH", "app/db/memory.db")
DATABASE_URL = f"sqlite+aiosqlite:///{db_path}"

engine = create_async_engine(DATABASE_URL, echo=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print(f"✅ SQLite database initialized at {db_path}")

if __name__ == "__main__":
    asyncio.run(init_db())
