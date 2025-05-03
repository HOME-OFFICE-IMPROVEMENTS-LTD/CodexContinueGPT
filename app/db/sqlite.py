import aiosqlite
import os

DB_PATH = os.getenv("SQLITE_DB_PATH", "app/db/memory.db")

async def get_db():
    return await aiosqlite.connect(DB_PATH)
