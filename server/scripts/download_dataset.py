#!/usr/bin/env python3
"""
Placeholder downloader for a disaster-imagery dataset (e.g. from Roboflow or Kaggle).

No dataset is bundled with this project — plug in your own source and API key.
Populate DATASET_URL and an API key via environment variable before running.
"""
import os
import sys
import zipfile
from pathlib import Path

import httpx

DATASET_URL = os.getenv("DATASET_DOWNLOAD_URL", "")
DEST_DIR = Path(__file__).resolve().parent.parent / "datasets"


def main() -> None:
    if not DATASET_URL:
        print(
            "No DATASET_DOWNLOAD_URL configured. Set it to a direct .zip download link "
            "(e.g. a Roboflow export URL) and re-run this script.\n"
            "Example: DATASET_DOWNLOAD_URL=https://... python scripts/download_dataset.py"
        )
        sys.exit(1)

    DEST_DIR.mkdir(exist_ok=True)
    zip_path = DEST_DIR / "dataset.zip"

    print(f"Downloading dataset from {DATASET_URL} ...")
    with httpx.stream("GET", DATASET_URL, timeout=120, follow_redirects=True) as response:
        response.raise_for_status()
        with open(zip_path, "wb") as f:
            for chunk in response.iter_bytes():
                f.write(chunk)

    print("Extracting...")
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(DEST_DIR)

    print(f"Dataset ready at {DEST_DIR}")


if __name__ == "__main__":
    main()
