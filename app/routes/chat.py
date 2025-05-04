# app/routes/chat.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.chat_memory import add_message, get_short_memory
from app.brain.planner import Planner
from app.services.model_loader import ModelLoader
from openai import OpenAIError

from app.plugins.agent_plugin import AgentPlugin

router = APIRouter()
loader = ModelLoader()
agent = AgentPlugin()

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

@router.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    try:
        # Add user message to memory
        await add_message(payload.session_id, "user", payload.message)

        # Check if message should be handled by a plugin
        tool_reply = agent.handle(payload.message, payload.session_id)
        if tool_reply:
            await add_message(payload.session_id, "assistant", tool_reply)
            return {"reply": tool_reply}

        # Get memory context
        memory = await get_short_memory(payload.session_id)

        # Generate model reply
        reply = await loader.chat(messages=memory)

        # Add model reply to memory
        await add_message(payload.session_id, "assistant", reply)

        return {"reply": reply}

    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
