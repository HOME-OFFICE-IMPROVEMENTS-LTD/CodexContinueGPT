# app/services/model_router.py

from app.config import MODEL_PROVIDER, OPENAI_API_KEY
from fastapi import HTTPException
from openai import AsyncOpenAI

# Create OpenAI Async Client
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def route_prompt(session_id: str, messages: list) -> dict:
    """
    Routes the incoming prompt to the correct LLM provider based on MODEL_PROVIDER.
    Returns a standardized dict {reply: str, usage: dict}.
    """
    try:
        if MODEL_PROVIDER == "openai":
            return await query_openai(messages)
        elif MODEL_PROVIDER == "azure":
            return await query_azure_openai(messages)
        elif MODEL_PROVIDER == "ollama":
            return await query_ollama(messages)
        else:
            raise HTTPException(status_code=500, detail=f"❌ Unknown MODEL_PROVIDER: {MODEL_PROVIDER}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"🛡️ LLM Routing Error: {str(e)}")

async def query_openai(messages: list) -> dict:
    try:
        response = await openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            stream=False,
        )
        return {
            "reply": response.choices[0].message.content,
            "usage": response.usage.model_dump() if hasattr(response, 'usage') else {}
        }
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"🔌 OpenAI Query Failed: {str(e)}")

async def query_azure_openai(messages: list) -> dict:
    # 🚧 Future Azure Integration
    raise HTTPException(status_code=501, detail="Azure OpenAI integration coming soon. 🚀")

async def query_ollama(messages: list) -> dict:
    # 🚧 Future Ollama Integration
    raise HTTPException(status_code=501, detail="Ollama (local LLM) integration coming soon. 🧠")
