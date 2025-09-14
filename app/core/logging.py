import time
import uuid
import logging
from typing import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("uvicorn.access")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ):
        """
        Logs incoming requests and outgoing responses.

        This middleware captures and logs key information about each request
        and its corresponding response, including:
        - A unique request ID for tracing.
        - Request details: method, URL, client IP, user agent, query parameters,
          and body size.
        - Response details: status code and the time taken to process the request.

        A unique `X-Request-ID` header is added to the response for easy
        correlation with the logs.

        Args:
            request (Request): The incoming request object.
            call_next (Callable): The next middleware or route handler in the chain.

        Returns:
            Response: The response object to be returned to the client.
        """

        request_id: str = str(uuid.uuid4())
        start_time = time.time()

        client_host: str = request.client.host if request.client else "unknown"
        user_agent: str = request.headers.get("user-agent", "-")
        body = await request.body()
        body_size: int = len(body) if body else 0

        logger.info(
            f"➡️ [{request_id}] {request.method} {request.url.path}"
            f" | IP: {client_host} | User Agent: {user_agent}"
            f" | Query: {dict(request.query_params)}"
            f" | Size: {body_size} bytes"
        )

        response = await call_next(request)
        duration = (time.time() - start_time) * 1000

        logger.info(
            f"⬅️ [{request_id}] {request.method} {request.url.path}"
            f" | Status: {response.status_code} | Time: {duration:.2f} ms"
        )

        response.headers["X-Request-ID"] = request_id
        return response
