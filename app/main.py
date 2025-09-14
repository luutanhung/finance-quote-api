from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded

from app.exceptions import NotFound, not_found_handler
from app.core import LoggingMiddleware
from app.core.rate_limiter import limiter, rate_limit_exceeded_handler
from app.routers import health_router
from app.quotes.router import router as quote_router

app = FastAPI()

app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
app.add_exception_handler(NotFound, not_found_handler)

app.add_middleware(LoggingMiddleware)

app.include_router(health_router)
app.include_router(quote_router)
