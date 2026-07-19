# AI Disaster Relief & Rescue Assistant — Backend

FastAPI backend for the AI Disaster Relief & Rescue Assistant: authentication, disaster
reporting with AI-powered image analysis (YOLOv8), shelter/hospital/rescue-team
directories with geo lookup, safe-route computation, an emergency chatbot (Gemini),
weather alerts, notifications, and an admin dashboard.

## Quick start

```bash
cd server
python -m venv .venv && source .venv/bin/activate   # or your preferred env tool
pip install -r requirements.txt
cp .env.example .env   # then fill in MONGODB_URI and any API keys you have
python scripts/create_demo_users.py   # optional: seeds demo accounts
uvicorn app.main:app --reload
```

Interactive API docs: http://localhost:8000/docs

## Project layout

```
server/
  app/            FastAPI app entrypoint (main.py)
  api/            Route definitions (one file per resource)
  controllers/    Request-level business logic
  services/       Integrations: YOLO, Gemini, Maps, Weather, Email, Notifications...
  models/         MongoDB document models (Pydantic)
  schemas/        Request/response validation schemas
  middleware/     Auth (JWT + RBAC), CORS, logging, rate limiting, error handling
  database/       MongoDB connection, indexes, seed data
  ml/             Standalone algorithms: pathfinding, severity/risk models, recommendations
  ai_model/       YOLOv8 training/inference pipeline
  utils/          Shared helpers (geo, file upload, image processing, validators)
  tests/          pytest suite (uses an in-memory Mongo fake, no real DB needed)
  scripts/        CLI ops tooling (seed, backup, health checks, AI training helpers)
  deployment/     Docker, Kubernetes, Render, Vercel, nginx, CI/CD configs
```

`databases/` and `file/` are legacy-compatibility folders kept from the original
project skeleton; they re-export the real implementations in `database/` and
`services/`/`ai_model/` respectively — build against those instead.

## Running tests

```bash
python -m pytest tests/ -q
```

## AI features and what's real vs. mocked

- **YOLO detection** (`services/yolo_service.py`) runs real Ultralytics inference if
  `weights/best.pt` exists; otherwise it falls back to a simple color-heuristic mock so
  the reporting flow still works end-to-end. Train a real model with
  `python scripts/train_ai_model.py` once you've populated `datasets/` — see
  `datasets/README.md`.
- **Gemini chatbot** (`services/gemini_service.py`) calls the real Gemini API if
  `GEMINI_API_KEY` is set; otherwise it returns static safety guidance.
- **Severity/risk/route ML models** (`ml/`) ship with trainable scikit-learn pipelines
  (`ml/training/`) and heuristic fallbacks so they work immediately without training.

See `docs/` for full API reference, installation, and deployment guides.
