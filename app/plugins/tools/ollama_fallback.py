import httpx
from app.brain.core.base import CodexTool

class OllamaFallback(CodexTool):
    name = "ollama_fallback"
    description = "Fallback to local Ollama model when no plugin matches"

    def initialize(self):
        print("OllamaFallback plugin initialized")

    def execute(self, input_text: str) -> dict:
        try:
            response = httpx.post(
                "http://172.17.0.1:11434/api/generate",  # Docker host IP
                json={
                    "model": "llama3",
                    "prompt": input_text,
                    "stream": False
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            return {"output": data.get("response", "").strip()}
        except Exception as e:
            return {"error": f"Ollama call failed: {str(e)}"}

    def run(self, input_text: str) -> dict:
        return self.execute(input_text)

    def shutdown(self):
        print("OllamaFallback plugin shutdown")

tool = OllamaFallback()
