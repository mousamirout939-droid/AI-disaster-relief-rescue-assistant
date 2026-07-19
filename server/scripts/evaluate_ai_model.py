#!/usr/bin/env python3
"""CLI wrapper: python scripts/evaluate_ai_model.py --weights weights/best.pt"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ai_model.evaluate import evaluate  # noqa: E402

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", default="weights/best.pt")
    args = parser.parse_args()
    print(evaluate(args.weights))
