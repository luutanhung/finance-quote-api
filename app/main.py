import sys

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from slowapi.errors import RateLimitExceeded

from app.exceptions import NotFound, not_found_handler
from app.core import LoggingMiddleware
from app.core.rate_limiter import limiter, rate_limit_exceeded_handler
from app.routers import health_router
from app.quotes.router import router as quote_router

IS_PROD = "production" if sys.argv[1] == "run" else "development"

if IS_PROD == "production":
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
else:
    app = FastAPI()

app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
app.add_exception_handler(NotFound, not_found_handler)

app.add_middleware(LoggingMiddleware)


@app.get("/", include_in_schema=False)
async def homepage():
    if IS_PROD:
        return RedirectResponse("https://luutanhung.github.io/finance-quote-api/")
    RedirectResponse("/docs")


@app.get("/docs", include_in_schema=False)
async def custom_docs():
    if IS_PROD:
        return RedirectResponse("https://luutanhung.github.io/finance-quote-api/")
    RedirectResponse("/docs")


@app.get("/docs", include_in_schema=False)
async def custom_redoc():
    if IS_PROD:
        return RedirectResponse("https://luutanhung.github.io/finance-quote-api/")
    RedirectResponse("/redoc")


app.include_router(health_router)
app.include_router(quote_router)
