# app/codex_prompt_engine/engine.py

from app.codex_prompt_engine.prompt_templates import BASE_SYSTEM_PROMPT

class CodexPromptEngine:
    def __init__(self, system_prompt: str = BASE_SYSTEM_PROMPT):
        self.system_prompt = system_prompt

    def build_prompt(self, history: list[dict], user_input: str) -> list[dict]:
        """
        Combine system prompt, chat history, and new input into a prompt for the LLM.
        """
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_input})
        return messages
