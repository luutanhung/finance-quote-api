from fastapi import Query

from .types import QuoteResponseType, Theme
from .services import QuoteProvider, SVGConverter


def get_quote_provider() -> QuoteProvider:
    return QuoteProvider()


def get_svg_converter(
    theme: Theme = Query(Theme.light, description="Declare theme (light or dark)"),
    width: int = Query(400, ge=400, le=600, description="Width of SVG"),
    height: int = Query(175, ge=175, le=300, description="Height of SVG"),
) -> SVGConverter:
    return SVGConverter(width=width, height=height, theme=theme)


def get_quote_response_type(
    response_type: QuoteResponseType = Query(
        QuoteResponseType.json, description="Declare response type (json or svg)"
    ),
) -> QuoteResponseType:
    return response_type
