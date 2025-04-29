# test_plugin_runner.py

import asyncio
from app.plugins.manager import load_plugins, TOOL_REGISTRY

async def main():
    load_plugins()
    tool = TOOL_REGISTRY.get("memory")
    if not tool:
        print("❌ Tool not found.")
        return
    result = await tool.run("default")
    print("✅ Tool output:\n", result)

if __name__ == "__main__":
    asyncio.run(main())
