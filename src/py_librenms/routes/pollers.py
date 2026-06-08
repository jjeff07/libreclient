"""Private async implementation for Pollers routes."""

from __future__ import annotations

from ..models.pollers import PollersResponse
from ._synchronicity import synchronizer
from ._types import ClientProtocol


class Pollers:
    """Async route namespace bound to a client transport."""

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client

    async def list_pollers(self) -> PollersResponse:
        """List all pollers in the system.

        Route: GET /api/v0/pollers
        """
        data = await self._client._get("/pollers")
        return PollersResponse.model_validate(data)

    async def list_poller_log(self, unpolled: bool = False) -> PollersResponse:
        """List all devices with polling information.

        Route: GET /api/v0/pollers/log

        :param unpolled: If True, filter to show only overdue devices.
        """
        params = {}
        if unpolled:
            params["unpolled"] = 1
        data = await self._client._get("/pollers/log", params=params)
        return PollersResponse.model_validate(data)


PollersSync = synchronizer.wrap(Pollers, name="PollersSync", target_module=__name__)
