"""Tests for shelters/hospitals/rescue-teams CRUD + nearby geo queries."""
import pytest

pytestmark = pytest.mark.asyncio


async def _register_admin(client, fake_db):
    """Registers via the normal endpoint then promotes the user to admin in the fake DB
    (there's no public admin-signup endpoint by design)."""
    from bson import ObjectId
    from config.security import hash_password
    from utils.helpers import now_ts

    result = await fake_db["admins"].insert_one({
        "name": "Admin", "email": "admin@test.com", "password": hash_password("Admin123!"),
        "role": "admin", "is_active": True, "created_at": now_ts(),
    })
    login = await client.post("/api/auth/login", json={"email": "admin@test.com", "password": "Admin123!"})
    assert login.status_code == 200
    return login.json()["data"]["access_token"]


async def test_create_and_list_shelter(client, fake_db):
    token = await _register_admin(client, fake_db)
    headers = {"Authorization": f"Bearer {token}"}

    create = await client.post(
        "/api/shelters",
        json={"name": "Test Shelter", "lat": 12.97, "lng": 77.59, "capacity": 100},
        headers=headers,
    )
    assert create.status_code == 201

    listing = await client.get("/api/shelters")
    assert listing.status_code == 200
    assert len(listing.json()["data"]) == 1
    assert listing.json()["data"][0]["name"] == "Test Shelter"


async def test_nearby_hospitals(client, fake_db, monkeypatch):
    # mongomock doesn't implement the `$nearSphere` geo operator used against real
    # MongoDB, so for this in-memory test we swap it for a filter that matches
    # everything and let the haversine distance_km calculation do the real work.
    import controllers.hospital_controller as hospital_controller
    monkeypatch.setattr(hospital_controller, "near_query", lambda lng, lat, radius_km: {})

    token = await _register_admin(client, fake_db)
    headers = {"Authorization": f"Bearer {token}"}

    await client.post(
        "/api/hospitals",
        json={"name": "Near Hospital", "lat": 12.97, "lng": 77.59, "beds_available": 5},
        headers=headers,
    )

    nearby = await client.get("/api/hospitals/nearby", params={"lat": 12.97, "lng": 77.59, "radius_km": 5})
    assert nearby.status_code == 200
    data = nearby.json()["data"]
    assert len(data) == 1
    assert "distance_km" in data[0]


async def test_shelter_requires_admin(client):
    resp = await client.post("/api/shelters", json={"name": "X", "lat": 1, "lng": 1})
    assert resp.status_code == 401  # no token at all
