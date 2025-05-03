# app/routes/chat.py

from fastapi import APIRouter, HTTPException, Request, status
from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from openai import AsyncOpenAI, OpenAIError
from pydantic import BaseModel
from typing import Optional

router = APIRouter()
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

class ChatRequest(BaseModel):
    session_id: Optional[str] = "default"
    message: str

@router.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        data = ChatRequest(**body)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid input: {str(e)}")

    try:
        # 🧠 Store user message
        memory.add_message(data.session_id, "user", data.message)

        # 🤖 Get assistant reply from OpenAI
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=memory.get_messages(data.session_id)
        )
        reply = response.choices[0].message.content

        # 🧠 Store assistant reply
        memory.add_message(data.session_id, "assistant", reply)

        return {"reply": reply}

    except OpenAIError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"LLM Error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {str(e)}")
