# tests/test_plugin_runner.py

from app.plugins.plugin_runner import run_plugin

def test_run_plugin_shell():
    result = run_plugin("shell", "echo hello")
    assert isinstance(result, dict)
    assert "output" in result
    assert "hello" in result["output"]

def test_run_plugin_agent():
    result = run_plugin("agent_plugin", "test input")
    assert isinstance(result, dict)
    assert result["agent_response"].startswith("🧠")
