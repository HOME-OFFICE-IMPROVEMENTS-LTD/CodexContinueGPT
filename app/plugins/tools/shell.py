# app/plugins/tools/shell.py

import subprocess
from app.brain.core.base import CodexTool  # Corrected import

class ShellPlugin(CodexTool):
    name = "shell"
    description = "Run a shell command"

    def initialize(self):
        print("Shell plugin initialized")

    def execute(self, input_text: str) -> dict:
        try:
            result = subprocess.run(input_text, shell=True, capture_output=True, text=True)
            return {"output": result.stdout.strip() or result.stderr.strip()}
        except Exception as e:
            return {"error": str(e)}

    def run(self, input_text: str) -> dict:
        # Required to satisfy abstract base class
        return self.execute(input_text)

    def shutdown(self):
        print("Shell plugin shutdown")

tool = ShellPlugin()
