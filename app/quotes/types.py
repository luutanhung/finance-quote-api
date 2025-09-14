from typing import TypeAlias, Literal
from enum import Enum

QuoteType: TypeAlias = Literal["inspiration", "practical"]


class QuoteResponseType(str, Enum):
    json = "json"
    svg = "svg"


class Theme(str, Enum):
    light = "light"
    dark = "dark"
