#!/usr/bin/env bash
# Starts backend and frontend together (backend in background, frontend in foreground).
set -euo pipefail
cd "$(dirname "$0")"
./start_backend.sh &
BACKEND_PID=$!
echo "Backend started (PID $BACKEND_PID)"
trap "kill $BACKEND_PID" EXIT
./start_frontend.sh
