#!/usr/bin/env bash
# Kills any process bound to the backend (8000) or frontend (5173) dev ports.
set -euo pipefail
for port in 8000 5173; do
  pid=$(lsof -ti tcp:"$port" || true)
  if [ -n "$pid" ]; then
    kill "$pid"
    echo "Stopped process on port $port (PID $pid)"
  else
    echo "No process running on port $port"
  fi
done
