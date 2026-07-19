# 🛟 AI Disaster Relief & Rescue Assistant

An AI-powered platform for disaster reporting, rescue coordination, and emergency response — built with
FastAPI + MongoDB on the backend and React 19 + Redux Toolkit on the frontend.

## Features

- 🔐 JWT authentication with role-based access (user / volunteer / rescue team / admin)
- 📸 Disaster reporting with photo upload + YOLOv8 detection and AI severity scoring
- 🏠 Nearby shelter & 🏥 hospital finder (geo-radius search)
- 🚑 Rescue team locator and dispatch
- 🗺️ Hazard-aware safe route planning (Google Maps + active-report avoidance)
- 🤖 Gemini-powered emergency chatbot
- 🌐 Multi-language emergency instructions
- ⛈️ Weather alerts, 🔔 in-app notifications, 🆘 one-tap SOS
- 📊 Admin analytics dashboard, 🙋 volunteer registration, 👤 profile management
- 🌓 Dark/light mode, fully responsive UI, offline-ready PWA shell

## Project Structure── server/     FastAPI backend (see server/README or docs/)
│   ├── api/            REST route handlers
│   ├── controllers/    Business logic
│   ├── services/       External integrations (YOLO, Gemini, Maps, Weather, Email…)
│   ├── models/          Mongo document models
│   ├── schemas/        Request/response validation
│   ├── ml/              Pathfinding & risk/severity ML utilities
│   ├── ai_model/        YOLO training/inference pipeline
│   ├── tests/           Pytest suite (17 tests, in-memory Mongo)
│   ├── scripts/         Ops scripts (seed, backup, admin creation, training…)
│   └── docs/            API reference, guides, architecture notes
└── client/     React 19 + Vite + Redux Toolkit + Tailwind frontend
└── src/
├── api/          Axios client + endpoint wrappers
├── store/        Redux Toolkit slices
├── components/   Reusable UI components + all pages
└── hooks/        useAuth, useGeolocation, useDarkMode## Quick Start

```bash
# 1. Backend
cd server
pip install -r requirements.txt
cp .env.example .env             # then fill in MONGODB_URI, JWT_SECRET_KEY, etc.
python scripts/seed_database.py    # optional: demo shelters/hospitals/users
python run.py                      # http://localhost:8000  (docs at /docs)

# 2. Frontend (separate terminal)
cd client
npm install
cp .env.example .env             # set VITE_API_BASE_URL if not localhost:8000
npm run dev                      # http://localhost:5173
Or from the repo root, once both are installed: npm run dev:server and npm run dev:client.

Configuration Notes
MongoDB: point MONGODB_URI at a local instance or MongoDB Atlas. Indexes (including 2dsphere geo
indexes) are created automatically on startup.

AI detection: the YOLO service looks for a trained model at server/weights/best.pt. Without one,
it automatically falls back to a lightweight heuristic detector so the reporting flow still works —
see server/ai_model/train.py to train your own on a labeled dataset.

Gemini chatbot: set GEMINI_API_KEY to enable live responses; otherwise the chatbot returns
built-in safety guidance.

Google Maps: set GOOGLE_MAPS_API_KEY (backend) and VITE_GOOGLE_MAPS_API_KEY (frontend) for live
directions and map rendering; the UI degrades to a plain location list without it.

Testing
Bash
cd server && pytest       # 17 tests covering auth, RBAC, geo search, AI fallback, routing
cd client && npm run lint  # 0 errors
cd client && npm run build # production build check
Documentation
See server/docs/README.md for the full documentation index (API reference,
installation guide, deployment guide, developer guide, troubleshooting).

License
MIT — see LICENSE.