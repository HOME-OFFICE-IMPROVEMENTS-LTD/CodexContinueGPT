# app/services/provider_router.py

from app.config import MODEL_PROVIDER, OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT
from openai import AsyncOpenAI

def get_openai_client():
    return AsyncOpenAI(api_key=OPENAI_API_KEY)

def get_model_config():
    if MODEL_PROVIDER == "azure":
        return {
            "model": None,
            "engine": "gpt-35-turbo",
            "api_base": AZURE_OPENAI_ENDPOINT,
            "api_version": "2023-05-15",
        }
    elif MODEL_PROVIDER == "ollama":
        return {
            "model": "mistral",  # default Ollama model
            "api_base": "http://localhost:11434",
        }
    else:
        return {
            "model": "gpt-3.5-turbo",
        }
