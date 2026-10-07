from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version('yandex-wiki-client')
except PackageNotFoundError:
    __version__ = '0+unknown'

from .client import WikiClient

__all__ = ['__version__', 'WikiClient']
