# Installation Guide

## Prerequisites
- Python 3.11+
- Node.js 20+ (for the frontend)
- A MongoDB instance (local `mongod`, Docker, or MongoDB Atlas)

## Backend
```bash
cd server
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env: set MONGODB_URI at minimum
uvicorn app.main:app --reload
```
Visit http://localhost:8000/docs for the interactive API explorer.

## Frontend
```bash
cd client
npm install
cp .env.example .env   # set VITE_API_BASE_URL=http://localhost:8000/api
npm run dev
```
Visit http://localhost:5173.

## Seeding demo data
```bash
cd server
python scripts/create_demo_users.py
python scripts/seed_database.py
```

## Running with Docker instead
```bash
docker compose up --build   # backend + MongoDB only, from server/
# or, for the full stack:
docker compose -f deployment/docker/docker-compose.yml up --build
```
