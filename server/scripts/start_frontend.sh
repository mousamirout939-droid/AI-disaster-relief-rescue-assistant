#!/usr/bin/env bash
# Starts the Vite dev server for the React frontend.
set -euo pipefail
cd "$(dirname "$0")/../../client"
npm run dev
