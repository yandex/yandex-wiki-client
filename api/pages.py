from __future__ import annotations
from typing import Any, Iterator

from .base import BaseApi
from ..models.operations import OperationCreated
from ..models.pages import (
    DeleteResult,
    Page,
    PageDetails,
    PageGridResource,
    PageRef,
    PageResource,
    PageRevision,
)
from ..models.pagination import CursorPage
from ..utils import exclude_none


class PageApi(BaseApi):
    def get_by_id(
        self,
        page_id: int,
        *,
        revision_id: int | None = None,
        fields: list[str] | None = None,
    ) -> Page:
        params = exclude_none(
            revision_id=revision_id,
            fields=','.join(fields) if fields else None,
        )
        data = self._request('GET', f'pages/{page_id}', params=params or None)
        return self._parse(Page, data)

    def get_by_slug(
        self,
        slug: str,
        *,
        revision_id: int | None = None,
        fields: list[str] | None = None,
    ) -> Page:
        params = {
            'slug': slug,
            **exclude_none(
                revision_id=revision_id,
                fields=','.join(fields) if fields else None,
            ),
        }
        data = self._request('GET', 'pages', params=params)
        return self._parse(Page, data)

    def create(
        self,
        slug: str,
        title: str,
        *,
        content: str | None = None,
        access_policy: dict[str, Any] | None = None,
    ) -> Page:
        body = {
            'slug': slug,
            'title': title,
            **exclude_none(content=content, access_policy=access_policy),
        }

        data = self._request('POST', 'pages', json=body)
        return self._parse(Page, data)

    def update(
        self,
        page_id: int,
        *,
        title: str | None = None,
        content: str | None = None,
        redirect: dict[str, Any] | None = None,
        actuality: dict[str, Any] | None = None,
        access_policy: dict[str, Any] | None = None,
        owner: dict[str, Any] | None = None,
        is_silent: bool = False,
        allow_merge: bool = False,
        revision: int | None = None,
    ) -> PageDetails:
        body = exclude_none(
            revision=str(revision) if revision is not None else None,
            title=title,
            content=content,
            redirect=redirect,
            actuality=actuality,
            access_policy=access_policy,
            owner=owner,
        )

        params = {'is_silent': is_silent, 'allow_merge': allow_merge}
        data = self._request('POST', f'pages/{page_id}', params=params, json=body)
        return self._parse(PageDetails, data)

    def delete(self, page_id: int, *, recursive: bool = False) -> DeleteResult:
        data = self._request(
            'DELETE',
            f'pages/{page_id}',
            params={'recursive': recursive},
        )
        return self._parse(DeleteResult, data)

    def clone(
        self,
        page_id: int,
        target: str,
        *,
        title: str | None = None,
        subscribe_me: bool = False,
    ) -> OperationCreated:
        body = {
            'target': target,
            'subscribe_me': subscribe_me,
            **exclude_none(title=title),
        }
        data = self._request('POST', f'pages/{page_id}/clone', json=body)
        return self._parse(OperationCreated, data)

    def move(
        self,
        operations: list[dict[str, Any]],
        *,
        copy_inherited_access: bool | None = None,
        dry_run: bool = False,
    ) -> OperationCreated:
        body = {
            'operations': operations,
            **exclude_none(copy_inherited_access=copy_inherited_access),
        }
        data = self._request('POST', 'pages/move', params={'dry_run': dry_run}, json=body)
        return self._parse(OperationCreated, data)

    def list_revisions(
        self,
        page_id: int,
        *,
        ids: list[int] | None = None,
        page_size: int | None = None,
    ) -> list[PageRevision]:
        return list(self.iter_revisions(page_id, ids=ids, page_size=page_size))

    def list_revisions_page(
        self,
        page_id: int,
        *,
        ids: list[int] | None = None,
        page_size: int | None = None,
        cursor: str | None = None,
    ) -> CursorPage[PageRevision]:
        params = exclude_none(
            ids=','.join(str(revision_id) for revision_id in ids) if ids else None,
            page_size=page_size,
            cursor=cursor,
        )
        return self._list_paginated_collection_page(
            'GET',
            f'pages/{page_id}/revisions',
            PageRevision,
            params=params or None,
        )

    def iter_revisions(
        self,
        page_id: int,
        *,
        ids: list[int] | None = None,
        page_size: int | None = None,
    ) -> Iterator[PageRevision]:
        params = exclude_none(
            ids=','.join(str(revision_id) for revision_id in ids) if ids else None,
            page_size=page_size,
        )
        return self._iter_paginated_collection(
            'GET',
            f'pages/{page_id}/revisions',
            PageRevision,
            params=params or None,
        )

    def append_content(
        self,
        page_id: int,
        content: str,
        *,
        body: dict[str, Any] | None = None,
        section: dict[str, Any] | None = None,
        anchor: dict[str, Any] | None = None,
        fields: list[str] | None = None,
        is_silent: bool = False,
        revision: int | None = None,
    ) -> Page:
        payload = {
            'content': content,
            **exclude_none(
                body=body,
                section=section,
                anchor=anchor,
                revision=str(revision) if revision is not None else None,
            ),
        }
        params = {
            'is_silent': is_silent,
            **exclude_none(fields=','.join(fields) if fields else None),
        }

        data = self._request('POST', f'pages/{page_id}/append-content', params=params, json=payload)
        return self._parse(Page, data)

    def list_grids(
        self,
        page_id: int,
        *,
        order_by: str | None = None,
        order_direction: str | None = None,
        page_size: int | None = None,
    ) -> list[PageGridResource]:
        return list(
            self.iter_grids(
                page_id,
                order_by=order_by,
                order_direction=order_direction,
                page_size=page_size,
            )
        )

    def list_grids_page(
        self,
        page_id: int,
        *,
        order_by: str | None = None,
        order_direction: str | None = None,
        page_size: int | None = None,
        cursor: str | None = None,
    ) -> CursorPage[PageGridResource]:
        params = exclude_none(
            order_by=order_by,
            order_direction=order_direction,
            page_size=page_size,
            cursor=cursor,
        )
        return self._list_paginated_collection_page(
            'GET',
            f'pages/{page_id}/grids',
            PageGridResource,
            params=params or None,
        )

    def iter_grids(
        self,
        page_id: int,
        *,
        order_by: str | None = None,
        order_direction: str | None = None,
        page_size: int | None = None,
    ) -> Iterator[PageGridResource]:
        params = exclude_none(
            order_by=order_by,
            order_direction=order_direction,
            page_size=page_size,
        )
        return self._iter_paginated_collection(
            'GET',
            f'pages/{page_id}/grids',
            PageGridResource,
            params=params or None,
        )

    def iter_descendants_by_id(
        self,
        page_id: int,
        *,
        include_self: bool = False,
        actuality: str | None = None,
        show_all: bool = False,
        page_size: int | None = None,
    ) -> Iterator[PageRef]:
        params = {
            'include_self': include_self,
            'show_all': show_all,
            **exclude_none(actuality=actuality, page_size=page_size),
        }
        return self._iter_paginated_collection(
            'GET',
            f'pages/{page_id}/descendants',
            PageRef,
            params=params,
        )

    def list_descendants_by_id_page(
        self,
        page_id: int,
        *,
        include_self: bool = False,
        actuality: str | None = None,
        show_all: bool = False,
        page_size: int | None = None,
        cursor: str | None = None,
    ) -> CursorPage[PageRef]:
        params = {
            'include_self': include_self,
            'show_all': show_all,
            **exclude_none(actuality=actuality, page_size=page_size, cursor=cursor),
        }
        return self._list_paginated_collection_page(
            'GET',
            f'pages/{page_id}/descendants',
            PageRef,
            params=params,
        )

    def list_descendants_by_id(
        self,
        page_id: int,
        *,
        include_self: bool = False,
        actuality: str | None = None,
        show_all: bool = False,
        page_size: int | None = None,
    ) -> list[PageRef]:
        return list(
            self.iter_descendants_by_id(
                page_id,
                include_self=include_self,
                actuality=actuality,
                show_all=show_all,
                page_size=page_size,
            )
        )

    def iter_descendants_by_slug(
        self,
        slug: str,
        *,
        include_self: bool = False,
        show_all: bool = False,
    ) -> Iterator[PageRef]:
        return self._iter_paginated_collection(
            'GET',
            'pages/descendants',
            PageRef,
            params={'slug': slug, 'include_self': include_self, 'show_all': show_all},
        )

    def list_descendants_by_slug(
        self,
        slug: str,
        *,
        include_self: bool = False,
        show_all: bool = False,
    ) -> list[PageRef]:
        return list(self.iter_descendants_by_slug(slug, include_self=include_self, show_all=show_all))

    def list_backlinks(
        self,
        page_id: int,
        *,
        for_cluster: bool = False,
        show_all: bool = False,
        page_size: int | None = None,
    ) -> list[PageRef]:
        return list(
            self.iter_backlinks(
                page_id,
                for_cluster=for_cluster,
                show_all=show_all,
                page_size=page_size,
            )
        )

    def iter_backlinks(
        self,
        page_id: int,
        *,
        for_cluster: bool = False,
        show_all: bool = False,
        page_size: int | None = None,
    ) -> Iterator[PageRef]:
        params = {
            'for_cluster': for_cluster,
            'show_all': show_all,
            **exclude_none(page_size=page_size),
        }
        return self._iter_paginated_collection(
            'GET',
            f'pages/{page_id}/backlinks',
            PageRef,
            params=params,
        )

    def list_resources(
        self,
        page_id: int,
        *,
        order_by: str | None = None,
        order_direction: str | None = None,
        types: list[str] | None = None,
        q: str | None = None,
        page_size: int | None = None,
    ) -> list[PageResource]:
        return list(
            self.iter_resources(
                page_id,
                order_by=order_by,
                order_direction=order_direction,
                types=types,
                q=q,
                page_size=page_size,
            )
        )

    def list_resources_page(
        self,
        page_id: int,
        *,
        order_by: str | None = None,
        order_direction: str | None = None,
        types: list[str] | None = None,
        q: str | None = None,
        page_size: int | None = None,
        cursor: str | None = None,
    ) -> CursorPage[PageResource]:
        params = exclude_none(
            order_by=order_by,
            order_direction=order_direction,
            types=','.join(types) if types else None,
            q=q,
            page_size=page_size,
            cursor=cursor,
        )
        return self._list_paginated_collection_page(
            'GET',
            f'pages/{page_id}/resources',
            PageResource,
            params=params or None,
        )

    def iter_resources(
        self,
        page_id: int,
        *,
        order_by: str | None = None,
        order_direction: str | None = None,
        types: list[str] | None = None,
        q: str | None = None,
        page_size: int | None = None,
    ) -> Iterator[PageResource]:
        params = exclude_none(
            order_by=order_by,
            order_direction=order_direction,
            types=','.join(types) if types else None,
            q=q,
            page_size=page_size,
        )
        return self._iter_paginated_collection(
            'GET',
            f'pages/{page_id}/resources',
            PageResource,
            params=params or None,
        )
