from __future__ import annotations
from contextlib import contextmanager
from functools import wraps
import tempfile
import time
from pathlib import Path
from typing import Any, BinaryIO, Callable, Iterator

import httpx

from .exceptions import (
    NetworkError,
    WikiClientError,
    error_from_response,
)

_RETRYABLE_STATUSES = {429, 502, 503, 504}
_MAX_BACKOFF_SECONDS = 8.0


@contextmanager
def _atomic_download(destination: Path) -> Iterator[BinaryIO]:
    output = tempfile.NamedTemporaryFile(mode='wb', dir=destination.parent, delete=False)
    temporary_path = Path(output.name)
    try:
        with output:
            yield output
        temporary_path.replace(destination)
    finally:
        temporary_path.unlink(missing_ok=True)


def _write_download(response: httpx.Response, destination: Path, max_bytes: int | None = None) -> None:
    with _atomic_download(destination) as output:
        size = 0
        for chunk in response.iter_bytes(chunk_size=64 * 1024):
            size += len(chunk)
            if max_bytes is not None and size > max_bytes:
                raise WikiClientError(f'File exceeds the transfer limit of {max_bytes} bytes')
            output.write(chunk)


def retry(send: Callable[..., httpx.Response]) -> Callable[..., httpx.Response]:
    @wraps(send)
    def wrapped(
        client: Any,
        method: str,
        url_path: str,
        *args: Any,
        **kwargs: Any,
    ) -> httpx.Response:
        retries = client._retries
        attempts = retries + 1
        last_exc: Exception | None = None

        for attempt in range(attempts):
            try:
                response = send(client, method, url_path, *args, **kwargs)
            except (httpx.TransportError, httpx.TimeoutException) as exc:
                last_exc = exc
                if attempt < retries:
                    time.sleep(_backoff(attempt))
                continue

            if response.status_code in _RETRYABLE_STATUSES and attempt < retries:
                time.sleep(_retry_after(response, attempt))
                continue

            if response.status_code >= 400:
                raise error_from_response(response)

            return response

        raise NetworkError(f'Request to {method} {url_path} failed after {attempts} attempts') from last_exc

    return wrapped


class HttpClient:
    def __init__(
        self,
        base_url: str,
        headers: dict[str, str],
        *,
        timeout: float = 30.0,
        retries: int = 3,
    ) -> None:
        self._retries = max(0, int(retries))
        self._http = httpx.Client(
            base_url=base_url,
            headers=headers,
            timeout=httpx.Timeout(timeout),
            event_hooks={'request': [self._strip_redirect_credentials]},
        )

    def _strip_redirect_credentials(self, request: httpx.Request) -> None:
        base = self._http.base_url
        if (request.url.scheme, request.url.host, request.url.port) == (base.scheme, base.host, base.port):
            return
        if request.url.scheme != 'https' or request.url.username or request.url.password:
            raise WikiClientError('File redirects must use HTTPS without credentials in the URL')
        # HTTPX removes Authorization across origins, but not custom TVM headers.
        # Leave redirect handling to HTTPX and strip API headers before sending.
        public_headers = {'accept', 'accept-encoding', 'connection', 'content-type', 'user-agent'}
        for name in self._http.headers:
            if name.lower() not in public_headers:
                request.headers.pop(name, None)
        request.headers.pop('authorization', None)
        request.headers.pop('cookie', None)

    def __enter__(self) -> 'HttpClient':
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def close(self) -> None:
        self._http.close()

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
    ) -> Any:
        response = self._request(method, path, params=params, json=json)
        if response.status_code == 204 or not response.content:
            return None
        return response.json()

    def send_bytes(
        self,
        method: str,
        path: str,
        content: bytes,
        *,
        params: dict[str, Any] | None = None,
        content_type: str = 'application/octet-stream',
    ) -> Any:
        response = self._request(
            method,
            path,
            params=params,
            content=content,
            headers={'Content-Type': content_type},
        )
        if response.status_code == 204 or not response.content:
            return None
        return response.json()

    def download(
        self,
        method: str,
        path: str,
        destination: str | Path,
        *,
        params: dict[str, Any] | None = None,
        max_bytes: int | None = None,
    ) -> None:
        url_path = path.lstrip('/')
        destination = Path(destination)

        self._download_once(method, url_path, destination, params, max_bytes)

    def _request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        url_path = path.lstrip('/')
        return self._request_once(method, url_path, **kwargs)

    @retry
    def _request_once(self, method: str, url_path: str, **kwargs: Any) -> httpx.Response:
        return self._http.request(method, url_path, **kwargs)

    @retry
    def _download_once(
        self,
        method: str,
        url_path: str,
        destination: Path,
        params: dict[str, Any] | None,
        max_bytes: int | None = None,
    ) -> httpx.Response:
        with self._http.stream(
            method,
            url_path,
            params=params,
            follow_redirects=True,
        ) as response:
            if response.status_code >= 400:
                response.read()
            else:
                _write_download(response, destination, max_bytes)
            return response


def _backoff(attempt: int) -> float:
    return min(0.5 * (2**attempt), _MAX_BACKOFF_SECONDS)


def _retry_after(response: httpx.Response, attempt: int) -> float:
    header = response.headers.get('Retry-After')
    if header:
        try:
            return max(0.0, float(header))
        except ValueError:
            pass
    return _backoff(attempt)
