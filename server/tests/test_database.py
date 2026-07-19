"""Tests for the MongoDB connection manager helper (mongodb.py)."""
import pytest

from database.mongodb import MongoManager, get_database


def test_get_database_raises_before_connect():
    mgr = MongoManager()
    mgr.db = None
    with pytest.raises(RuntimeError):
        get_database()


@pytest.mark.asyncio
async def test_fake_db_fixture_is_usable(fake_db):
    await fake_db["ping_collection"].insert_one({"ok": 1})
    doc = await fake_db["ping_collection"].find_one({"ok": 1})
    assert doc["ok"] == 1
