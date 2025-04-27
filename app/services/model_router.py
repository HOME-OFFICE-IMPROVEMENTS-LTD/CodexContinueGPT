# app/services/model_router.py

from app.config import MODEL_PROVIDER, OPENAI_API_KEY
from openai import AsyncOpenAI
from fastapi import HTTPException

# Create OpenAI client (default)
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def route_prompt(session_id: str, messages: list):
    if MODEL_PROVIDER == "openai":
        return await query_openai(messages)
    elif MODEL_PROVIDER == "azure":
        return await query_azure_openai(messages)
    elif MODEL_PROVIDER == "ollama":
        return await query_ollama(messages)
    else:
        raise HTTPException(status_code=500, detail=f"Unknown MODEL_PROVIDER: {MODEL_PROVIDER}")

async def query_openai(messages):
    response = await openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content

async def query_azure_openai(messages):
    # Future: Add Azure OpenAI calling here
    raise NotImplementedError("Azure OpenAI integration coming soon.")

async def query_ollama(messages):
    # Future: Add Ollama (local LLM) integration here
    raise NotImplementedError("Ollama local LLM support coming soon.")
