# app/routes/chat.py

from fastapi import APIRouter, Request, HTTPException
from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessage
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
            raise HTTPException(status_code=400, detail="Missing 'message' in request.")

        memory.add_message(session_id, "user", user_input)

        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=memory.get_messages(session_id),
        )

        assistant_reply = response.choices[0].message.content
        memory.add_message(session_id, "assistant", assistant_reply)

        return {
            "session_id": session_id,
            "reply": assistant_reply,
            "status": "success"
        }

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logging.exception("Error in /chat endpoint")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
