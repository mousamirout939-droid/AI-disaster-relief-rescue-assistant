"""Simple augmentation pipeline (flip, brightness, rotation) to expand a small training set."""
from pathlib import Path

import cv2
import numpy as np


def flip_horizontal(image: np.ndarray) -> np.ndarray:
    return cv2.flip(image, 1)


def adjust_brightness(image: np.ndarray, factor: float = 1.2) -> np.ndarray:
    return cv2.convertScaleAbs(image, alpha=factor, beta=0)


def rotate(image: np.ndarray, angle: float = 10) -> np.ndarray:
    h, w = image.shape[:2]
    matrix = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    return cv2.warpAffine(image, matrix, (w, h))


def augment_directory(src_dir: Path, dst_dir: Path) -> int:
    """Writes flipped/brightened/rotated variants of every image in src_dir to dst_dir."""
    dst_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for img_path in src_dir.glob("*.*"):
        image = cv2.imread(str(img_path))
        if image is None:
            continue
        variants = {
            "flip": flip_horizontal(image),
            "bright": adjust_brightness(image),
            "rot": rotate(image),
        }
        for suffix, variant in variants.items():
            out_path = dst_dir / f"{img_path.stem}_{suffix}{img_path.suffix}"
            cv2.imwrite(str(out_path), variant)
            count += 1
    return count


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python ai_model/image_augmentation.py <src_dir> <dst_dir>")
        sys.exit(1)
    n = augment_directory(Path(sys.argv[1]), Path(sys.argv[2]))
    print(f"Wrote {n} augmented images.")
