from __future__ import annotations

from .api.attachments import AttachmentApi
from .api.comments import CommentApi
from .api.grids import GridApi
from .api.operations import OperationApi
from .api.page_access import PageAccessApi
from .api.pages import PageApi
from .api.recovery_tokens import RecoveryTokenApi
from .api.search import SearchApi
from .api.spaces import SpaceApi
from .api.users import UserApi
from .exceptions import ConfigError
from .http import HttpClient
from . import __version__


class WikiClient:
    USER_AGENT: str = f'yandex-wiki-client/{__version__}'

    def __init__(
        self,
        *,
        oauth_token: str | None = None,
        iam_token: str | None = None,
        org_id: str | None = None,
        cloud_org_id: str | None = None,
        collab_org_id: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float = 30.0,
        retries: int = 3,
        base_url: str = 'https://api.wiki.yandex.net',
        api_prefix: str = 'v1',
    ) -> None:
        if headers is not None:
            request_headers = headers
        else:
            auth_header = self._build_auth_header(oauth_token, iam_token)
            org_header = self._build_org_header(
                org_id=org_id,
                cloud_org_id=cloud_org_id,
                collab_org_id=collab_org_id,
            )
            request_headers = {
                **auth_header,
                **org_header,
                'User-Agent': self.USER_AGENT,
                'Accept': 'application/json',
            }

        api_base_url = self._build_api_base_url(base_url, api_prefix)

        self.http = HttpClient(
            base_url=api_base_url,
            headers=request_headers,
            timeout=timeout,
            retries=retries,
        )

        self.pages = PageApi(self)
        self.page_access = PageAccessApi(self)
        self.attachments = AttachmentApi(self)
        self.comments = CommentApi(self)
        self.grids = GridApi(self)
        self.operations = OperationApi(self)
        self.recovery_tokens = RecoveryTokenApi(self)
        self.search = SearchApi(self)
        self.spaces = SpaceApi(self)
        self.users = UserApi(self)

    @staticmethod
    def _build_api_base_url(base_url: str, api_prefix: str) -> str:
        api_root = base_url.rstrip('/')
        if api_prefix:
            api_root += f'/{api_prefix.rstrip("/")}'
        return f'{api_root}/'

    @staticmethod
    def _build_auth_header(oauth_token: str | None, iam_token: str | None) -> dict[str, str]:
        if (oauth_token is None) == (iam_token is None):
            raise ConfigError('oauth_token or iam_token are mutually exclusive')
        if oauth_token is not None:
            return {'Authorization': f'OAuth {oauth_token}'}
        return {'Authorization': f'Bearer {iam_token}'}

    def _build_org_header(
        self,
        org_id: str | None,
        cloud_org_id: str | None,
        collab_org_id: str | None,
    ) -> dict[str, str]:
        if [org_id, cloud_org_id, collab_org_id].count(None) != 2:
            raise ConfigError('only one of org_id, cloud_org_id, collab_org_id must be provided')
        if org_id is not None:
            return {'X-Org-Id': str(org_id)}
        if cloud_org_id is not None:
            return {'X-Cloud-Org-Id': str(cloud_org_id)}
        return {'X-Collab-Org-Id': str(collab_org_id)}

    def __enter__(self) -> 'WikiClient':
        return self

    def close(self) -> None:
        self.http.close()

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
