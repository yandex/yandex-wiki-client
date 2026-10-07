from typing import Any, Final

NOT_SET: Final[Any] = object()


def exclude_none(**values: Any) -> dict[str, Any]:
    return {key: value for key, value in values.items() if value is not None}


def exclude_not_set(**values: Any) -> dict[str, Any]:
    return {key: value for key, value in values.items() if value is not NOT_SET}
