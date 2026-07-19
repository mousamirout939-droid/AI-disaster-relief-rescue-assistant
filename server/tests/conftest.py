"""
Shared pytest fixtures.

Uses mongomock-motor to fake MongoDB in-process, so the full test suite runs
without a real MongoDB Atlas connection. Overrides `get_db` on the FastAPI
app so every route under test talks to the fake database.
"""
import asyncio
import sys
from pathlib import Path

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from mongomock_motor import AsyncMongoMockClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import app  # noqa: E402
from database.connection import get_db  # noqa: E402


@pytest_asyncio.fixture
async def fake_db():
    client = AsyncMongoMockClient()
    db = client["disaster_relief_test"]
    yield db


@pytest_asyncio.fixture
async def client(fake_db):
    async def _get_db_override():
        return fake_db

    app.dependency_overrides[get_db] = _get_db_override
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
