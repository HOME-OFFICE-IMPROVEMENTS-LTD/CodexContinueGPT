import os
import httpx
import json
import logging
from typing import Dict, List, Optional, Any
from app.plugins.registry import CodexTool

# Setup logging
logger = logging.getLogger(__name__)

# Configuration for OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")  # Default to more efficient model
FALLBACK_MODEL = "gpt-4o-mini"  # Secondary model if primary fails
REQUEST_TIMEOUT = float(os.getenv("OPENAI_TIMEOUT", "30.0"))  # Timeout in seconds

class OpenAIFallback(CodexTool):
    name = "OpenAIFallback"
    description = "Primary LLM using OpenAI's API"
    
    async def _query_openai(self, input_text: str, model: str = DEFAULT_MODEL, api_key: Optional[str] = None) -> Optional[str]:
        """Query OpenAI API with the given input text"""
        # Use provided API key or fall back to environment variable
        api_key = api_key or OPENAI_API_KEY
        
        if not api_key:
            logger.warning("OpenAI API key not set. Please set OPENAI_API_KEY environment variable.")
            return None
            
        messages = [
            {"role": "user", "content": input_text}
        ]
        
        try:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
                logger.info(f"Sending request to OpenAI {model} model with message: {input_text[:50]}...")
                
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": model,
                    "messages": messages
                }
                
                response = await client.post(
                    f"{OPENAI_BASE_URL}/chat/completions", 
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                logger.info(f"Received response from {model} model")
                return data.get("choices", [{}])[0].get("message", {}).get("content", None)
        except Exception as e:
            logger.error(f"Error querying OpenAI {model} model: {str(e)}")
            return None

    async def run(self, input_text: str, api_key: Optional[str] = None, model: Optional[str] = None) -> Optional[Any]:
        """Run the OpenAI fallback tool with the given input text. Returns str, dict, or None."""
        try:
            # Use provided API key or fall back to environment variable
            api_key = api_key or OPENAI_API_KEY
            # Use provided model or fall back to default
            use_model = model or DEFAULT_MODEL
            
            # Check if API key is set
            if not api_key or api_key == "your-openai-api-key" or api_key == "your-openai-api-key-here":
                logger.error("Invalid OpenAI API key. Please set a valid OPENAI_API_KEY environment variable.")
                # Return a helpful message instead of None
                return {
                    "output": "I need an OpenAI API key to work properly. Please set the OPENAI_API_KEY environment variable."
                }
                
            logger.info(f"Using model: {use_model}")
            # Try with specified/default model
            response = await self._query_openai(input_text, use_model, api_key)
            if response:
                return response
                
            # If specified model fails, try fallback model
            logger.warning(f"Model {use_model} failed, trying fallback model {FALLBACK_MODEL}")
            response = await self._query_openai(input_text, FALLBACK_MODEL, api_key)
            if response:
                return response
                
            # If both models fail, indicate that we should try the next fallback plugin
            logger.error("All OpenAI models failed")
            return None
            
        except Exception as e:
            logger.error(f"OpenAI fallback error: {str(e)}")
            return None

    async def execute(self, data, *args, **kwargs):
        # 'data' is the standard argument for PluginInterface.execute
        api_key = kwargs.get('api_key')
        model = kwargs.get('model')
        
        if isinstance(data, dict) and 'input_text' in data:
            input_text = data['input_text']
            # Also check for api_key in the data dict if not in kwargs
            if not api_key and 'api_key' in data:
                api_key = data['api_key']
            # Also check for model in the data dict if not in kwargs
            if not model and 'model' in data:
                model = data['model']
        else:
            input_text = data
        
        result = await self.run(input_text, api_key=api_key, model=model)
        
        # Handle the result: either a string response or a dictionary with 'output' key
        if isinstance(result, dict) and 'output' in result:
            # This is already formatted correctly
            return result
        elif result:
            # This is a string result from the API
            return {"output": result}
        else:
            # Fallback for None or empty string
            return {"output": "I need a valid OpenAI API key to provide responses. Please update your OPENAI_API_KEY in the .env file with a valid API key from https://platform.openai.com/account/api-keys."}

    async def initialize(self):
        logger.info(f"OpenAI fallback plugin initialized with models: {DEFAULT_MODEL} (primary) and {FALLBACK_MODEL} (fallback)")

    async def shutdown(self):
        pass

# Create an instance of the plugin to be imported elsewhere - name must be 'tool'
tool = OpenAIFallback()
