# app/brain/model_manager.py

from app.config import MODEL_PROVIDER, OPENAI_API_KEY
from openai import AsyncOpenAI
import httpx

class ModelManager:
    def __init__(self):
        if MODEL_PROVIDER == "openai":
            self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        else:
            self.client = None  # Placeholder for Ollama, Azure, etc.

    async def chat(self, session_id: str, messages: list[dict]) -> str:
        if MODEL_PROVIDER == "openai":
            return await self._chat_openai(messages)
        elif MODEL_PROVIDER == "ollama":
            return await self._chat_ollama(messages)
        else:
            raise ValueError(f"Unsupported MODEL_PROVIDER: {MODEL_PROVIDER}")

    async def _chat_openai(self, messages: list[dict]) -> str:
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content

    async def _chat_ollama(self, messages: list[dict]) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "llama3",
                    "messages": messages
                }
            )
            response.raise_for_status()
            data = response.json()
            return data["message"]["content"]

# ✅ Global instance
model_manager = ModelManager()
