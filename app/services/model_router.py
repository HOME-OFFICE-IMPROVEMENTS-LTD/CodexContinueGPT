# app/services/model_router.py

from app.config import MODEL_PROVIDER, OPENAI_API_KEY
from app.chat_memory import memory
from typing import List
from openai import AsyncOpenAI
import httpx

class ModelRouter:
    def __init__(self):
        if MODEL_PROVIDER == "openai":
            self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        elif MODEL_PROVIDER == "azure":
            # Azure-specific initialization (placeholder for future)
            self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)  # Temporary same as OpenAI
        elif MODEL_PROVIDER == "ollama":
            self.client = None  # Ollama does not need client
        else:
            raise ValueError(f"Unsupported MODEL_PROVIDER: {MODEL_PROVIDER}")

    async def generate_response(self, session_id: str, messages: List[dict]) -> str:
        if MODEL_PROVIDER in ["openai", "azure"]:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )
            return response.choices[0].message.content
        
        elif MODEL_PROVIDER == "ollama":
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "http://localhost:11434/api/chat",
                    json={"model": "llama3", "messages": messages},
                    timeout=60
                )
                resp.raise_for_status()
                data = resp.json()
                return data["message"]["content"]

        else:
            raise ValueError("Invalid MODEL_PROVIDER configured.")
