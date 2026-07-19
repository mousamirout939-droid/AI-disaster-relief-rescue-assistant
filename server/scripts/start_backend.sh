#!/usr/bin/env bash
# Starts the FastAPI backend with uvicorn (dev mode with auto-reload).
set -euo pipefail
cd "$(dirname "$0")/.."
uvicorn app.main:app --reload --host 0.0.0.0 --port "${PORT:-8000}"
