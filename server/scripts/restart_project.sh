#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
./stop_project.sh || true
./start_project.sh
