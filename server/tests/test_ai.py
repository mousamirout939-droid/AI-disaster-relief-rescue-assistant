"""Tests for the AI endpoints (YOLO mock-fallback detection + Gemini chat fallback)."""
import io

import pytest
from PIL import Image

pytestmark = pytest.mark.asyncio


def _sample_jpeg_bytes() -> bytes:
    img = Image.new("RGB", (64, 64), color=(180, 30, 20))  # reddish -> mock "fire" heuristic
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


async def test_detect_endpoint_returns_detection(client):
    files = {"image": ("test.jpg", _sample_jpeg_bytes(), "image/jpeg")}
    resp = await client.post("/api/ai/detect", files=files)
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert "detections" in data
    assert "severity" in data
    assert data["severity"] in ("low", "moderate", "high", "critical")


async def test_chat_endpoint_falls_back_without_api_key(client):
    resp = await client.post("/api/ai/chat", json={"message": "There is a fire near my building, what do I do?"})
    assert resp.status_code == 200
    reply = resp.json()["data"]["reply"]
    assert isinstance(reply, str) and len(reply) > 0
