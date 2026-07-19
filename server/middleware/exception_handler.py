"""Global exception handlers registered on the FastAPI app for consistent error responses."""
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from config.logging import logger
from utils.response import error_response


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return error_response(
            message="Validation error",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            errors=exc.errors(),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return error_response(message=str(exc.detail), status_code=exc.status_code)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.error("Unhandled exception on %s: %s", request.url.path, exc, exc_info=True)
        return error_response(message="Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
