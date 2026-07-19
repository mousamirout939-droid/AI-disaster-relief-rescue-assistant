# Deploying the Frontend to Vercel

1. In the Vercel dashboard, **Add New Project** and import this repo.
2. Set the root directory to `client/`.
3. Framework preset: **Vite**.
4. Add an environment variable `VITE_API_BASE_URL` pointing at your deployed backend, e.g.
   `https://disaster-relief-api.onrender.com/api`.
5. Deploy. `vercel.json` in `deployment/vercel/` handles the SPA rewrite rule for React Router.
