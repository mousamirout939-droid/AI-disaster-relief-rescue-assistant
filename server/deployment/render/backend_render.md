# Deploying the Backend to Render

1. Push this repo to GitHub.
2. In the Render dashboard, choose **New > Web Service** and connect the repo.
3. Set the root directory to `server/`.
4. Render will detect `dockerfile` automatically (or use the provided `render.yaml` blueprint).
5. Add environment variables from `server/.env.example` under **Environment**.
6. Set the health check path to `/health`.
7. Deploy. Render will build the Docker image and expose the service at `https://<service-name>.onrender.com`.
