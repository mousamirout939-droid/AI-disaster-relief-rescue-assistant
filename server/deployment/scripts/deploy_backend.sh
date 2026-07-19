#!/usr/bin/env bash
# Triggers a Render deploy via its deploy hook URL (set RENDER_DEPLOY_HOOK_URL).
set -euo pipefail
if [ -z "${RENDER_DEPLOY_HOOK_URL:-}" ]; then
  echo "Set RENDER_DEPLOY_HOOK_URL to your Render deploy hook and re-run."
  exit 1
fi
curl -X POST "$RENDER_DEPLOY_HOOK_URL"
echo "Backend deploy triggered."
