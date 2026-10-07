from __future__ import annotations

from typing import Any
from uuid import UUID

from .base import _Base
from .pages import PageRef


class OperationIdentity(_Base):
    type: str
    id: str


class OperationCreated(_Base):
    operation: OperationIdentity
    dry_run: bool = False
    status_url: str


class OperationProgress(_Base):
    percentage: float
    details: str


class PageCloneResult(_Base):
    page: PageRef


class GridCloneResult(_Base):
    grid: PageRef | None = None
    page: PageRef
    grid_id: UUID | int


class MoveResult(_Base):
    page_count: int


class PageCloneOperationStatus(_Base):
    status: str
    progress: OperationProgress | None = None
    result: PageCloneResult | dict[str, Any] | None = None


class GridCloneOperationStatus(_Base):
    status: str
    progress: OperationProgress | None = None
    result: GridCloneResult | dict[str, Any] | None = None


class MoveOperationStatus(_Base):
    status: str
    progress: OperationProgress | None = None
    result: MoveResult | dict[str, Any] | None = None
