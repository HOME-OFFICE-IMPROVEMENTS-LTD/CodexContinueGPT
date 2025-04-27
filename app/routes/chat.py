# app/routes/chat.py

from fastapi import APIRouter, Request, HTTPException
from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from openai import AsyncOpenAI, OpenAIError

router = APIRouter()

# Initialize OpenAI Async Client
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@router.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message")
        session_id = data.get("session_id", "default")

        if not user_message:
            raise HTTPException(status_code=400, detail="Missing user message")

        # 🧠 Save user input
        memory.add_message(session_id, "user", user_message)

        # 📡 Call OpenAI
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=memory.get_messages(session_id),
        )

        assistant_reply = response.choices[0].message.content

        # 🧠 Save assistant reply
        memory.add_message(session_id, "assistant", assistant_reply)

        return {
            "reply": assistant_reply,
            "session_id": session_id,
        }

    except OpenAIError as oe:
        raise HTTPException(status_code=500, detail=f"OpenAI API Error: {str(oe)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
