import time
from collections import defaultdict, deque
from typing import Dict, Tuple
# pyrefly: ignore [missing-import]
from fastapi import HTTPException, Request, status

from app.config import settings


class InMemoryRateLimiter:
    """
    Lightweight in-memory sliding-window rate limiter for the MVP.
    
    IMPORTANT ARCHITECTURE NOTES:
    - State is process-local and kept strictly in-memory (no Redis/DB).
    - Counters reset if the server instance restarts.
    - Across multi-instance deployments, each instance enforces its own window.
    - Cleans up stale timestamps automatically to prevent memory leaks.
    """

    def __init__(self, requests_per_minute: int = 5, window_seconds: float = 60.0):
        self.requests_per_minute = requests_per_minute
        self.window_seconds = window_seconds
        self._history: Dict[str, deque] = defaultdict(deque)

    def is_allowed(self, client_ip: str) -> Tuple[bool, int]:
        """
        Evaluates whether client_ip has exceeded the rate limit.
        Returns (is_allowed: bool, retry_after_seconds: int).
        """
        now = time.time()
        window_start = now - self.window_seconds
        client_timestamps = self._history[client_ip]

        # Evict timestamps outside the sliding window
        while client_timestamps and client_timestamps[0] < window_start:
            client_timestamps.popleft()

        # Check limit
        if len(client_timestamps) >= self.requests_per_minute:
            oldest_in_window = client_timestamps[0]
            retry_after = max(1, int(oldest_in_window + self.window_seconds - now))
            return False, retry_after

        # Record this request
        client_timestamps.append(now)
        return True, 0

    def reset(self):
        """Clears all history (useful for testing)."""
        self._history.clear()


# Default limiter instance: 5 requests per minute
rate_limiter = InMemoryRateLimiter(requests_per_minute=5, window_seconds=60.0)


async def rate_limit_dependency(request: Request) -> None:
    """
    FastAPI dependency to enforce rate limiting on specific endpoints.
    Extracts client IP safely from headers (X-Forwarded-For) or client host.
    """
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        client_ip = forwarded_for.split(",")[0].strip()
    elif request.client and request.client.host:
        client_ip = request.client.host
    else:
        client_ip = "127.0.0.1"

    allowed, retry_after = rate_limiter.is_allowed(client_ip)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Maximum 5 requests per minute allowed.",
            headers={"Retry-After": str(retry_after)},
        )
