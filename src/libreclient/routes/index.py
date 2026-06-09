"""Private async implementation for Index routes."""

from __future__ import annotations

from ..models.index import IndexResponse
from ._synchronicity import synchronizer
from ._types import ClientProtocol


class Index:
    """Async route namespace bound to a client transport."""

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client

    async def list_api_endpoints(self) -> IndexResponse:
        """Retrieve all available API route names and their URLs.

        Route: GET /api/v0
        """
        data = await self._client._get("")
        return IndexResponse(endpoints=data)


IndexSync = synchronizer.wrap(Index, name="IndexSync", target_module=__name__)
