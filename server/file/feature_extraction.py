"""Extracts simple color/texture summary features from an image, used by
the lightweight (non-YOLO) heuristics as extra signal alongside detections."""
import numpy as np

from utils.image_processing import load_image, to_grayscale


def extract_color_histogram(image_path: str, bins: int = 8) -> list[float]:
    image = load_image(image_path)
    hist = []
    for channel in range(3):
        channel_hist, _ = np.histogram(image[:, :, channel], bins=bins, range=(0, 255))
        hist.extend((channel_hist / channel_hist.sum()).tolist())
    return hist


def extract_edge_density(image_path: str) -> float:
    import cv2
    image = load_image(image_path)
    gray = to_grayscale(image)
    edges = cv2.Canny(gray, 100, 200)
    return float(np.count_nonzero(edges) / edges.size)
