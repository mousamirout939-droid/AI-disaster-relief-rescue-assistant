"""Small shared helpers for the ml/ package (model persistence, synthetic data)."""
import pickle
from pathlib import Path
from typing import Any


def save_model(model: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(model, f)


def load_model(path: Path) -> Any | None:
    if not path.exists():
        return None
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except Exception:  # noqa: BLE001
        return None
