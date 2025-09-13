from typing import Optional

from pydantic import BaseModel, AnyHttpUrl


class Quote(BaseModel):
    id: int
    quote: str
    author: Optional[str] = None
    author_avatar_url: Optional[AnyHttpUrl] = None
    type: str


class QuoteRead(Quote):
    pass
