# app/tools/hello_tool.py

from app.tools.tool import Tool

class HelloTool(Tool):
    name = "hello"
    description = "Returns a friendly hello message."

    def run(self, input: dict) -> str:
        name = input.get("name", "World")
        return f"👋 Hello, {name}!"
