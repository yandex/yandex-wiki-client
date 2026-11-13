from __future__ import annotations
from datetime import datetime

from .base import _Base
from .common import Group
from .users import User


class PageAccess(_Base):
    id: str
    created_at: datetime | None = None
    user: User | None = None
    group: Group | None = None
    role: str
    inheritance: str | None = None
