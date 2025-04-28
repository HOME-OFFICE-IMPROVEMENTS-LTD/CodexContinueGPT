# app/routes/chat.py

from fastapi import APIRouter, Request, HTTPException
from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from openai import AsyncOpenAI

router = APIRouter()

# Initialize OpenAI Client
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@router.post("/chat")
async def chat(request: Request):
    try:
        # Parse request
        data = await request.json()
        user_input = data.get("message")
        session_id = data.get("session_id", "default")

        if not user_input:
            raise HTTPException(status_code=400, detail="Message field is required.")

        # Save user message
        memory.add_message(session_id, "user", user_input)

        # Call OpenAI
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=memory.get_messages(session_id)
        )

        assistant_reply = response.choices[0].message.content.strip()

        # Save assistant reply
        memory.add_message(session_id, "assistant", assistant_reply)

        return {"session_id": session_id, "reply": assistant_reply}

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        # Log unexpected errors (optional: integrate better logging later)
        print(f"🔥 Unexpected Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
