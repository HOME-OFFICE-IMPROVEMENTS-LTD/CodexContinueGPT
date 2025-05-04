# tests/test_plugin_registry.py

from app.plugins.registry import PluginRegistry
from app.brain.core.base import CodexTool

class DummyTool(CodexTool):
    def run(self, input_data):
        return "dummy"

def test_plugin_registry_register_and_retrieve():
    registry = PluginRegistry()
    dummy_tool = DummyTool()
    registry.register("dummy", dummy_tool)
    retrieved = registry.get("dummy")
    assert retrieved is dummy_tool