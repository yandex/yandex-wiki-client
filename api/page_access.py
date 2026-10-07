from __future__ import annotations

from .base import BaseApi
from ..models.common import GroupIdentity, UserIdentity
from ..models.page_access import PageAccess
from ..utils import exclude_none


class PageAccessApi(BaseApi):
    def create(
        self,
        page_id: int,
        role: str,
        *,
        user: UserIdentity | None = None,
        group: GroupIdentity | None = None,
        inheritance: str | None = None,
    ) -> PageAccess:
        body = {
            'role': role,
            **exclude_none(
                user=user.dict(exclude_none=True) if user is not None else None,
                group=group.dict() if group is not None else None,
                inheritance=inheritance,
            ),
        }

        data = self._request('POST', f'pages/{page_id}/access', json=body)
        return self._parse(PageAccess, data)

    def update(
        self,
        page_id: int,
        access_id: str,
        *,
        role: str | None = None,
        inheritance: str | None = None,
        prevent_selflock: bool | None = None,
    ) -> PageAccess:
        params = exclude_none(prevent_selflock=prevent_selflock)
        body = exclude_none(role=role, inheritance=inheritance)

        data = self._request('POST', f'pages/{page_id}/access/{access_id}', params=params, json=body)
        return self._parse(PageAccess, data)

    def delete(
        self,
        page_id: int,
        access_id: str,
        *,
        prevent_selflock: bool | None = None,
    ) -> None:
        params = exclude_none(prevent_selflock=prevent_selflock)
        self._request('DELETE', f'pages/{page_id}/access/{access_id}', params=params)

    def delete_all(
        self,
        page_id: int,
        *,
        prevent_selflock: bool | None = None,
    ) -> None:
        params = exclude_none(prevent_selflock=prevent_selflock)
        self._request('DELETE', f'pages/{page_id}/access', params=params)
