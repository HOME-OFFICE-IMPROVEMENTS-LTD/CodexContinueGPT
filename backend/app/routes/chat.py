from fastapi import APIRouter, Request
from app.chat_memory import memory
import openai
from app.config import OPENAI_API_KEY

router = APIRouter()

openai.api_key = OPENAI_API_KEY

@router.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message")
    session_id = data.get("session_id", "default")

    if not user_input:
        return {"error": "Message is required."}

    # 🧠 Save user input into memory
    memory.add_message(session_id, "user", user_input)

    # 🧠 Prepare full conversation history for OpenAI
    conversation = memory.get_messages(session_id)

    # 🔥 Send to OpenAI ChatCompletion
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    assistant_reply = response["choices"][0]["message"]["content"]

    # 🧠 Save assistant reply into memory
    memory.add_message(session_id, "assistant", assistant_reply)

    return {"reply": assistant_reply}
