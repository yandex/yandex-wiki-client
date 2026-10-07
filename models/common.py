from __future__ import annotations
from typing import Any

from .base import _Base


class UserIdentity(_Base):
    uid: str | None = None
    cloud_uid: str | None = None


class GroupIdentity(_Base):
    src: str
    id: str


class Group(_Base):
    id: str | None = None
    identity: GroupIdentity
    name: str
    type: str
    metadata: dict[str, Any] | None = None
    members_count: int | None = None


class PageIdentity(_Base):
    id: int | None = None
    slug: str | None = None
