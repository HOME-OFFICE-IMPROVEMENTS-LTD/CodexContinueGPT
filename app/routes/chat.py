# app/routes/chat.py

from fastapi import APIRouter, Request, HTTPException
from app.chat_memory import memory
from app.services.model_router import ModelRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()
router_model = ModelRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

@router.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        data = ChatRequest(**body)
        session_id = data.session_id
        user_input = data.message

        memory.add_message(session_id, "user", user_input)

        response = await router_model.ask(memory.get_messages(session_id))

        memory.add_message(session_id, "assistant", response)

        return { "reply": response }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
