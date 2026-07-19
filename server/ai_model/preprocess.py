"""Dataset preprocessing: resize/normalize raw images and mirror them into processed_images/."""
from pathlib import Path

import cv2

RAW_DIR = Path(__file__).resolve().parent.parent / "raw_images"
PROCESSED_DIR = Path(__file__).resolve().parent.parent / "processed_images"
TARGET_SIZE = (640, 640)


def preprocess_all(raw_dir: Path = RAW_DIR, out_dir: Path = PROCESSED_DIR) -> int:
    """Resizes every image under raw_dir/<class>/ into out_dir/resized/<class>/. Returns count processed."""
    resized_dir = out_dir / "resized"
    count = 0
    if not raw_dir.exists():
        print(f"No raw images found at {raw_dir} — nothing to preprocess.")
        return 0

    for class_dir in raw_dir.iterdir():
        if not class_dir.is_dir():
            continue
        target_class_dir = resized_dir / class_dir.name
        target_class_dir.mkdir(parents=True, exist_ok=True)

        for img_path in class_dir.glob("*.*"):
            image = cv2.imread(str(img_path))
            if image is None:
                continue
            resized = cv2.resize(image, TARGET_SIZE, interpolation=cv2.INTER_AREA)
            cv2.imwrite(str(target_class_dir / img_path.name), resized)
            count += 1

    return count


if __name__ == "__main__":
    n = preprocess_all()
    print(f"Preprocessed {n} images into {PROCESSED_DIR / 'resized'}")
