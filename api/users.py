from __future__ import annotations

from .base import BaseApi
from ..models.users import UserMe


class UserApi(BaseApi):
    def get_me(self) -> UserMe:
        data = self._request('GET', 'users/me')
        return self._parse(UserMe, data)
