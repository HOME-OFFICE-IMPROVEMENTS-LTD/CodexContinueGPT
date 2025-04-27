# app/routes/chat.py

from fastapi import APIRouter, Request, HTTPException
from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from openai import AsyncOpenAI, OpenAIError
import asyncio

router = APIRouter()

# Initialize OpenAI client
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@router.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        session_id = data.get("session_id", "default")
        user_input = data.get("message")

        if not user_input:
            raise HTTPException(status_code=400, detail="Missing 'message' in request.")

        # Save user message to memory
        memory.add_message(session_id, "user", user_input)

        # Query OpenAI with timeout protection
        try:
            response = await asyncio.wait_for(
                client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=memory.get_messages(session_id)
                ),
                timeout=20  # Timeout after 20 seconds
            )
        except asyncio.TimeoutError:
            raise HTTPException(status_code=504, detail="OpenAI API timeout.")
        except OpenAIError as e:
            raise HTTPException(status_code=502, detail=f"OpenAI API error: {str(e)}")

        assistant_reply = response.choices[0].message.content

        # Save assistant reply to memory
        memory.add_message(session_id, "assistant", assistant_reply)

        return {"reply": assistant_reply}

    except HTTPException as http_exc:
        raise http_exc  # Propagate HTTP errors correctly

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
