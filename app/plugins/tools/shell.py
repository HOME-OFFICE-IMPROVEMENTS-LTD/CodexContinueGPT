# app/plugins/tools/shell.py

import subprocess
from app.plugins.base import Tool

class ShellTool(Tool):
    name = "shell"
    description = "Run a shell command"

    async def run(self, input_text: str) -> str:
        try:
            result = subprocess.run(input_text, shell=True, capture_output=True, text=True)
            return result.stdout.strip() or result.stderr.strip()
        except Exception as e:
            return str(e)

tool = ShellTool()
