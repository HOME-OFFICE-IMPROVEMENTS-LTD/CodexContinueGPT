# app/routes/chat.py

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from openai import AsyncOpenAI
import time

router = APIRouter()
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@router.post("/chat")
async def chat(request: Request):
    start_time = time.time()

    try:
        data = await request.json()
        session_id = data.get("session_id", "default")
        message = data.get("message")

        if not message:
            return JSONResponse(
                status_code=400,
                content={"error": "Message field is required."}
            )

        # 🧠 Save user message to memory
        memory.add_message(session_id, "user", message)

        # 🔥 Call LLM
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=memory.get_messages(session_id)
        )

        assistant_reply = response.choices[0].message.content.strip()

        # 🧠 Save assistant reply
        memory.add_message(session_id, "assistant", assistant_reply)

        duration = round(time.time() - start_time, 2)

        return JSONResponse(
            status_code=200,
            content={
                "reply": assistant_reply,
                "session_id": session_id,
                "duration": duration,
                "tokens": response.usage.total_tokens if hasattr(response, "usage") else None
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "An unexpected error occurred.",
                "details": str(e)
            }
        )
