from app.quotes.services.quote_provider import QuoteProvider


def get_quote_provider() -> QuoteProvider:
    return QuoteProvider()
