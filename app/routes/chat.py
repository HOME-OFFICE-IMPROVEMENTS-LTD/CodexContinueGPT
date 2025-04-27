# app/routes/chat.py

from fastapi import APIRouter, Request
from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from openai import AsyncOpenAI

router = APIRouter()

# Create OpenAI client
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@router.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message")
    session_id = data.get("session_id", "default")

    if not user_input:
        return {"error": "Message is required."}

    # Save user message to memory
    memory.add_message(session_id, "user", user_input)

    # Prepare conversation
    conversation = memory.get_messages(session_id)

    # Ask OpenAI
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation,
    )

    assistant_reply = response.choices[0].message.content

    # Save assistant reply to memory
    memory.add_message(session_id, "assistant", assistant_reply)

    return {"reply": assistant_reply}
