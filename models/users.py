from __future__ import annotations

from .base import _Base
from .common import UserIdentity  # noqa: F401


class OrganizationIdentity(_Base):
    dir_id: str | None = None
    collab_id: str | None = None


class UserMe(_Base):
    username: str
    homecluster: str | None = None
    identity: UserIdentity
    org: OrganizationIdentity


class User(_Base):
    id: str
    identity: UserIdentity | None = None
    username: str
    display_name: str
    is_dismissed: bool
    affiliation: str
