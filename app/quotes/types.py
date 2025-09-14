from typing import TypeAlias, Literal
from enum import Enum

QuoteType: TypeAlias = Literal["inspiration", "practical"]


class QuoteResponseType(str, Enum):
    json = "json"
    svg = "svg"
