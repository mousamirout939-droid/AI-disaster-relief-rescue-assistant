#!/usr/bin/env bash
# Used as a Docker HEALTHCHECK for the backend container.
curl -f http://localhost:8000/health || exit 1
