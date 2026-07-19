# Troubleshooting

**"Database not initialized" error** — the FastAPI `lifespan` startup event didn't run
(e.g. you imported `app.main` without going through uvicorn/TestClient's lifespan). Make
sure you're running via `uvicorn app.main:app` or a test client that triggers lifespan.

**MongoDB connection fails on startup** — the app still starts (it logs a warning rather
than crashing) so you can fix `MONGODB_URI` without redeploying. Run
`python scripts/check_database.py` to debug.

**AI detection always returns the same class** — you're on the mock detector (no
`weights/best.pt`). Run `python scripts/check_ai_model.py` to confirm, and see
`datasets/README.md` to train a real model.

**Chatbot returns a canned response** — `GEMINI_API_KEY` isn't set in `.env`.

**CORS errors from the frontend** — add the frontend's origin to `CORS_ORIGINS` in `.env`.

**bcrypt/passlib version errors** — this project calls the `bcrypt` package directly
(see `config/security.py`) specifically to avoid a known passlib+bcrypt version-detection
bug; make sure you're not shadowing it with an older `passlib[bcrypt]` install.
