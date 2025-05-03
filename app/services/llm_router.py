# app/services/llm_router.py

import os
from openai import AsyncOpenAI
from typing import List, Dict

MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "openai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_API_KEY = os.getenv("AZURE_API_KEY", "")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")

class LLMRouter:
    def __init__(self):
        self.provider = MODEL_PROVIDER.lower()
        self.client = self._init_client()

    def _init_client(self):
        if self.provider == "openai":
            return AsyncOpenAI(api_key=OPENAI_API_KEY)
        elif self.provider == "azure":
            return AsyncOpenAI(
                api_key=AZURE_API_KEY,
                base_url=AZURE_OPENAI_ENDPOINT,
            )
        else:
            return None  # Ollama handled manually via HTTP

    async def generate(self, messages: List[Dict]) -> str:
        if self.provider in ("openai", "azure"):
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )
            return response.choices[0].message.content

        elif self.provider == "ollama":
            import httpx
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{OLLAMA_API_URL}/api/chat",
                    json={"model": "mistral", "messages": messages},
                )
                return resp.json()["message"]["content"]

        else:
            return "❌ Invalid model provider configured."

# Singleton instance for shared use
llm_router = LLMRouter()
