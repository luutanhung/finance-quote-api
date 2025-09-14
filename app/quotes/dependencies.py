from fastapi import Query

from .types import QuoteResponseType, Theme
from .services import QuoteProvider, SVGConverter


def get_quote_provider() -> QuoteProvider:
    """
    Dependency function to provide a QuoteProvider instance.

    This function is responsible for creating and returning a single instance
    of the `QuoteProvider` class, which manages the quote data.
    """
    return QuoteProvider()


def get_svg_converter(
    theme: Theme = Query(Theme.light, description="Declare theme (light or dark)"),
    width: int = Query(400, ge=400, le=600, description="Width of SVG"),
    height: int = Query(175, ge=175, le=300, description="Height of SVG"),
) -> SVGConverter:
    """
    Dependency function to provide an SVGConverter instance.

    This function constructs and returns an `SVGConverter` object,
    configured based on query parameters from the request. This allows the
    caller to customize the appearance of the generated SVG image.

    Args:
        theme (Theme): The color theme for the SVG (light or dark).
        width (int): The width of the SVG image in pixels.
        height (int): The height of the SVG image in pixels.
    """

    return SVGConverter(width=width, height=height, theme=theme)


def get_quote_response_type(
    response_type: QuoteResponseType = Query(
        QuoteResponseType.json, description="Declare response type (json or svg)"
    ),
) -> QuoteResponseType:
    """
    Dependency function to determine the response format.

    This function extracts the desired response format (e.g., JSON or SVG)
    from the request's query parameters and returns it.
    """

    return response_type
