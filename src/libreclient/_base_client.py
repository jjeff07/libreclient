"""Shared base client functionality for sync/async LibreNMS clients."""

from __future__ import annotations

import inspect
from abc import ABC, abstractmethod
from typing import Any, cast

from .config import LibreConfig


class BaseLibreClient(LibreConfig, ABC):
    """Common transport helpers used by both sync and async clients.

    Route namespaces implemented as async code can call these methods and work
    with either concrete client implementation.
    """

    def _api_url(self, path: str) -> str:
        suffix = path if path.startswith("/") else f"/{path}"
        return f"{self.base_url}{suffix}"

    @abstractmethod
    async def _request_raw(self, method: str, url: str, **kwargs: Any) -> Any:
        """Execute one HTTP request and return the raw response object."""

    async def _request(
        self, method: str, path: str, **kwargs: Any
    ) -> dict | list:
        response = await self._request_raw(
            method, self._api_url(path), **kwargs
        )
        response.raise_for_status()
        return await _json_from_response(response)

    async def _request_bytes(
        self, method: str, path: str, **kwargs: Any
    ) -> bytes:
        response = await self._request_raw(
            method, self._api_url(path), **kwargs
        )
        response.raise_for_status()
        payload = response.content
        if inspect.isawaitable(payload):
            payload = await payload
        return cast("bytes", payload)

    async def _get(self, path: str, **kwargs: Any) -> dict | list:
        return await self._request("GET", path, **kwargs)

    async def _post(self, path: str, **kwargs: Any) -> dict:
        return await self._request("POST", path, **kwargs)

    async def _put(self, path: str, **kwargs: Any) -> dict:
        return await self._request("PUT", path, **kwargs)

    async def _patch(self, path: str, **kwargs: Any) -> dict:
        return await self._request("PATCH", path, **kwargs)

    async def _delete(self, path: str, **kwargs: Any) -> dict:
        return await self._request("DELETE", path, **kwargs)

    async def _get_bytes(self, path: str, **kwargs: Any) -> bytes:
        return await self._request_bytes("GET", path, **kwargs)


async def _json_from_response(response: Any) -> dict | list:
    """Normalize niquests response.json() for sync/async response types."""
    payload = response.json()
    if inspect.isawaitable(payload):
        payload = await payload
    return cast("dict", payload)
