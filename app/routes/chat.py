# app/routes/chat.py

from fastapi import APIRouter, Request, HTTPException
from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from openai import AsyncOpenAI
import openai

router = APIRouter()

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@router.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message")
        session_id = data.get("session_id", "default")

        if not user_input:
            raise HTTPException(status_code=422, detail="Message field is required.")

        # Save user message
        memory.add_message(session_id, "user", user_input)

        # Get assistant reply
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=memory.get_messages(session_id),
        )

        assistant_reply = response.choices[0].message.content

        # Save assistant reply
        memory.add_message(session_id, "assistant", assistant_reply)

        return {"status": "success", "reply": assistant_reply}

    except openai.APIError as e:
        raise HTTPException(status_code=503, detail=f"OpenAI API Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected Error: {str(e)}")
