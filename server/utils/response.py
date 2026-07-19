"""Standard API response envelope helpers so every endpoint returns a consistent shape."""
from typing import Any, Optional

from fastapi.responses import JSONResponse


def success_response(data: Any = None, message: str = "Success", status_code: int = 200) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"success": True, "message": message, "data": data})


def error_response(message: str = "Something went wrong", status_code: int = 400, errors: Optional[Any] = None) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"success": False, "message": message, "errors": errors})
