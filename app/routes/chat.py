# app/routes/chat.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.chat_memory import add_message, get_short_memory
from app.brain.planner import Planner
from app.services.model_loader import ModelLoader
from openai import OpenAIError

from app.plugins.register_all import register_all_plugins

router = APIRouter()
loader = ModelLoader()
registry = register_all_plugins()

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

@router.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    try:
        message = payload.message.strip()
        session_id = payload.session_id

        # Add user message to memory
        await add_message(session_id, "user", message)

        # Check if message is a plugin invocation
        if message.startswith("/run "):
            parts = message.split(" ", 2)
            if len(parts) < 3:
                raise HTTPException(status_code=400, detail="Invalid /run command format. Use /run <plugin> <input>")

            plugin_name = parts[1]
            plugin_input = parts[2]

            plugin = registry.get(plugin_name)
            if not plugin:
                raise HTTPException(status_code=404, detail=f"Plugin '{plugin_name}' not found")

            plugin.initialize()
            result = plugin.run(plugin_input)
            plugin.shutdown()

            # Add assistant reply
            await add_message(session_id, "assistant", str(result))
            return {"reply": str(result)}

        # Standard LLM Chat
        memory = await get_short_memory(session_id)
        reply = await loader.chat(messages=memory)
        await add_message(session_id, "assistant", reply)

        return {"reply": reply}

    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
