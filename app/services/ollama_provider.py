# app/services/ollama_provider.py

import httpx
from app.services.base_provider import BaseProvider

class OllamaProvider(BaseProvider):
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url

    async def chat(self, messages: list, model: str = "mistral"):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.base_url}/api/chat", json={
                    "model": model,
                    "messages": messages
                })
                response.raise_for_status()
                result = response.json()
                return result['message']['content']
        except Exception as e:
            return f"Ollama Error: {str(e)}"
