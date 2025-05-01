# app/routes/chat.py

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

router = APIRouter()
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@router.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message")
        session_id = data.get("session_id", "default")

        if not user_input:
            return JSONResponse(status_code=400, content={"error": "Missing 'message' in request body."})

        memory.add_message(session_id, "user", user_input)

        messages: list[ChatCompletionMessageParam] = memory.get_messages(session_id)

        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        assistant_reply = response.choices[0].message.content
        memory.add_message(session_id, "assistant", assistant_reply)

        return {"reply": assistant_reply}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
