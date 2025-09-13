from typing import Optional, Literal

from fastapi import APIRouter

from .schemas import Quote, QuoteRead
from .services import QuoteService

quote_service = QuoteService()

router = APIRouter(prefix="/quotes", tags=["Quote"])


@router.get("/random", response_model=QuoteRead)
def get_random_quote(type: Optional[Literal["inspiration", "practical"]] = None):
    quote: Quote = quote_service.get_random_quote(type)
    return QuoteRead(**quote.model_dump())


@router.get("/{id}", response_model=QuoteRead)
def get_quote_by_id(id: int):
    quote: Quote = quote_service.get_quote_by_id(id)
    return QuoteRead(**quote.model_dump())
