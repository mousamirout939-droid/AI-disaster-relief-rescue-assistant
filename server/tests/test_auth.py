"""Tests for registration, login, and the /auth/me endpoint."""
import pytest

pytestmark = pytest.mark.asyncio


async def test_register_and_login(client):
    register_payload = {
        "name": "Test User",
        "email": "test.user@example.com",
        "password": "Password123",
        "phone": "+911234567890",
    }
    resp = await client.post("/api/auth/register", json=register_payload)
    assert resp.status_code == 201
    body = resp.json()
    assert body["success"] is True
    assert "access_token" in body["data"]

    login_resp = await client.post(
        "/api/auth/login", json={"email": register_payload["email"], "password": register_payload["password"]}
    )
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()["data"]


async def test_register_duplicate_email_rejected(client):
    payload = {"name": "Dup User", "email": "dup@example.com", "password": "Password123"}
    first = await client.post("/api/auth/register", json=payload)
    assert first.status_code == 201

    second = await client.post("/api/auth/register", json=payload)
    assert second.status_code == 400


async def test_login_wrong_password_rejected(client):
    payload = {"name": "Wrong Pass", "email": "wrongpass@example.com", "password": "Password123"}
    await client.post("/api/auth/register", json=payload)

    resp = await client.post("/api/auth/login", json={"email": payload["email"], "password": "WrongPass1"})
    assert resp.status_code == 401


async def test_me_requires_token(client):
    resp = await client.get("/api/auth/me")
    assert resp.status_code == 401


async def test_me_with_valid_token(client):
    payload = {"name": "Me User", "email": "me@example.com", "password": "Password123"}
    reg = await client.post("/api/auth/register", json=payload)
    token = reg.json()["data"]["access_token"]

    resp = await client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["data"]["email"] == payload["email"]
