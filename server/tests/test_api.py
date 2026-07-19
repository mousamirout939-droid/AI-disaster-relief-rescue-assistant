"""Smoke tests for health endpoints and the response envelope shape."""
import pytest

pytestmark = pytest.mark.asyncio


async def test_root(client):
    resp = await client.get("/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "running"


async def test_health(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "healthy"}


async def test_shelters_list_envelope(client):
    resp = await client.get("/api/shelters")
    assert resp.status_code == 200
    body = resp.json()
    assert set(["success", "message", "data"]).issubset(body.keys())
    assert body["success"] is True
    assert body["data"] == []
