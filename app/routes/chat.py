# app/routes/chat.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.chat_memory import add_message, get_short_memory
from app.brain.planner import Planner
from app.services.model_loader import ModelLoader
from openai import OpenAIError

router = APIRouter()
loader = ModelLoader()

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

@router.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    try:
        # Add user message to memory
        await add_message(payload.session_id, "user", payload.message)

        # Get short memory
        memory = await get_short_memory(payload.session_id)

        # Call model
        reply = await loader.chat(messages=memory)

        # Add assistant reply to memory
        await add_message(payload.session_id, "assistant", reply)

        return {"reply": reply}

    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
