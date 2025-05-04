# app/routes/chat.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from openai import OpenAIError

from app.chat_memory import add_message
from app.brain.planner_agent import PlannerAgent

router = APIRouter()
planner = PlannerAgent()

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

@router.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    try:
        # 🧠 Add user message to memory
        await add_message(payload.session_id, "user", payload.message)

        # 🔁 Route through planner agent (plugin or fallback)
        reply = await planner.route(payload.message, payload.session_id)

        # 🧠 Add assistant reply to memory
        await add_message(payload.session_id, "assistant", reply)

        return {"reply": reply}

    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
