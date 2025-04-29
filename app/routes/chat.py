# app/routes/chat.py

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from openai import AsyncOpenAI, OpenAIError

router = APIRouter()
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@router.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        session_id = data.get("session_id", "default")
        user_message = data.get("message")

        if not user_message:
            return JSONResponse(status_code=400, content={"error": "Message field is required."})

        memory.add_message(session_id, "user", user_message)

        # 🤖 Call OpenAI
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=memory.get_messages(session_id)
        )

        assistant_reply = response.choices[0].message.content.strip()
        memory.add_message(session_id, "assistant", assistant_reply)

        return JSONResponse(status_code=200, content={"reply": assistant_reply})

    except OpenAIError as oe:
        return JSONResponse(status_code=502, content={"error": f"OpenAI Error: {str(oe)}"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Internal Server Error: {str(e)}"})
