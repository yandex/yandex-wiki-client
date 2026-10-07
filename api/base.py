from __future__ import annotations
from typing import Any, Iterator, TYPE_CHECKING, Type, TypeVar

from pydantic.v1 import BaseModel

from ..models.pagination import CursorPage

if TYPE_CHECKING:
    from ..client import WikiClient


M = TypeVar('M', bound=BaseModel)


class BaseApi:
    def __init__(self, client: 'WikiClient') -> None:
        self._client = client

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
    ) -> Any:
        return self._client.http.request(method, path, params=params, json=json)

    @staticmethod
    def _parse(model: Type[M], data: Any) -> M:
        return model.parse_obj(data)

    def _list_paginated_collection_page(
        self,
        method: str,
        path: str,
        item_model: Type[M],
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
    ) -> CursorPage[M]:
        data = self._request(method, path, params=params, json=json)
        return CursorPage[item_model].parse_obj(data)

    def _iter_paginated_pages(
        self,
        method: str,
        path: str,
        item_model: Type[M],
        *,
        params: dict[str, Any] | None = None,
    ) -> Iterator[list[M]]:
        base_params: dict[str, Any] = dict(params or {})
        cursor: str | None = None
        while True:
            req_params = dict(base_params)
            if cursor is not None:
                req_params['cursor'] = cursor
            data = self._request(method, path, params=req_params or None)
            yield [self._parse(item_model, item) for item in data.get('results') or []]
            cursor = data.get('next_cursor')
            if not cursor:
                return

    def _iter_paginated_collection(
        self,
        method: str,
        path: str,
        item_model: Type[M],
        *,
        params: dict[str, Any] | None = None,
    ) -> Iterator[M]:
        for page in self._iter_paginated_pages(method, path, item_model, params=params):
            yield from page
