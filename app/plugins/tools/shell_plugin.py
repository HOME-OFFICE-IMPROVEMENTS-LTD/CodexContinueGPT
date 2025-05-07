# app/plugins/tools/shell_plugin.py

from app.brain.core.base import CodexTool
import subprocess
from datetime import datetime

class ShellPlugin(CodexTool):
    name = "shell"
    description = "Run a shell command"
    author = "CodexContinueGPT"
    version = "1.0"
    updated_at = "2025-05-04T19:50:23.388715"
    category = "Utility"
    requirements = []
    parameters = {}
    example = "run shell echo hello"

    def initialize(self):
        print("ShellPlugin initialized")

    def run(self, input_text: str, session_id: str) -> str:
        try:
            result = subprocess.check_output(input_text, shell=True, stderr=subprocess.STDOUT)
            return result.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"⚠️ Shell error: {e.output.decode('utf-8')}"
        
plugin = ShellPlugin()
