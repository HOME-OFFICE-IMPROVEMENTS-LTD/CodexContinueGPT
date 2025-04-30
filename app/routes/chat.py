# app/routes/chat.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from openai import AsyncOpenAI

router = APIRouter()
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

class ChatRequest(BaseModel):
    session_id: Optional[str] = "default"
    message: str

@router.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    try:
        memory.add_message(payload.session_id, "user", payload.message)

        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=memory.get_messages(payload.session_id),
        )

        reply = response.choices[0].message.content.strip()
        memory.add_message(payload.session_id, "assistant", reply)

        return {"reply": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
