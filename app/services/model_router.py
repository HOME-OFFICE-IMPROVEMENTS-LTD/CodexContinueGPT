# app/services/model_router.py

from app.config import MODEL_PROVIDER, OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT
from openai import AsyncOpenAI
import httpx

class ModelRouter:
    def __init__(self):
        self.provider = MODEL_PROVIDER.lower()
        self.client = self._init_client()

    def _init_client(self):
        if self.provider == "openai":
            return AsyncOpenAI(api_key=OPENAI_API_KEY)
        elif self.provider == "azure":
            return AsyncOpenAI(api_key=OPENAI_API_KEY, base_url=AZURE_OPENAI_ENDPOINT)
        else:
            return None  # Ollama & others handled manually

    async def ask(self, messages: list[dict], model="gpt-3.5-turbo") -> str:
        try:
            if self.provider in ["openai", "azure"]:
                response = await self.client.chat.completions.create(
                    model=model,
                    messages=messages
                )
                return response.choices[0].message.content

            elif self.provider == "ollama":
                payload = { "model": model, "messages": messages }
                async with httpx.AsyncClient() as client:
                    res = await client.post("http://localhost:11434/api/chat", json=payload)
                    res.raise_for_status()
                    return res.json()["message"]["content"]

            return "❌ Unknown provider: MODEL_PROVIDER=" + self.provider
        except Exception as e:
            return f"🔥 LLM error: {str(e)}"
