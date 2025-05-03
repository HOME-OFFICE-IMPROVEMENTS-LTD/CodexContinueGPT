# app/routes/chat.py

from fastapi import APIRouter, Request, HTTPException
from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from openai import AsyncOpenAI, OpenAIError
from app.codex_prompt_engine.engine import CodexPromptEngine
from pydantic import BaseModel
from typing import Optional

router = APIRouter()
client = AsyncOpenAI(api_key=OPENAI_API_KEY)
prompt_engine = CodexPromptEngine()

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

@router.post("/chat")
async def chat_endpoint(request: Request):
    try:
        body = await request.json()
        data = ChatRequest(**body)
        session_id = data.session_id
        user_input = data.message

        memory.add_message(session_id, "user", user_input)
        history = memory.get_messages(session_id)
        prompt = prompt_engine.build_prompt(history[:-1], user_input)

        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=prompt,
        )

        assistant_reply = response.choices[0].message.content
        memory.add_message(session_id, "assistant", assistant_reply)

        return { "reply": assistant_reply }

    except OpenAIError as e:
        raise HTTPException(status_code=502, detail=f"OpenAI error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
