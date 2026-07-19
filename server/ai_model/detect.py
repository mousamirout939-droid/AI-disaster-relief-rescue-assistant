"""Alias CLI entrypoint kept for parity with the original skeleton's file naming (detect.py vs predict.py)."""
from ai_model.predict import predict_and_save  # noqa: F401

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python ai_model/detect.py <image_path>")
        sys.exit(1)
    print(predict_and_save(sys.argv[1]))
