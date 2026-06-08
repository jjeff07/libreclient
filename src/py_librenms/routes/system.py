"""Private async implementation for System routes."""

from __future__ import annotations

from ..models import ApiResponse
from ..models.system import SystemResponse
from ._synchronicity import synchronizer
from ._types import ClientProtocol


class System:
    """Async route namespace bound to a client transport."""

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client

    async def ping(self) -> ApiResponse:
        """Simple endpoint to check API availability.

        Route: GET /api/v0/ping
        """
        data = await self._client._get("/ping")
        return ApiResponse.model_validate(data)

    async def system(self) -> SystemResponse:
        """Display LibreNMS instance information.

        Route: GET /api/v0/system
        """
        data = await self._client._get("/system")
        return SystemResponse.model_validate(data)


SystemSync = synchronizer.wrap(System, name="SystemSync", target_module=__name__)
