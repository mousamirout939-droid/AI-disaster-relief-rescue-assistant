#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../server"
python scripts/backup_database.py
