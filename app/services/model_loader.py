import os
import httpx

class ModelLoader:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.api_endpoint = os.getenv('API_ENDPOINT', 'https://api.openai.com/v1/chat/completions')

    async def chat(self, messages: list[dict], model="gpt-3.5-turbo", service="openai") -> str:
        async with httpx.AsyncClient() as client:
            try:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }

                payload = {
                    "model": model,
                    "messages": messages,
                    "temperature": 0.7
                }

                # Optional routing logic
                if service == "azure":
                    self.api_endpoint = os.getenv('AZURE_API_ENDPOINT', self.api_endpoint)
                elif service == "ollama":
                    self.api_endpoint = os.getenv('OLLAMA_API_ENDPOINT', self.api_endpoint)

                response = await client.post(self.api_endpoint, headers=headers, json=payload)
                response.raise_for_status()
                response_data = response.json()
                return response_data["choices"][0]["message"]["content"]

            except httpx.HTTPStatusError as exc:
                return f"HTTP error: {exc.response.status_code} - {exc.response.text}"
            except Exception as exc:
                return f"Unexpected error: {str(exc)}"
