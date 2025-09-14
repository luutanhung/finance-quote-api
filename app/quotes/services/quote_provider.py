from typing import Optional

import json
from pathlib import Path
import random

from app.exceptions import NotFound

from ..types import QuoteType
from ..schemas import Quote


class QuoteProvider:
    """
    Mananges and provides access to a collection of quotes from a static JSON file.

    This class handles the loading of quotes from a specified JSON file,
    assigns a unique ID to each quote, and provides methods to retrieve quotes
    randomly or by a specific ID or type.
    """

    def __init__(self) -> None:
        """
        Initializes the QuoteProvider by loading quotes from 'quotes.json'.

        The method locates the 'quotes.json' file, reads its content, and
        parses it into a list of Quote objects. Each quote is assigned a
        unique integer ID.
        """

        current_dir = Path(__file__).parent.parent
        file_path = current_dir / "data" / "quotes.json"
        with open(file_path, "r") as f:
            data = json.load(f)
            self.quotes: list[Quote] = []
            counter: int = 1
            for q in data:
                q["id"] = counter
                counter += 1
                self.quotes.append(Quote(**q))

    def get_random_quote(self, quote_type: Optional[QuoteType] = None) -> Quote:
        """
        Retrieves a random quote.

        If a `quote_type` is provided, a random quote of that specific type
        is returned. Otherwise, a random quote from the entire collection is
        returned.

        Args:
            quote_type (Optional[QuoteType]): The type of quote to filter by.

        Raises:
            NotFound: If no quotes are found for the specified type.

        Returns:
            Quote: A randomly selected Quote object.
        """

        if quote_type:
            filtered_quotes = [q for q in self.quotes if q.type == quote_type]
            if not filtered_quotes:
                raise NotFound()
            return random.choice(filtered_quotes)

        return random.choice(self.quotes)

    def get_quote_by_id(self, id: int) -> Quote:
        """
        Retrieves a specific quote by its ID.

        Args:
            id (int): The unique integer ID of the quote to retrieve.

        Raises:
            NotFound: If no quote with the given ID is found.

        Returns:
            Quote: The Quote object with the matching ID.
        """

        found_quote = None
        for quote in self.quotes:
            if quote.id == id:
                found_quote = quote
        if not found_quote:
            raise NotFound()
        return found_quote
