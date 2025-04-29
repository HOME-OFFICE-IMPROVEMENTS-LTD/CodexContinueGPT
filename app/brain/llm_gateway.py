# app/brain/llm_gateway.py

from openai import AsyncOpenAI

class LLMGateway:
    def __init__(self, openai_key=None, azure_endpoint=None, azure_key=None, ollama_base_url=None):
        self.openai_client = AsyncOpenAI(api_key=openai_key) if openai_key else None
        self.azure_endpoint = azure_endpoint
        self.azure_key = azure_key
        self.ollama_base_url = ollama_base_url

    async def chat_openai(self, messages):
        response = await self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        return response.choices[0].message.content

    async def chat_azure(self, messages):
        # Placeholder for Azure OpenAI API call
        pass

    async def chat_ollama(self, messages):
        # Placeholder for Ollama API call
        pass
