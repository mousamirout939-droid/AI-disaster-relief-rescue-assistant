# Health Checks

- **Backend**: `GET /health` returns `{"status": "healthy"}`. Used by Docker `HEALTHCHECK`,
  Render, and the Kubernetes readiness/liveness probes.
- **Database**: `python scripts/check_database.py` pings MongoDB and prints per-collection counts.
- **AI model**: `python scripts/check_ai_model.py` reports whether real YOLO weights are loaded
  or the app is falling back to the mock detector.
