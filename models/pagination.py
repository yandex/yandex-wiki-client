from __future__ import annotations

from typing import Generic, TypeVar

from pydantic.v1.generics import GenericModel

T = TypeVar('T')


class CursorPage(GenericModel, Generic[T]):
    results: list[T]
    next_cursor: str | None = None
    prev_cursor: str | None = None
