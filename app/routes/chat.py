# app/routes/chat.py

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from openai import AsyncOpenAI

router = APIRouter()
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@router.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        session_id = data.get("session_id", "default")
        user_input = data.get("message", "").strip()

        if not user_input:
            return JSONResponse(
                status_code=422,
                content={"error": "Missing required 'message' in request body"}
            )

        # Save user input
        memory.add_message(session_id, "user", user_input)

        # Query OpenAI
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=memory.get_messages(session_id)
        )

        reply = response.choices[0].message.content.strip()

        # Save assistant reply
        memory.add_message(session_id, "assistant", reply)

        return {"reply": reply}

    except Exception as e:
        print(f"[❌ Chat Route Error] {str(e)}")  # Future: use logging
        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error", "details": str(e)}
        )
