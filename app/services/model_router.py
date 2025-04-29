# app/services/model_router.py

from app.config import MODEL_PROVIDER, OPENAI_API_KEY
from openai import AsyncOpenAI
import httpx, os

class ModelRouter:
    def __init__(self):
        self.provider = MODEL_PROVIDER.lower()
        self.client = self._get_client()

    def _get_client(self):
        if self.provider == "openai":
            return AsyncOpenAI(api_key=OPENAI_API_KEY)
        elif self.provider == "azure":
            return AsyncOpenAI(
                api_key=os.getenv("AZURE_OPENAI_KEY"),
                base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
                default_headers={"api-key": os.getenv("AZURE_OPENAI_KEY")},
            )
        elif self.provider == "ollama":
            return httpx.AsyncClient(base_url="http://localhost:11434")
        else:
            raise ValueError(f"❌ Unsupported MODEL_PROVIDER: {self.provider}")

    async def chat(self, messages, model="gpt-3.5-turbo"):
        if self.provider in ["openai", "azure"]:
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
            )
            return response.choices[0].message.content
        elif self.provider == "ollama":
            payload = {"model": "llama3", "messages": messages}
            resp = await self.client.post("/api/chat", json=payload)
            return resp.json()["message"]["content"]
