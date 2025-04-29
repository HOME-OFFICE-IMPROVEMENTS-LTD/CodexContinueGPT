# backend/app/routes/chat.py

from fastapi import APIRouter, Request, HTTPException
from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from openai import AsyncOpenAI
from openai import OpenAIError

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

        # Save user message
        memory.add_message(session_id, "user", user_input)

        # Get assistant response
        completion = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=memory.get_messages(session_id)
        )

        assistant_reply = completion.choices[0].message.content

        # Save assistant message
        memory.add_message(session_id, "assistant", assistant_reply)

        return {"reply": assistant_reply}

    except OpenAIError as oe:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {str(oe)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
