from __future__ import annotations
from datetime import datetime

from .base import _Base


class SearchResult(_Base):
    url: str
    slug: str
    title: str
    content: str
    type: str
    modified_at: datetime
