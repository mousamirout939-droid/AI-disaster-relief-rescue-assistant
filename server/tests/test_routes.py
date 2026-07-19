"""Tests for the safe-route endpoint (degrades gracefully with no Maps API key)."""
import pytest

pytestmark = pytest.mark.asyncio


async def test_safe_route_without_api_key(client):
    resp = await client.get("/api/routes/safe", params={"origin": "12.9,77.5", "destination": "12.95,77.6"})
    assert resp.status_code == 200
    body = resp.json()["data"]
    assert body["directions"]["available"] is False
    assert "active_hazards_considered" in body


async def test_alerts_crud_requires_admin(client):
    listing = await client.get("/api/alerts")
    assert listing.status_code == 200
    assert listing.json()["data"] == []

    resp = await client.post("/api/alerts", json={"title": "Flood Warning", "message": "Heavy rain expected", "severity": "high"})
    assert resp.status_code == 401
