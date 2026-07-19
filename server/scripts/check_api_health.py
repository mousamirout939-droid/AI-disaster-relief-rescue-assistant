#!/usr/bin/env python3
"""Hits the running API's /health endpoint. Usage: python scripts/check_api_health.py [base_url]"""
import sys

import httpx

DEFAULT_URL = "http://localhost:8000"


def main() -> None:
    base_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    try:
        resp = httpx.get(f"{base_url}/health", timeout=5)
        resp.raise_for_status()
        print(f"API healthy at {base_url}: {resp.json()}")
    except Exception as exc:  # noqa: BLE001
        print(f"API health check FAILED for {base_url}: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
