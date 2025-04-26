# backend/app/routes/chat.py

from fastapi import APIRouter, Request
import openai
from app.memory import ChatMemory

router = APIRouter()

memory = ChatMemory()  # 🧠 Initialize memory

@router.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message")
    session_id = data.get("session_id", "default")  # 🆔 Get session ID, or fallback to "default"

    if not user_input:
        return {"error": "Message is required."}

    # Save user message in session memory
    memory.add_message(session_id, "user", user_input)

    # Get OpenAI response
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=memory.get_messages(session_id),
    )

    assistant_reply = response.choices[0].message.content

    # Save assistant message in session memory
    memory.add_message(session_id, "assistant", assistant_reply)

    return {"response": assistant_reply}

















