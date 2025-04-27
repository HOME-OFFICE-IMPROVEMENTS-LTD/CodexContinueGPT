# app/routes/chat.py

from fastapi import APIRouter, Request, HTTPException
from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from app.models.chat_models import ChatRequest
from openai import AsyncOpenAI
from typing import Optional

router = APIRouter()

# Initialize OpenAI Client (default, for OpenAI models)
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@router.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message")
        session_id = data.get("session_id", "default")
        model_provider = data.get("provider", "openai")  # 🧠 NEW: optional field for provider choice
        model_name = data.get("model", "gpt-3.5-turbo")  # 🧠 NEW: optional field for model choice

        if not user_input:
            raise HTTPException(status_code=400, detail="Message field is required.")

        # Save user message
        memory.add_message(session_id, "user", user_input)

        # Prepare conversation history
        conversation = memory.get_messages(session_id)

        # Handle different model providers (multi-LLM routing future-proof)
        if model_provider == "openai":
            response = await client.chat.completions.create(
                model=model_name,
                messages=conversation
            )
            assistant_reply = response.choices[0].message.content
        else:
            raise HTTPException(status_code=400, detail=f"Model provider '{model_provider}' not supported yet.")

        # Save assistant reply
        memory.add_message(session_id, "assistant", assistant_reply)

        return {"reply": assistant_reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
