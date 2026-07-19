#!/usr/bin/env bash
# Builds the React frontend for production.
set -euo pipefail
cd "$(dirname "$0")/../../client"
npm ci
npm run build
echo "Frontend build complete. Output in client/dist/"
