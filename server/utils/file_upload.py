"""Handles saving uploaded files (disaster report photos, profile pictures) to disk."""
import os
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from config.settings import settings

BASE_UPLOAD_DIR = Path(__file__).resolve().parent.parent / settings.UPLOAD_DIR


def _validate_extension(filename: str) -> str:
    ext = Path(filename).suffix.lower()
    if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '{ext}'. Allowed: {settings.ALLOWED_IMAGE_EXTENSIONS}",
        )
    return ext


async def save_upload_file(file: UploadFile, subfolder: str = "disaster_images") -> str:
    """Saves an UploadFile to disk and returns a relative URL path."""
    ext = _validate_extension(file.filename or "")

    contents = await file.read()
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(contents) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Max size is {settings.MAX_UPLOAD_SIZE_MB}MB.",
        )

    target_dir = BASE_UPLOAD_DIR / subfolder
    target_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid.uuid4().hex}{ext}"
    target_path = target_dir / filename
    with open(target_path, "wb") as f:
        f.write(contents)

    return f"/{settings.UPLOAD_DIR}/{subfolder}/{filename}"


def delete_upload_file(relative_url: str) -> None:
    path = Path(__file__).resolve().parent.parent / relative_url.lstrip("/")
    if path.exists():
        os.remove(path)
