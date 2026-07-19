#!/usr/bin/env bash
# Deploys the frontend to Vercel using the Vercel CLI.
set -euo pipefail
cd "$(dirname "$0")/../../client"
npx vercel --prod
