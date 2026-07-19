#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../server"
python scripts/clean_database.py
