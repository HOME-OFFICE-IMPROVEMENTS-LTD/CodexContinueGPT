# app/services/ollama.py

import httpx

class OllamaClient:
    async def chat(self, messages: list[dict]) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:11434/api/chat", json={
                "model": "llama3",
                "messages": messages
            })
            return response.json()["message"]["content"]
