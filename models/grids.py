from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from .base import _Base
from .common import PageIdentity


class GridColumnDefaultSort(_Base):
    slug: str
    title: str
    direction: str


class GridColumn(_Base):
    id: str | None = None
    slug: str
    title: str
    type: str
    required: bool
    width: int | None = None
    width_units: str | None = None
    pinned: str | None = None
    color: str | None = None
    multiple: bool | None = None
    format: str | None = None
    ticket_field: str | None = None
    select_options: list[str] | None = None
    mark_rows: bool | None = None
    description: str | None = None


class GridStructure(_Base):
    default_sort: list[GridColumnDefaultSort] | None = None
    columns: list[GridColumn]


class GridRow(_Base):
    id: str
    row: list[Any]
    pinned: bool | None = None
    color: str | None = None


class GridAttributes(_Base):
    created_at: datetime
    modified_at: datetime


class Grid(_Base):
    id: UUID | int
    created_at: datetime
    title: str
    page: PageIdentity
    structure: GridStructure
    rich_text_format: str
    rows: list[GridRow]
    revision: str
    user_permissions: list[str] | None = None
    attributes: GridAttributes | None = None
    template_id: int | None = None


class GridRevision(_Base):
    revision: str | None = None


class AddRowsResult(_Base):
    revision: str
    results: list[GridRow] | None = None


class GridCell(_Base):
    row_id: str
    column_slug: str
    value: Any = None


class UpdateCellsResult(_Base):
    revision: str | None = None
    cells: list[GridCell]


class ColumnSuggestion(_Base):
    slug: str
    occupied: bool
    suggest: list[str]


class UpdateColumnResult(_Base):
    revision: str
    column: GridColumn
