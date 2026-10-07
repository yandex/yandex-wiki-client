from __future__ import annotations
from typing import Iterator

from .base import BaseApi
from ..models.comments import (
    Comment,
    CommentExtended,
    DeleteCommentResult,
)
from ..models.pagination import CursorPage
from ..utils import exclude_none


class CommentApi(BaseApi):
    def list(
        self,
        page_id: int,
        *,
        order_by: str | None = None,
        order_direction: str | None = None,
        status_filter: str | None = None,
    ) -> list[CommentExtended]:
        return list(
            self.iter_comments(
                page_id,
                order_by=order_by,
                order_direction=order_direction,
                status_filter=status_filter,
            )
        )

    def iter_comments(
        self,
        page_id: int,
        *,
        order_by: str | None = None,
        order_direction: str | None = None,
        status_filter: str | None = None,
    ) -> Iterator[CommentExtended]:
        params = exclude_none(
            order_by=order_by,
            order_direction=order_direction,
            status_filter=status_filter,
        )
        return self._iter_paginated_collection(
            'GET',
            f'pages/{page_id}/comments',
            CommentExtended,
            params=params or None,
        )

    def list_page(
        self,
        page_id: int,
        *,
        order_by: str | None = None,
        order_direction: str | None = None,
        status_filter: str | None = None,
        page_size: int | None = None,
        cursor: str | None = None,
    ) -> CursorPage[CommentExtended]:
        params = exclude_none(
            order_by=order_by,
            order_direction=order_direction,
            status_filter=status_filter,
            page_size=page_size,
            cursor=cursor,
        )
        return self._list_paginated_collection_page(
            'GET',
            f'pages/{page_id}/comments',
            CommentExtended,
            params=params or None,
        )

    def get_thread(self, page_id: int, comment_id: int) -> list[Comment]:
        return list(self.iter_thread(page_id, comment_id))

    def iter_thread(self, page_id: int, comment_id: int) -> Iterator[Comment]:
        return self._iter_paginated_collection(
            'GET',
            f'pages/{page_id}/comments/{comment_id}/thread',
            Comment,
        )

    def create(
        self,
        page_id: int,
        body: str,
        *,
        parent_id: int | None = None,
        thread_id: int | None = None,
        inline_text: str | None = None,
    ) -> Comment:
        payload = {
            'body': body,
            **exclude_none(parent_id=parent_id, thread_id=thread_id, inline_text=inline_text),
        }
        data = self._request('POST', f'pages/{page_id}/comments', json=payload)
        return self._parse(Comment, data)

    def delete(self, page_id: int, comment_id: int) -> DeleteCommentResult:
        data = self._request('DELETE', f'pages/{page_id}/comments/{comment_id}')
        return self._parse(DeleteCommentResult, data)
