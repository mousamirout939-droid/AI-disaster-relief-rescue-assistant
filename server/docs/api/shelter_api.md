# Shelter API

- `POST /api/shelters` (admin) — create
- `GET /api/shelters` — list all
- `GET /api/shelters/nearby?lat=..&lng=..&radius_km=15` — nearest open shelters, sorted by distance
- `PATCH /api/shelters/{id}/occupancy` (admin) — update current occupancy
