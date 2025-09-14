from typing import Optional

from fastapi import APIRouter, Depends, Response, Query

from .types import QuoteType, QuoteResponseType
from .schemas import Quote, QuoteRead
from .dependencies import get_quote_provider, get_svg_converter, get_quote_response_type
from .services import QuoteProvider, SVGConverter

router = APIRouter(prefix="/quotes", tags=["Quote"])


@router.get("/random")
def get_random_quote(
    quote_type: Optional[QuoteType] = Query(None, description="Declare type of quote"),
    response_type: QuoteResponseType = Depends(get_quote_response_type),
    quote_provider: QuoteProvider = Depends(get_quote_provider),
    svg_converter: SVGConverter = Depends(get_svg_converter),
):
    quote: Quote = quote_provider.get_random_quote(quote_type)
    if response_type == QuoteResponseType.svg:
        quote_svg: str = svg_converter.convert_to_svg(quote)
        return Response(content=quote_svg, media_type="image/svg+xml")
    return QuoteRead(**quote.model_dump())


@router.get("/{id}", response_model=QuoteRead)
def get_quote_by_id(
    id: int,
    response_type: QuoteResponseType = Depends(get_quote_response_type),
    quote_provider: QuoteProvider = Depends(get_quote_provider),
):
    quote: Quote = quote_provider.get_quote_by_id(id)
    return QuoteRead(**quote.model_dump())
