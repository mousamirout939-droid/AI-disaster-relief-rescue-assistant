#!/usr/bin/env bash
# Installs backend Python dependencies into the current environment.
set -euo pipefail
cd "$(dirname "$0")/.."
pip install -r requirements.txt
echo "Backend dependencies installed."
