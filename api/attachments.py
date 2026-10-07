from __future__ import annotations
import contextlib
from pathlib import Path
from typing import Iterator

from .base import BaseApi
from ..models.attachments import Attachment
from ..models.pagination import CursorPage
from ..utils import exclude_none

PART_SIZE = 5 * 1024 * 1024  # 5 MB


class AttachmentApi(BaseApi):
    def get(self, page_id: int, file_id: int) -> Attachment:
        data = self._request('GET', f'pages/{page_id}/attachments/{file_id}')
        return self._parse(Attachment, data)

    def list(
        self,
        page_id: int,
        *,
        order_by: str | None = None,
        order_direction: str | None = None,
    ) -> list[Attachment]:
        return list(self.iter_attachments(page_id, order_by=order_by, order_direction=order_direction))

    def iter_attachments(
        self,
        page_id: int,
        *,
        order_by: str | None = None,
        order_direction: str | None = None,
    ) -> Iterator[Attachment]:
        params = exclude_none(order_by=order_by, order_direction=order_direction)
        return self._iter_paginated_collection(
            'GET',
            f'pages/{page_id}/attachments',
            Attachment,
            params=params or None,
        )

    def list_page(
        self,
        page_id: int,
        *,
        order_by: str | None = None,
        order_direction: str | None = None,
        page_size: int | None = None,
        cursor: str | None = None,
    ) -> CursorPage[Attachment]:
        params = exclude_none(
            order_by=order_by,
            order_direction=order_direction,
            page_size=page_size,
            cursor=cursor,
        )
        return self._list_paginated_collection_page(
            'GET',
            f'pages/{page_id}/attachments',
            Attachment,
            params=params or None,
        )

    def download_by_url(self, url: str, destination: str | Path) -> None:
        self._client.http.download(
            'GET',
            'pages/attachments/download_by_url',
            destination,
            params={'url': url.lstrip('/'), 'download': True},
        )

    def download_by_id(self, page_id: int, file_id: int, destination: str | Path) -> None:
        self._client.http.download('GET', f'pages/{page_id}/attachments/{file_id}/download', destination)

    def download_preview(self, page_id: int, file_id: int, destination: str | Path) -> None:
        self._client.http.download('GET', f'pages/{page_id}/attachments/{file_id}/preview', destination)

    def upload(self, page_id: int, file_path: str | Path, *, file_name: str | None = None) -> Attachment:
        session_id = self._upload_file(Path(file_path), file_name=file_name)
        result = self._request(
            'POST',
            f'pages/{page_id}/attachments',
            json={'upload_sessions': [session_id]},
        )
        return self._parse(Attachment, result['results'][0])

    def delete(self, page_id: int, file_id: int) -> None:
        self._request('DELETE', f'pages/{page_id}/attachments/{file_id}')

    def _upload_file(self, file_path: Path, *, file_name: str | None = None) -> str:
        file_size = file_path.stat().st_size
        file_name = file_name or file_path.name
        session = self._request(
            'POST',
            'upload_sessions',
            json={'file_name': file_name, 'file_size': file_size},
        )
        session_id = session['session_id']

        try:
            with open(file_path, 'rb') as f:
                part_number = 1
                while chunk := f.read(PART_SIZE):
                    self._client.http.send_bytes(
                        'PUT',
                        f'upload_sessions/{session_id}/upload_part',
                        chunk,
                        params={'part_number': part_number},
                    )
                    part_number += 1
        except Exception:
            with contextlib.suppress(Exception):
                self._request('POST', f'upload_sessions/{session_id}/abort')
            raise

        self._request('POST', f'upload_sessions/{session_id}/finish')
        return session_id
