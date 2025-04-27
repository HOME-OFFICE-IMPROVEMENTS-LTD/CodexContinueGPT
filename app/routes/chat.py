# app/routes/chat.py

from fastapi import APIRouter, Request, HTTPException
from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from openai import AsyncOpenAI

router = APIRouter()

# Create OpenAI client
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@router.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        session_id = data.get("session_id", "default")
        user_input = data.get("message")

        if not user_input:
            raise HTTPException(status_code=400, detail="Message field is required.")

        # 🧠 Save user message into memory
        memory.add_message(session_id, "user", user_input)

        # 🧠 Retrieve full conversation history
        conversation = memory.get_messages(session_id)

        # 🤖 Send conversation to OpenAI
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )

        assistant_reply = response.choices[0].message.content

        # 🧠 Save assistant reply
        memory.add_message(session_id, "assistant", assistant_reply)

        return {"reply": assistant_reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
