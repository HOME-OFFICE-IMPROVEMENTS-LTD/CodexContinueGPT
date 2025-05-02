# app/services/llm_router.py

from app.config import OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT

class LLMRouter:
    def __init__(self, provider: str):
        self.provider = provider.lower()
        self.client = self._init_client()

    def _init_client(self):
        if self.provider == "openai":
            from openai import AsyncOpenAI
            return AsyncOpenAI(api_key=OPENAI_API_KEY)
        elif self.provider == "azure":
            from openai import AzureOpenAI
            return AzureOpenAI(
                api_key=OPENAI_API_KEY,
                api_version="2023-07-01-preview",
                azure_endpoint=AZURE_OPENAI_ENDPOINT
            )
        elif self.provider == "ollama":
            from app.services.ollama import OllamaClient
            return OllamaClient()
        else:
            raise ValueError("Unsupported provider")

    async def chat(self, messages: list[dict]) -> str:
        if self.provider in ["openai", "azure"]:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            return response.choices[0].message.content
        elif self.provider == "ollama":
            return await self.client.chat(messages)
