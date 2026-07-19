#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../server"
python scripts/restore_database.py "$1"
