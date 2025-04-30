# app/routes/chat.py

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from openai import AsyncOpenAI
import logging

router = APIRouter()
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

logger = logging.getLogger("codexcontinue.chat")
logging.basicConfig(level=logging.INFO)

@router.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message")
        session_id = data.get("session_id", "default")

        if not user_input:
            raise HTTPException(status_code=400, detail="Message field is required.")

        memory.add_message(session_id, "user", user_input)

        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=memory.get_messages(session_id),
        )

        assistant_reply = response.choices[0].message.content
        memory.add_message(session_id, "assistant", assistant_reply)

        logger.info(f"[{session_id}] User: {user_input} | Assistant: {assistant_reply}")
        return JSONResponse(status_code=200, content={"reply": assistant_reply})

    except Exception as e:
        logger.error(f"❌ Chat failed: {str(e)}")
        fallback_message = (
            "⚠️ Sorry, something went wrong while processing your request."
        )
        return JSONResponse(status_code=500, content={"reply": fallback_message})
