
from fastapi import APIRouter, Request, HTTPException
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
async def chat(request: Request):
    try:
        data = await request.json()
        chat_input = ChatRequest(**data)

        # Save user message
        memory.add_message(chat_input.session_id, "user", chat_input.message)

        # Query OpenAI
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=memory.get_messages(chat_input.session_id)
        )

        assistant_reply = response.choices[0].message.content
        memory.add_message(chat_input.session_id, "assistant", assistant_reply)

        return {"reply": assistant_reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI Error: {str(e)}")
