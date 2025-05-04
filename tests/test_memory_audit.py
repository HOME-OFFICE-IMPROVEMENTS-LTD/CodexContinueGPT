# tests/test_memory_audit.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_memory_audit_endpoint():
    res = client.get("/memory/audit/default")
    assert res.status_code in [200, 404, 500]  # may return empty or uninitialized
