from fastapi import FastAPI

from app.exceptions import NotFound, not_found_handler
from app.middlewares import LoggingMiddleware
from app.routers import health_router
from app.quotes.router import router as quote_router

app = FastAPI()

app.add_exception_handler(NotFound, not_found_handler)

app.add_middleware(LoggingMiddleware)

app.include_router(health_router)
app.include_router(quote_router)
