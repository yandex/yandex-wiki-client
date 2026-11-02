from __future__ import annotations

from pathlib import Path
from typing import Any, Literal
from uuid import UUID

from .base import BaseApi
from ..models.operations import OperationCreated
from ..models.common import PageIdentity
from ..models.grids import (
    AddRowsResult,
    ColumnSuggestion,
    Grid,
    GridRevision,
    UpdateColumnResult,
    UpdateCellsResult,
)
from ..utils import NOT_SET, exclude_none, exclude_not_set


class GridApi(BaseApi):
    def export(
        self,
        grid_id: str,
        destination: str | Path,
        *,
        format: Literal['csv', 'xls', 'docx'] = 'csv',
        max_bytes: int | None = None,
    ) -> None:
        """Download a native grid export through the Intranet API."""
        self._client.http.download('GET', f'grids/{grid_id}/export/{format}', destination, max_bytes=max_bytes)

    def create(self, page: PageIdentity, title: str) -> Grid:
        body = {
            'page': page.dict(exclude_none=True),
            'title': title,
        }
        data = self._request('POST', 'grids', json=body)
        return self._parse(Grid, data)

    def get(
        self,
        grid_id: UUID | str,
        *,
        only_cols: str | None = None,
        only_rows: str | None = None,
        filter: str | None = None,
        sort: str | None = None,
        revision: int | None = None,
        fields: list[str] | None = None,
    ) -> Grid:
        params = exclude_none(
            only_cols=only_cols,
            only_rows=only_rows,
            filter=filter,
            sort=sort,
            revision=revision,
            fields=','.join(fields) if fields else None,
        )

        data = self._request('GET', f'grids/{grid_id}', params=params or None)
        return self._parse(Grid, data)

    def update(
        self,
        grid_id: UUID | str,
        *,
        revision: str | None = None,
        title: str | None = None,
        default_sort: list[dict[str, str]] | None = None,
    ) -> GridRevision:
        body = exclude_none(revision=revision, title=title, default_sort=default_sort)

        data = self._request('POST', f'grids/{grid_id}', json=body)
        return self._parse(GridRevision, data)

    def delete(self, grid_id: UUID | str) -> None:
        self._request('DELETE', f'grids/{grid_id}')

    def clone(
        self,
        grid_id: UUID | str,
        target: str,
        *,
        title: str | None = None,
        with_data: bool = False,
    ) -> OperationCreated:
        body = {
            'target': target,
            'with_data': with_data,
            **exclude_none(title=title),
        }
        data = self._request('POST', f'grids/{grid_id}/clone', json=body)
        return self._parse(OperationCreated, data)

    def add_rows(
        self,
        grid_id: UUID | str,
        rows: list[dict[str, Any]],
        *,
        revision: str | None = None,
        position: int | None = None,
        after_row_id: str | None = None,
    ) -> AddRowsResult:
        body = {
            'rows': rows,
            **exclude_none(revision=revision, position=position, after_row_id=after_row_id),
        }

        data = self._request('POST', f'grids/{grid_id}/rows', json=body)
        return self._parse(AddRowsResult, data)

    def remove_rows(
        self,
        grid_id: UUID | str,
        row_ids: list[str],
        *,
        revision: str | None = None,
    ) -> GridRevision:
        body = {'row_ids': row_ids, **exclude_none(revision=revision)}

        data = self._request('DELETE', f'grids/{grid_id}/rows', json=body)
        return self._parse(GridRevision, data)

    def add_columns(
        self,
        grid_id: UUID | str,
        columns: list[dict[str, Any]],
        *,
        revision: str | None = None,
        position: int | None = None,
    ) -> GridRevision:
        body = {'columns': columns, **exclude_none(revision=revision, position=position)}

        data = self._request('POST', f'grids/{grid_id}/columns', json=body)
        return self._parse(GridRevision, data)

    def remove_columns(
        self,
        grid_id: UUID | str,
        column_slugs: list[str],
        *,
        revision: str | None = None,
    ) -> GridRevision:
        body = {'column_slugs': column_slugs, **exclude_none(revision=revision)}

        data = self._request('DELETE', f'grids/{grid_id}/columns', json=body)
        return self._parse(GridRevision, data)

    def suggest_column(
        self,
        grid_id: UUID | str,
        *,
        title: str | None = None,
        slug: str | None = None,
    ) -> ColumnSuggestion:
        body = exclude_none(title=title, slug=slug)

        data = self._request('POST', f'grids/{grid_id}/columns/suggest', json=body)
        return self._parse(ColumnSuggestion, data)

    def update_column(
        self,
        grid_id: UUID | str,
        column_slug: str,
        *,
        revision: str | None = None,
        title: str | None = NOT_SET,
        description: str | None = NOT_SET,
        required: bool | None = NOT_SET,
        width: int | None = NOT_SET,
        width_units: str | None = NOT_SET,
        format: str | None = NOT_SET,
        pinned: str | None = NOT_SET,
        color: str | None = NOT_SET,
        multiple: bool | None = NOT_SET,
        ticket_field: str | None = NOT_SET,
        select_options: list[str] | None = NOT_SET,
        mark_rows: bool | None = NOT_SET,
    ) -> UpdateColumnResult:
        body = exclude_not_set(
            revision=revision,
            title=title,
            description=description,
            required=required,
            width=width,
            width_units=width_units,
            format=format,
            pinned=pinned,
            color=color,
            multiple=multiple,
            ticket_field=ticket_field,
            select_options=select_options,
            mark_rows=mark_rows,
        )

        data = self._request('POST', f'grids/{grid_id}/column/{column_slug}', json=body)
        return self._parse(UpdateColumnResult, data)

    def update_cells(
        self,
        grid_id: UUID | str,
        cells: list[dict[str, Any]],
        *,
        revision: str | None = None,
    ) -> UpdateCellsResult:
        body = {'cells': cells, **exclude_none(revision=revision)}

        data = self._request('POST', f'grids/{grid_id}/cells', json=body)
        return self._parse(UpdateCellsResult, data)

    def move_rows(
        self,
        grid_id: UUID | str,
        row_id: str,
        *,
        revision: str | None = None,
        position: int | None = None,
        after_row_id: str | None = None,
        rows_count: int | None = None,
    ) -> GridRevision:
        body = {
            'row_id': row_id,
            **exclude_none(
                revision=revision,
                position=position,
                after_row_id=after_row_id,
                rows_count=rows_count,
            ),
        }

        data = self._request('POST', f'grids/{grid_id}/rows/move', json=body)
        return self._parse(GridRevision, data)

    def update_row(
        self,
        grid_id: UUID | str,
        row_id: str,
        *,
        revision: str | None = None,
        pinned: bool | None = NOT_SET,
        color: str | None = NOT_SET,
    ) -> None:
        body = exclude_not_set(revision=revision, pinned=pinned, color=color)
        self._request('POST', f'grids/{grid_id}/rows/{row_id}', json=body)

    def move_columns(
        self,
        grid_id: UUID | str,
        column_slug: str,
        position: int,
        *,
        revision: str | None = None,
        columns_count: int | None = None,
    ) -> GridRevision:
        body = {
            'column_slug': column_slug,
            'position': position,
            **exclude_none(revision=revision, columns_count=columns_count),
        }

        data = self._request('POST', f'grids/{grid_id}/columns/move', json=body)
        return self._parse(GridRevision, data)
