# app/routes/chat.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from openai import OpenAIError

from app.brain.planner_agent import PlannerAgent

router = APIRouter()
agent = PlannerAgent()

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

@router.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    try:
        result = await agent.run(payload.session_id, payload.message)
        return {
            "reply": result["reply"],
            "tool_used": result.get("tool")
        }

    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
