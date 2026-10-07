from __future__ import annotations
from typing import Any, Iterator

from .base import BaseApi
from ..models.pagination import CursorPage
from ..models.search import SearchResult
from ..utils import exclude_none


class SearchApi(BaseApi):
    def list(
        self,
        query: str,
        *,
        filters: dict[str, Any] | None = None,
        cursor: int = 1,
        limit: int = 10,
        order_by: str = 'relevancy',
        highlight: bool = False,
    ) -> list[SearchResult]:
        return list(
            self.iter_results(
                query,
                filters=filters,
                cursor=cursor,
                limit=limit,
                order_by=order_by,
                highlight=highlight,
            )
        )

    def iter_results(
        self,
        query: str,
        *,
        filters: dict[str, Any] | None = None,
        cursor: int = 1,
        limit: int = 10,
        order_by: str = 'relevancy',
        highlight: bool = False,
    ) -> Iterator[SearchResult]:
        body = {
            'query': query,
            'cursor': cursor,
            'limit': limit,
            'order_by': order_by,
            'highlight': highlight,
            **exclude_none(filters=filters),
        }

        while True:
            data = self._request('POST', 'search', json=body)
            for item in data.get('results') or []:
                yield self._parse(SearchResult, item)

            next_cursor = data.get('next_cursor')
            if not next_cursor:
                return
            body['cursor'] = int(next_cursor)

    def list_page(
        self,
        query: str,
        *,
        filters: dict[str, Any] | None = None,
        cursor: int = 1,
        limit: int = 10,
        order_by: str = 'relevancy',
        highlight: bool = False,
    ) -> CursorPage[SearchResult]:
        body = {
            'query': query,
            'cursor': cursor,
            'limit': limit,
            'order_by': order_by,
            'highlight': highlight,
            **exclude_none(filters=filters),
        }
        return self._list_paginated_collection_page('POST', 'search', SearchResult, json=body)
