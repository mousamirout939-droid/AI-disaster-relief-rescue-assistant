#!/usr/bin/env bash
# Sanity-builds the backend: installs deps and compiles every .py file.
set -euo pipefail
cd "$(dirname "$0")/.."
pip install -r requirements.txt
python -m compileall -q .
echo "Backend build check passed."
