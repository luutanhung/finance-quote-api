from typing import Optional

from pydantic import BaseModel, AnyHttpUrl

from .types import QuoteType


class Quote(BaseModel):
    id: int
    quote: str
    author: Optional[str] = None
    author_avatar_url: Optional[AnyHttpUrl] = None
    type: QuoteType


class QuoteRead(Quote):
    pass
