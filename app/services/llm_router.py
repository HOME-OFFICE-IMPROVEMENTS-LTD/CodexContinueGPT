# app/services/llm_router.py

import os
from openai import AsyncOpenAI

MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "openai")

# Clients - Initialize as needed
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Placeholder for future providers (e.g., Azure, Ollama)
# TODO: Add AzureOpenAI client, Ollama local inference, etc.

async def chat_completion(messages: list) -> str:
    """
    Universal Chat Completion function.
    Routes to the correct LLM backend based on MODEL_PROVIDER.
    """
    if MODEL_PROVIDER == "openai":
        response = await openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        return response.choices[0].message.content

    elif MODEL_PROVIDER == "azure":
        raise NotImplementedError("Azure OpenAI routing not yet implemented.")

    elif MODEL_PROVIDER == "ollama":
        raise NotImplementedError("Ollama local LLM routing not yet implemented.")

    else:
        raise ValueError(f"Unsupported MODEL_PROVIDER: {MODEL_PROVIDER}")

