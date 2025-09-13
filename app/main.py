from fastapi import FastAPI

from app.quotes.router import router as quote_router
from app.exceptions import NotFound, not_found_handler

app = FastAPI()

app.add_exception_handler(NotFound, not_found_handler)

app.include_router(quote_router)
