# app/routes/chat.py

from fastapi import APIRouter, Request, HTTPException
from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from openai import AsyncOpenAI
import logging

router = APIRouter()

# Initialize OpenAI client
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# Logger setup
logger = logging.getLogger(__name__)

@router.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        session_id = data.get("session_id", "default")
        user_input = data.get("message")

        if not user_input:
            raise HTTPException(status_code=400, detail="Missing 'message' field in request.")

        # Save user message to memory
        memory.add_message(session_id, "user", user_input)

        # Call OpenAI asynchronously
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=memory.get_messages(session_id),
        )

        assistant_reply = response.choices[0].message.content

        # Save assistant reply to memory
        memory.add_message(session_id, "assistant", assistant_reply)

        return {"session_id": session_id, "reply": assistant_reply}

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error. Please try again later.")
