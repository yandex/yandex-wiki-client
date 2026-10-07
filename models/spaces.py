from __future__ import annotations
from datetime import datetime

from .base import _Base
from .common import Group
from .users import User


class SpaceRole(_Base):
    id: int
    role: str
    created_at: datetime
    user: User | None = None
    group: Group | None = None


class Space(_Base):
    slug: str
    title: str
    description: str = ''
    search_exclude: bool = False
    created_at: datetime
    modified_at: datetime
    owner: SpaceRole | None = None
    roles: list[SpaceRole] = []
