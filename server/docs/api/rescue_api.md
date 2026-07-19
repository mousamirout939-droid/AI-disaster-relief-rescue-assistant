# Rescue Team API

- `POST /api/rescue-teams` (admin) — create
- `GET /api/rescue-teams` — list all
- `GET /api/rescue-teams/nearby?lat=..&lng=..&radius_km=25` — nearest *available* teams
- `POST /api/rescue-teams/{id}/dispatch` (admin) — `{ "report_id": "..." }`, marks the team dispatched
