# app/routes/sessions.py

from fastapi import APIRouter
from sqlalchemy import select, distinct
from app.db.sqlite_conn import get_db
from app.db.models import Message

router = APIRouter()

@router.get("/sessions")
async def list_sessions():
    async with get_db() as db:
        result = await db.execute(select(distinct(Message.session_id)))
        sessions = [row[0] for row in result.fetchall()]
        return {"sessions": sorted(sessions)}
