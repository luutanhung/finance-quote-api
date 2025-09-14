import re

from fastapi import status, Request

from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "60 per hour", "2 per minute"],
)


def rate_limit_exceeded_handler(request: Request, exc):
    detail: str = getattr(exc, "detail", "")
    retry_after: int = 60

    match = re.search(r"(\d+)\s+per\s+1\s+(\w+)", detail)
    if match:
        _, unit = match.groups()
        if unit.startswith("second"):
            retry_after = 1
        elif unit.startswith("minute"):
            retry_after = 60
        elif unit.startswith("hour"):
            retry_after = 3600
        elif unit.startswith("day"):
            retry_after = 86400

    response_body = {
        "detail": "Rate limit exceeded. Please try again later.",
        "retry_after_seconds": retry_after,
    }
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content=response_body,
        headers={"Retry-After": str(retry_after)},
    )
