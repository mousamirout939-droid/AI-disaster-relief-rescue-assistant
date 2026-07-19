"""CLI: run detection on an image and save an annotated preview to outputs/annotated_images/."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ai_model.inference import run_inference  # noqa: E402
from utils.image_processing import draw_detections, load_image  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs" / "annotated_images"


def predict_and_save(image_path: str) -> Path:
    detections = run_inference(image_path)
    image = load_image(image_path)
    annotated = draw_detections(image, detections)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"annotated_{Path(image_path).name}"

    import cv2
    cv2.imwrite(str(out_path), annotated)
    return out_path


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ai_model/predict.py <image_path>")
        sys.exit(1)
    saved_to = predict_and_save(sys.argv[1])
    print(f"Annotated image saved to {saved_to}")
