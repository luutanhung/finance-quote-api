from typing import Optional

from fastapi import APIRouter, Depends, Response, Query

from .types import QuoteType, QuoteResponseType
from .schemas import Quote, QuoteRead
from .dependencies import (
    get_quote_provider,
    get_svg_converter,
    get_quote_response_type,
)
from .services import QuoteProvider, SVGConverter

router = APIRouter(prefix="/api/quotes", tags=["Quote"])


@router.get("/random")
def get_random_quote(
    quote_type: Optional[QuoteType] = Query(None, description="Declare type of quote"),
    response_type: QuoteResponseType = Depends(get_quote_response_type),
    quote_provider: QuoteProvider = Depends(get_quote_provider),
    svg_converter: SVGConverter = Depends(get_svg_converter),
):
    """
    Retrieves a random quote.

    This endpoint returns a random quote from the collection. You can
    optionally filter the quote by its `type` using the `quote_type` query
    parameter. The response can be either a JSON object or an SVG image,
    controlled by the `response_type` parameter.

    Args:
        quote_type (Optional[QuoteType]): The type of quote to retrieve.
            For example, `programming`, `philosophy`, or `humor`.
        response_type (QuoteResponseType): The desired format of the response.
            Defaults to JSON. Use `svg` to get an SVG image.
        quote_provider (QuoteProvider): Dependency to get the quote data.
        svg_converter (SVGConverter): Dependency to convert the quote to SVG.

    Returns:
        Union[QuoteRead, Response]: A QuoteRead Pydantic model in JSON format,
                                    or a FastAPI Response with an SVG image.

    Raises:
        HTTPException: 404 Not Found if no quotes of the specified type exist.
    """

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
    svg_converter: SVGConverter = Depends(get_svg_converter),
):
    """
    Retrieves a quote by its unique ID.

    This endpoint fetches a specific quote using its integer ID. The response
    can be either a JSON object or an SVG image, depending on the
    `response_type` parameter.

    Args:
        id (int): The unique integer ID of the quote.
        response_type (QuoteResponseType): The desired format of the response.
            Defaults to JSON. Use `svg` to get an SVG image.
        quote_provider (QuoteProvider): Dependency to get the quote data.
        svg_converter (SVGConverter): Dependency to convert the quote to SVG.

    Returns:
        Union[QuoteRead, Response]: A QuoteRead Pydantic model in JSON format,
                                    or a FastAPI Response with an SVG image.

    Raises:
        HTTPException: 404 Not Found if the quote with the specified ID does
                       not exist.
    """

    quote: Quote = quote_provider.get_quote_by_id(id)
    if response_type == QuoteResponseType.svg:
        quote_svg: str = svg_converter.convert_to_svg(quote)
        return Response(content=quote_svg, media_type="image/svg+xml")
    return QuoteRead(**quote.model_dump())
