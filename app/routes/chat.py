# app/routes/chat.py

from fastapi import APIRouter, Request, HTTPException
from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from openai import AsyncOpenAI, APIConnectionError, BadRequestError

router = APIRouter()

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@router.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message")
        session_id = data.get("session_id", "default")

        if not user_input:
            raise HTTPException(status_code=400, detail="Message field is required.")

        # Save user message to memory
        memory.add_message(session_id, "user", user_input)

        # Get conversation so far
        messages = memory.get_messages(session_id)

        # Call OpenAI
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        assistant_reply = response.choices[0].message.content

        # Save assistant reply
        memory.add_message(session_id, "assistant", assistant_reply)

        return {
            "session_id": session_id,
            "reply": assistant_reply
        }

    except BadRequestError as e:
        print(f"[400 Error] Bad request: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    except APIConnectionError as e:
        print(f"[503 Error] OpenAI Connection failed: {e}")
        raise HTTPException(status_code=503, detail="Connection to OpenAI failed.")

    except Exception as e:
        print(f"[500 Error] Unexpected server error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
