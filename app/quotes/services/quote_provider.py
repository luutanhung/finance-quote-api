from typing import Optional

import json
from pathlib import Path
import random

from app.exceptions import NotFound

from ..types import QuoteType
from ..schemas import Quote


class QuoteProvider:
    def __init__(self) -> None:
        current_dir = Path(__file__).parent
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
        if quote_type:
            filtered_quotes = [q for q in self.quotes if q.type == quote_type]
            if not filtered_quotes:
                raise NotFound()
            return random.choice(filtered_quotes)

        return random.choice(self.quotes)

    def get_quote_by_id(self, id: int) -> Quote:
        found_quote = None
        for quote in self.quotes:
            if quote.id == id:
                found_quote = quote
        if not found_quote:
            raise NotFound()
        return found_quote
