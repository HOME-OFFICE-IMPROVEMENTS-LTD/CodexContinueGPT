# app/brain/llm_router.py

from app.config import MODEL_PROVIDER, OPENAI_API_KEY
from openai import AsyncOpenAI
import httpx
import os

class LLMRouter:
    def __init__(self):
        self.provider = MODEL_PROVIDER.lower()

    async def chat(self, messages: list):
        if self.provider == "openai":
            return await self._chat_with_openai(messages)
        elif self.provider == "ollama":
            return await self._chat_with_ollama(messages)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    async def _chat_with_openai(self, messages: list):
        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content

    async def _chat_with_ollama(self, messages: list):
        # �� Ollama expects a string prompt (we'll collapse messages)
        prompt = "\n".join(f"{m['role']}: {m['content']}" for m in messages)
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama3", "prompt": prompt, "stream": False}
            )
        return response.json().get("response", "[Error: no response]")
