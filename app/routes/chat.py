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
        session_id = data.get("session_id", "default")
        user_message = data.get("message")

        if not user_message:
            raise HTTPException(status_code=400, detail="Missing user message.")

        # Save user input to memory
        memory.add_message(session_id, "user", user_message)

        # Get past context
        messages = memory.get_messages(session_id)

        # Query OpenAI model
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        reply = response.choices[0].message.content

        # Store reply
        memory.add_message(session_id, "assistant", reply)

        return {"reply": reply}

    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI Error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")
