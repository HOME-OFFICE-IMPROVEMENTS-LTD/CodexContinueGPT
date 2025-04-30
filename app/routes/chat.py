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
        user_input = data.get("message")

        if not user_input:
            return JSONResponse(status_code=400, content={"error": "Message is required."})

        # 🧠 Save user message to memory
        memory.add_message(session_id, "user", user_input)

        # 🔥 Send to OpenAI
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=memory.get_messages(session_id),
        )
        assistant_reply = response.choices[0].message.content

        # 💾 Store assistant reply
        memory.add_message(session_id, "assistant", assistant_reply)

        return {"reply": assistant_reply}

    except OpenAIError as oe:
        return JSONResponse(status_code=502, content={"error": f"OpenAI error: {str(oe)}"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Internal Server Error: {str(e)}"})
