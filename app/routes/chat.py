# app/routes/chat.py

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from openai import AsyncOpenAI
import traceback

router = APIRouter()

# Create OpenAI client
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@router.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message")
        session_id = data.get("session_id", "default")

        if not user_input:
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": "Message is required."}
            )

        # �� Save user input
        memory.add_message(session_id, "user", user_input)

        # 🔥 Query OpenAI
        chat_response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=memory.get_messages(session_id),
        )

        assistant_reply = chat_response.choices[0].message.content.strip()

        # 🧠 Save assistant reply
        memory.add_message(session_id, "assistant", assistant_reply)

        return JSONResponse(
            status_code=200,
            content={"success": True, "reply": assistant_reply}
        )

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
