from __future__ import annotations

from typing import Any, Iterator, Sequence

from .base import BaseApi
from ..models.spaces import Space

MAX_PAGE_SIZE = 100


class SpaceApi(BaseApi):
    def iter_space_pages(
        self,
        *,
        slugs: Sequence[str] | None = None,
        is_personal: bool | None = None,
        show_all: bool = False,
        page_size: int | None = None,
    ) -> Iterator[list[Space]]:
        params: dict[str, Any] = {'show_all': show_all}
        if slugs is not None:
            params['slugs'] = ','.join(slugs)
        if is_personal is not None:
            params['is_personal'] = is_personal
        if page_size is not None:
            params['page_size'] = page_size
        return self._iter_paginated_pages('GET', 'spaces', Space, params=params)
