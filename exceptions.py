from __future__ import annotations
import json
from typing import Any

import httpx


class WikiClientError(Exception):
    pass


class ConfigError(WikiClientError):
    pass


class NetworkError(WikiClientError):
    pass


class ApiError(WikiClientError):
    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str | None = None,
        details: Any = None,
        response: httpx.Response | None = None,
    ) -> None:
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.details = details
        self.response = response
        super().__init__(self._format())

    def _format(self) -> str:
        msg = self.message or ''
        return f'[{self.status_code} {self.error_code}] {msg}'.rstrip()


class UnauthorizedError(ApiError):
    pass


class RateLimitedError(ApiError):
    pass


class SlugOccupiedError(ApiError):
    error_code = 'SLUG_OCCUPIED'


class SlugReservedError(ApiError):
    error_code = 'SLUG_RESERVED'


class PageNotFoundError(ApiError):
    error_code = 'NOT_FOUND'


class PageIsReservedError(ApiError):
    error_code = 'PAGE_IS_RESERVED'


class ChangesConflictError(ApiError):
    error_code = 'CHANGES_CONFLICT'


class ValidationApiError(ApiError):
    error_code = 'VALIDATION_ERROR'


class ForbiddenError(ApiError):
    error_code = 'FORBIDDEN'


class PageAccessAlreadyGrantedError(ApiError):
    error_code = 'PAGE_ACCESS_ALREADY_GRANTED'


class FeatureDisabledError(ApiError):
    error_code = 'FEATURE_DISABLED'


class SpaceRequiredError(ApiError):
    error_code = 'SPACE_REQUIRED'


_ERROR_CODE_REGISTRY: dict[str, type[ApiError]] = {
    cls.error_code: cls
    for cls in [
        SlugOccupiedError,
        SlugReservedError,
        PageNotFoundError,
        PageIsReservedError,
        ChangesConflictError,
        ValidationApiError,
        ForbiddenError,
        PageAccessAlreadyGrantedError,
        FeatureDisabledError,
        SpaceRequiredError,
    ]
}


def error_from_response(response: httpx.Response) -> ApiError:
    status = response.status_code
    body: Any
    try:
        body = response.json()
    except (json.JSONDecodeError, ValueError):
        body = None

    if isinstance(body, dict):
        error_code = body.get('error_code') or f'HTTP_{status}'
        message = body.get('message') or body.get('debug_message')
        details = body.get('details')
    else:
        error_code = f'HTTP_{status}'
        message = response.text or None
        details = None

    cls = _ERROR_CODE_REGISTRY.get(error_code)
    if cls is None:
        if status == 401:
            cls = UnauthorizedError
        elif status == 429:
            cls = RateLimitedError
        else:
            cls = ApiError

    return cls(
        status_code=status,
        error_code=error_code,
        message=message,
        details=details,
        response=response,
    )
