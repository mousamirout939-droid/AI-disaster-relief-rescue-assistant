# Deployment

This folder holds deployment configuration for every target this project supports:

| Path | Purpose |
|---|---|
| `docker/` | Dockerfiles + compose file for running backend, frontend, and MongoDB together |
| `kubernetes/` | Deployment/Service/Ingress/ConfigMap manifests for a K8s cluster |
| `render/` | Render.com blueprint + notes for the backend |
| `vercel/` | Vercel config + notes for the frontend |
| `nginx/` | Reverse-proxy config used by the frontend Docker image / self-hosted setups |
| `github_actions/` | CI (test/build) and CD (deploy) workflows |
| `monitoring/` | Health-check and logging notes |
| `scripts/` | One-off deploy/backup/restore helper scripts |

See `deployment_guide.md` for the full step-by-step walkthrough.
