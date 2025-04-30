# app/routes/chat.py

from fastapi import APIRouter, Request, HTTPException
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
            raise HTTPException(status_code=422, detail="Message is required.")

        memory.add_message(session_id, "user", user_input)

        try:
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=memory.get_messages(session_id)
            )
            assistant_reply = response.choices[0].message.content
        except Exception as e:
            logging.error(f"[OpenAI Error] {e}")
            assistant_reply = "⚠️ Sorry, I couldn’t reach my brain right now. Try again soon."

        memory.add_message(session_id, "assistant", assistant_reply)
        return {"reply": assistant_reply}

    except HTTPException as he:
        raise he
    except Exception as e:
        logging.exception("[Internal Server Error]")
        raise HTTPException(status_code=500, detail="Unexpected server error.")
