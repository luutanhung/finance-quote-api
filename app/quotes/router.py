from typing import Optional

from fastapi import APIRouter, Depends

from .types import QuoteType
from .schemas import Quote, QuoteRead
from .dependencies import get_quote_provider
from .services.quote_provider import QuoteProvider

router = APIRouter(prefix="/quotes", tags=["Quote"])


@router.get("/random", response_model=QuoteRead)
def get_random_quote(
    quote_type: Optional[QuoteType] = None,
    quote_provider: QuoteProvider = Depends(get_quote_provider),
):
    quote: Quote = quote_provider.get_random_quote(quote_type)
    return QuoteRead(**quote.model_dump())


@router.get("/{id}", response_model=QuoteRead)
def get_quote_by_id(
    id: int, quote_provider: QuoteProvider = Depends(get_quote_provider)
):
    quote: Quote = quote_provider.get_quote_by_id(id)
    return QuoteRead(**quote.model_dump())
