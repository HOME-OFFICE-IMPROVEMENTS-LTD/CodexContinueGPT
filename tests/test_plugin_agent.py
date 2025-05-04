# tests/test_plugin_agent.py

from app.brain.agent.plugin_agent import PluginAgent

def test_plugin_agent_shell():
    agent = PluginAgent()
    result = agent.maybe_execute("/run shell echo from_agent")
    assert "output" in result
    assert "from_agent" in result["output"]

def test_plugin_agent_fail():
    agent = PluginAgent()
    result = agent.maybe_execute("/run not_a_real_plugin test")
    assert "error" in result
