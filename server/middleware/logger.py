"""Request/response logging middleware — logs method, path, status code, and duration."""
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from config.logging import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "%s %s -> %s (%.1fms)",
            request.method, request.url.path, response.status_code, duration_ms,
        )
        return response
