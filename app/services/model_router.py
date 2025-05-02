# app/services/model_router.py

import os
import httpx
import logging
from openai import AsyncOpenAI
from app.config import MODEL_PROVIDER, OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo")

class ModelRouter:
    def __init__(self):
        self.provider = MODEL_PROVIDER.lower()
        self.client = self._get_client()

    def _get_client(self):
        if self.provider == "openai":
            return AsyncOpenAI(api_key=OPENAI_API_KEY)
        elif self.provider == "azure":
            return AsyncOpenAI(api_key=OPENAI_API_KEY, base_url=AZURE_OPENAI_ENDPOINT)
        return None  # Ollama or unsupported

    async def ask(self, messages: list, model: str = DEFAULT_MODEL) -> str:
        try:
            if self.provider in ["openai", "azure"]:
                response = await self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                )
                return response.choices[0].message.content

            elif self.provider == "ollama":
                payload = {
                    "model": model,
                    "messages": messages,
                    "stream": False
                }
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.post("http://localhost:11434/api/chat", json=payload)
                    resp.raise_for_status()
                    data = resp.json()
                    return data.get("message", {}).get("content", "⚠️ No content returned.")

            else:
                logging.error(f"Unsupported model provider: {self.provider}")
                return "❌ Unsupported MODEL_PROVIDER in .env"

        except Exception as e:
            logging.exception("🔥 ModelRouter failed")
            return f"🔥 Model error: {str(e)}"
