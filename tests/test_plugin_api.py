# tests/test_plugin_api.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_plugins():
    response = client.get("/plugins")
    assert response.status_code == 200
    assert "plugins" in response.json()

def test_execute_shell_plugin():
    response = client.post("/plugins/execute", json={
        "plugin": "shell",
        "data": "echo plugin_api_test"
    })
    assert response.status_code == 200
    result = response.json().get("result", {})
    assert "output" in result
    assert "plugin_api_test" in result["output"]
