# backend/app/services/model_service.py

from app.config import MODEL_PROVIDER, OPENAI_API_KEY
from app.chat_memory import memory
from openai import AsyncOpenAI
from fastapi import HTTPException

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def generate_response(session_id: str, user_input: str) -> str:
    memory.add_message(session_id, "user", user_input)
    conversation = memory.get_messages(session_id)

    try:
        if MODEL_PROVIDER == "openai":
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation,
            )
            assistant_reply = response.choices[0].message.content

        elif MODEL_PROVIDER == "azure_openai":
            assistant_reply = "Azure OpenAI not yet implemented."

        elif MODEL_PROVIDER == "ollama":
            assistant_reply = "Ollama model not yet implemented."

        elif MODEL_PROVIDER == "github_copilot":
            assistant_reply = "GitHub Copilot integration not yet implemented."

        else:
            raise HTTPException(status_code=400, detail="Invalid MODEL_PROVIDER configured.")
        
        memory.add_message(session_id, "assistant", assistant_reply)
        return assistant_reply

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM provider error: {str(e)}")
