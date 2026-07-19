"""
Simple in-memory sliding-window rate limiter middleware.
Good enough for a single-process demo deployment; swap for Redis in production.
"""
import time
from collections import defaultdict

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from config.settings import settings


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self._hits: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        window_start = now - settings.RATE_LIMIT_WINDOW_SECONDS

        hits = [t for t in self._hits[client_ip] if t > window_start]
        hits.append(now)
        self._hits[client_ip] = hits

        if len(hits) > settings.RATE_LIMIT_REQUESTS:
            return JSONResponse(
                status_code=429,
                content={"success": False, "message": "Too many requests. Please slow down."},
            )

        return await call_next(request)
