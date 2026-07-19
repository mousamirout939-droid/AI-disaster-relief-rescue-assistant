# Deployment Guide

## Recommended setup
- **Backend** → Render (Docker web service)
- **Frontend** → Vercel (static Vite build)
- **Database** → MongoDB Atlas (free/shared tier is enough for a demo)

## 1. MongoDB Atlas
1. Create a free cluster at https://cloud.mongodb.com.
2. Create a database user and allow network access from `0.0.0.0/0` (or Render's IPs).
3. Copy the connection string into `MONGODB_URI`.

## 2. Backend (Render)
See `render/backend_render.md` and `render/environment.md`.

## 3. Frontend (Vercel)
See `vercel/frontend_vercel.md`.

## 4. Local Docker (alternative to the above)
```bash
docker compose -f deployment/docker/docker-compose.yml up --build
```
This runs backend (`:8000`), frontend (`:3000`), and MongoDB (`:27017`) together.

## 5. CI/CD
GitHub Actions workflows in `github_actions/` run backend tests and build the frontend on every
push, and `deploy.yml` triggers Render + Vercel deploys on pushes to `main` (requires the
`RENDER_SERVICE_ID`, `RENDER_DEPLOY_KEY`, `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`
repo secrets).

## 6. Post-deploy checklist
- [ ] `GET /health` on the backend returns `200`
- [ ] `CORS_ORIGINS` includes the deployed frontend URL
- [ ] Admin account created (`python scripts/create_admin.py --email ... --password ...`)
- [ ] YOLO weights uploaded to `weights/best.pt` if you have a trained model (optional — the
      app falls back to a mock detector otherwise)
