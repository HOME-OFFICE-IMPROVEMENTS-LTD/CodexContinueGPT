# app/routes/chat.py

from fastapi import APIRouter, Request, HTTPException
from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from openai import AsyncOpenAI, APIConnectionError, BadRequestError

router = APIRouter()

# OpenAI client (new SDK)
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@router.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message")
        session_id = data.get("session_id", "default")

        if not user_input:
            raise HTTPException(status_code=422, detail="Missing 'message' in request.")

        # 🧠 Add user message to memory
        memory.add_message(session_id, "user", user_input)

        # 🤖 Call LLM
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=memory.get_messages(session_id)
        )

        assistant_reply = response.choices[0].message.content

        # 🧠 Save assistant message
        memory.add_message(session_id, "assistant", assistant_reply)

        return {"session_id": session_id, "reply": assistant_reply}

    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except APIConnectionError:
        raise HTTPException(status_code=503, detail="Failed to connect to OpenAI API.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
