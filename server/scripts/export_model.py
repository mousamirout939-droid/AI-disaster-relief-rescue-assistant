#!/usr/bin/env python3
"""Exports a trained .pt model to ONNX for lighter-weight / cross-platform deployment."""
import argparse
from pathlib import Path


def export(weights_path: str, fmt: str = "onnx") -> None:
    from ultralytics import YOLO

    model = YOLO(weights_path)
    exported_path = model.export(format=fmt)
    print(f"Exported model to {exported_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", default="weights/best.pt")
    parser.add_argument("--format", default="onnx")
    args = parser.parse_args()
    export(args.weights, args.format)
