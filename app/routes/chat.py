# app/routes/chat.py

from fastapi import APIRouter, Request, HTTPException
from openai import AsyncOpenAI
from app.chat_memory import memory
from app.config import OPENAI_API_KEY, MODEL_PROVIDER

router = APIRouter()
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@router.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        message = data.get("message")
        session_id = data.get("session_id", "default")

        if not message:
            raise HTTPException(status_code=400, detail="Message is required.")

        memory.add_message(session_id, "user", message)

        # Multi-model support (future-ready)
        if MODEL_PROVIDER == "openai":
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=memory.get_messages(session_id)
            )
            reply = response.choices[0].message.content
        elif MODEL_PROVIDER == "azure":
            raise HTTPException(status_code=501, detail="Azure provider not implemented yet.")
        elif MODEL_PROVIDER == "ollama":
            raise HTTPException(status_code=501, detail="Ollama provider not implemented yet.")
        else:
            raise HTTPException(status_code=400, detail="Unsupported MODEL_PROVIDER")

        memory.add_message(session_id, "assistant", reply)
        return {"reply": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
