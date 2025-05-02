# app/routes/chat.py

from fastapi import APIRouter, Request, HTTPException
from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from openai import AsyncOpenAI, OpenAIError

router = APIRouter()
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@router.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message")
        session_id = data.get("session_id", "default")

        if not user_input:
            raise HTTPException(status_code=400, detail="Message is required")

        # Save user message to memory
        memory.add_message(session_id, "user", user_input)

        # Fetch assistant response
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=memory.get_messages(session_id),
        )

        assistant_reply = response.choices[0].message.content.strip()

        # Save assistant response
        memory.add_message(session_id, "assistant", assistant_reply)

        return {"reply": assistant_reply}

    except OpenAIError as e:
        raise HTTPException(status_code=502, detail=f"OpenAI Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")
