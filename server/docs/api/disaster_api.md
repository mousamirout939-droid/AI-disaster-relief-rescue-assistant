# Disaster & Reports API

## `GET /api/disasters?status=active`
List classified disaster events.

## `GET /api/disasters/nearby?lat=..&lng=..&radius_km=10`

## `POST /api/reports` (multipart/form-data, auth required)
Fields: `disaster_type`, `description`, `lat`, `lng`, `address` (optional), `image`
(optional file). If an image is included, it's analyzed with YOLO and the response
includes `ai_detections`, `ai_severity`, `ai_confidence`.

## `GET /api/reports/mine` (auth required)

## `PATCH /api/reports/{report_id}/status` (admin only)
```json
{ "status": "verified" }
```
