# app/routes/chat.py

from fastapi import APIRouter, Request, HTTPException
from openai import AsyncOpenAI
from app.chat_memory import memory
from app.config import OPENAI_API_KEY

router = APIRouter()
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@router.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        message = data.get("message")
        session_id = data.get("session_id", "default")

        if not message:
            raise HTTPException(status_code=400, detail="Missing 'message' in request body")

        # 🧠 Save user input to memory
        memory.add_message(session_id, "user", message)

        # 🧠 Get conversation history
        history = memory.get_messages(session_id)

        # 🧠 Send to OpenAI
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=history
        )

        assistant_reply = response.choices[0].message.content

        # 🧠 Save assistant reply to memory
        memory.add_message(session_id, "assistant", assistant_reply)

        return { "session_id": session_id, "reply": assistant_reply }

    except HTTPException as http_err:
        raise http_err

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
