# app/routes/chat.py

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from openai import AsyncOpenAI
from pydantic import BaseModel
from typing import Optional

router = APIRouter()
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

@router.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    try:
        # Save user message
        memory.add_message(payload.session_id, "user", payload.message)

        # Call OpenAI with memory context
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=memory.get_messages(payload.session_id)
        )

        reply = response.choices[0].message.content.strip()

        # Save assistant message
        memory.add_message(payload.session_id, "assistant", reply)

        return {"reply": reply, "session_id": payload.session_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Assistant error: {str(e)}")
