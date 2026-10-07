from __future__ import annotations
from datetime import datetime

from .base import _Base
from .users import User


class Attachment(_Base):
    id: int
    name: str
    is_downloadable: bool = True
    download_url: str
    size: str
    description: str
    user: User | None = None
    created_at: datetime
    mimetype: str
    has_preview: bool
    check_status: str
