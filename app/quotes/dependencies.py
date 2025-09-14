from fastapi import Query

from .types import QuoteResponseType
from .services import QuoteProvider, SVGConverter


def get_quote_provider() -> QuoteProvider:
    return QuoteProvider()


def get_svg_converter() -> SVGConverter:
    return SVGConverter()


def get_quote_response_type(
    response_type: QuoteResponseType = Query(
        QuoteResponseType.json, description="Declare response type (json or svg)"
    ),
) -> QuoteResponseType:
    return response_type
