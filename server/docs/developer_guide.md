# Developer Guide

## Request lifecycle
`api/*.py` (FastAPI router) → `controllers/*.py` (business logic) → `services/*.py`
(external integrations) / direct Motor queries → `schemas/*.py` validate in/out.

## Adding a new resource
1. Add a Pydantic document model in `models/`.
2. Add request/response schemas in `schemas/`.
3. Add business logic functions in `controllers/`.
4. Add a router in `api/`, wire it into `app/main.py`'s router list.
5. Add an index for it in `database/indexes.py` if it needs geo/unique lookups.
6. Add tests in `tests/`.

## Auth model
JWT access + refresh tokens (`config/jwt_handler.py`). `middleware/auth.py` exposes
`get_current_user` and `require_roles(*roles)` as FastAPI dependencies. Roles:
`user`, `volunteer`, `rescue_team`, `admin` (admins live in a separate `admins`
collection from regular `users`).

## AI pipeline
`services/yolo_service.py` wraps Ultralytics; `services/ai_service.py` turns raw
detections into a severity level. `services/gemini_service.py` is the chatbot.
Everything degrades gracefully without API keys/trained weights — see the main
`README.md`'s "AI features" section.

## Code style
Standard library + FastAPI/Pydantic idioms, async throughout, one responsibility per
module. Run `python -m pytest tests/ -q` before committing.
