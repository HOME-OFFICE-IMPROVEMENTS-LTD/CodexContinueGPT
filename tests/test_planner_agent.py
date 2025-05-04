# tests/test_planner_agent.py

import pytest
from app.brain.planner_agent import PlannerAgent

@pytest.fixture
def planner():
    return PlannerAgent()

def test_run_shell_plugin(planner):
    result = planner.route("run shell echo hello", "default")
    assert isinstance(result, str)
    assert "hello" in result.lower()

def test_fallback_to_llm(planner):
    result = planner.route("Tell me a joke", "default")
    assert isinstance(result, str)
    assert result.startswith("🧠") or "joke" in result.lower()
