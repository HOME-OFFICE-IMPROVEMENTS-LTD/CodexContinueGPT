# app/routes/chat.py

from fastapi import APIRouter, Request, HTTPException
from app.chat_memory import memory
from app.config import MODEL_PROVIDER, OPENAI_API_KEY
from openai import AsyncOpenAI

router = APIRouter()
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@router.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message")
        session_id = data.get("session_id", "default")

        if not user_input:
            raise HTTPException(status_code=422, detail="Missing 'message' field.")

        # Save user input to memory
        memory.add_message(session_id, "user", user_input)

        # Generate assistant reply
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=memory.get_messages(session_id),
        )

        assistant_reply = response.choices[0].message.content
        memory.add_message(session_id, "assistant", assistant_reply)

        return {"reply": assistant_reply}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")
