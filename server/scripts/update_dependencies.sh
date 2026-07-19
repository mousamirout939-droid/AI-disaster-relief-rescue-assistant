#!/usr/bin/env bash
# Upgrades backend and frontend dependencies to their latest compatible versions.
set -euo pipefail
cd "$(dirname "$0")/.."
pip install --upgrade -r requirements.txt
cd ../client
npm update
echo "Dependencies updated. Review changes before committing."
