# tests/test_tools_api.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_tools():
    res = client.get("/tools")
    assert res.status_code == 200
    tools = res.json().get("tools", [])
    assert isinstance(tools, list)
    assert any("shell" in tool["name"].lower() for tool in tools)
