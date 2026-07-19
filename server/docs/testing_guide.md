# Testing Guide

```bash
cd server
pip install -r requirements.txt   # includes mongomock-motor, pytest, pillow
python -m pytest tests/ -q
```

Tests use `mongomock-motor` to fake MongoDB in-process (see `tests/conftest.py`), so
no real database connection is required. Each test gets a fresh, isolated fake
database via the `fake_db` fixture.

## Test files
- `test_auth.py` — registration, login, RBAC on `/auth/me`
- `test_disaster.py` — shelter/hospital CRUD, nearby geo search, admin-only writes
- `test_routes.py` — safe-route endpoint, alerts
- `test_ai.py` — YOLO mock-detector fallback, Gemini chat fallback
- `test_database.py` — connection manager behaviour
- `test_api.py` — health checks, response envelope shape

## Writing new tests
Use the `client` fixture (an `httpx.AsyncClient` wired to the app with a fake DB) and
`fake_db` fixture directly when you need to seed data or bypass an endpoint that isn't
implemented for the flow you're testing (see `test_disaster.py`'s `_register_admin`
helper for an example).
