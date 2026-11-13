from __future__ import annotations
from datetime import datetime
from typing import Any
from uuid import UUID

from .attachments import Attachment
from .common import Group
from .base import _Base
from .users import User


class Breadcrumb(_Base):
    id: int | None = None
    title: str
    slug: str
    page_exists: bool


class PageAttributes(_Base):
    created_at: datetime
    modified_at: datetime
    lang: str
    is_readonly: bool
    comments_count: int
    entity_links_count: int
    comments_enabled: bool
    is_collaborative: bool | None = None
    is_draft: bool | None = None
    is_available_for_ai: bool


class PageDetails(_Base):
    id: int
    slug: str
    title: str
    page_type: str


class RevisionDraftInfo(_Base):
    id: int
    created_at: datetime
    modified_at: datetime


class PublicPageRevision(_Base):
    status: str


class PageRevision(_Base):
    id: int
    author: User
    created_at: datetime
    page_type: str
    revision_draft: RevisionDraftInfo | None = None
    publication: PublicPageRevision | None = None


class Actuality(_Base):
    status: str
    marked_at: datetime | None = None
    user: User | None = None
    comment: str | None = None
    external_links: list[str] | None = None
    actual_pages: list[PageDetails] | None = None


class Redirect(_Base):
    page_id: int | None = None
    redirect_target: PageDetails | None = None


class AccessPolicy(_Base):
    access_type: str
    inherited_access_type: str | None = None
    all_staff_role: str | None = None
    has_external: bool | None = None
    invite: dict[str, Any] | None = None


class PageAccessItem(_Base):
    id: str
    created_at: datetime | None = None
    user: User | None = None
    group: Group | None = None
    role: str
    inheritance: str | None = None


class AccessLists(_Base):
    direct: list[PageAccessItem]
    by_link: list[PageAccessItem]
    inherited: list[PageAccessItem]


class Owner(_Base):
    user: User | None = None
    group: Group | None = None


class PageFullDetails(PageDetails):
    last_revision_id: int | None = None
    redirect: Redirect | None = None
    breadcrumbs: list[Breadcrumb] | None = None
    attributes: PageAttributes | None = None
    content: str | None = None
    access_policy: AccessPolicy | None = None
    access_lists: AccessLists | None = None
    owner: Owner | None = None
    actuality: Actuality | None = None
    active_revision: PageRevision | None = None


Page = PageFullDetails


class DeleteResult(_Base):
    recovery_token: UUID


class RecoverPageResult(_Base):
    id: int
    slug: str
    pages_count: int | None = None


class PageRef(_Base):
    id: int
    slug: str


class PageGridResource(_Base):
    id: UUID | int
    title: str
    created_at: datetime


class PageResource(_Base):
    type: str
    item: Attachment | PageGridResource
