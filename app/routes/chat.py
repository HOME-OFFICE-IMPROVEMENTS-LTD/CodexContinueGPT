# app/routes/chat.py

from fastapi import APIRouter, Request
from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from openai import AsyncOpenAI
import logging

router = APIRouter()
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@router.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message")
        session_id = data.get("session_id", "default")

        if not user_input:
            return {"error": "Message is required."}

        memory.add_message(session_id, "user", user_input)

        chat_history = memory.get_messages(session_id)

        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_history
        )

        assistant_reply = response.choices[0].message.content
        memory.add_message(session_id, "assistant", assistant_reply)

        return {"reply": assistant_reply}

    except Exception as e:
        logging.exception("Chat endpoint failed")
        return {"error": f"Chat failed: {str(e)}"}
