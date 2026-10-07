from __future__ import annotations

from .base import BaseApi
from ..models.pages import RecoverPageResult


class RecoveryTokenApi(BaseApi):
    def recover(self, recovery_token: str) -> RecoverPageResult:
        data = self._request('POST', f'recovery_tokens/{recovery_token}/recover')
        return self._parse(RecoverPageResult, data)
