"""Type definitions and utilities for route classes."""

from __future__ import annotations

import re
from typing import Any, Protocol

_DURATION_RE = re.compile(r"^\d{2,}:\d{2}$")
_START_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:00$")


class ClientProtocol(Protocol):
    """Structural type describing the transport methods routes depend on."""

    async def _get(self, path: str, **kwargs: Any) -> dict | list: ...
    async def _post(self, path: str, **kwargs: Any) -> dict: ...
    async def _put(self, path: str, **kwargs: Any) -> dict: ...
    async def _patch(self, path: str, **kwargs: Any) -> dict: ...
    async def _delete(self, path: str, **kwargs: Any) -> dict: ...
    async def _get_bytes(self, path: str, **kwargs: Any) -> bytes: ...


def _compact(**kwargs: Any) -> dict[str, Any]:
    """Return a dict with None values removed."""
    return {k: v for k, v in kwargs.items() if v is not None}


def _validate_maintenance_params(
    duration: str, start: str | None = None
) -> None:
    """Validate duration and start format for maintenance endpoints.

    :raises ValueError: If duration or start format is invalid.
    """
    if not _DURATION_RE.match(duration):
        raise ValueError(
            f"'duration' must be in 'HH:MM' format (e.g. '02:00'), got '{duration}'"
        )
    if start is not None and not _START_RE.match(start):
        raise ValueError(
            f"'start' must be in 'Y-m-d H:i:00' format (e.g. '2022-08-01 22:45:00'), got '{start}'"
        )


def _graph_params(
    from_time: str | None = None,
    to_time: str | None = None,
    width: int | None = None,
    height: int | None = None,
    **extra: Any,
) -> dict[str, Any]:
    """Build query params for graph endpoints, mapping Python names to API keys."""
    params: dict[str, Any] = {}
    if from_time is not None:
        params["from"] = from_time
    if to_time is not None:
        params["to"] = to_time
    if width is not None:
        params["width"] = width
    if height is not None:
        params["height"] = height
    for k, v in extra.items():
        if v is not None:
            params[k] = v
    return params
