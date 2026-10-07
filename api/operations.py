from __future__ import annotations

from .base import BaseApi
from ..models.operations import (
    GridCloneOperationStatus,
    MoveOperationStatus,
    PageCloneOperationStatus,
)


class OperationApi(BaseApi):
    def get_clone_status(self, task_id: str) -> PageCloneOperationStatus:
        data = self._request('GET', f'operations/clone/{task_id}')
        return self._parse(PageCloneOperationStatus, data)

    def get_clone_inline_grid_status(self, task_id: str) -> GridCloneOperationStatus:
        data = self._request('GET', f'operations/clone_inline_grid/{task_id}')
        return self._parse(GridCloneOperationStatus, data)

    def get_move_status(self, task_id: str) -> MoveOperationStatus:
        data = self._request('GET', f'operations/move/{task_id}')
        return self._parse(MoveOperationStatus, data)
