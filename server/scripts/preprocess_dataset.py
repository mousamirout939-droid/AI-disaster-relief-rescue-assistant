#!/usr/bin/env python3
"""CLI wrapper: python scripts/preprocess_dataset.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ai_model.preprocess import preprocess_all  # noqa: E402

if __name__ == "__main__":
    n = preprocess_all()
    print(f"Preprocessed {n} images.")
