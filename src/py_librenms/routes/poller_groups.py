"""Private async implementation for PollerGroups routes."""

from __future__ import annotations

from ..models.poller_groups import PollerGroupsResponse
from ._synchronicity import synchronizer
from ._types import ClientProtocol


class PollerGroups:
    """Async route namespace bound to a client transport."""

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client

    async def get_poller_group(
        self, poller_group: str | int | None = None
    ) -> PollerGroupsResponse:
        """Get a specific poller group or all poller groups if none is specified.

        Route: GET /api/v0/poller_group(/:poller_group)

        :param poller_group: Optional name or id of the poller group.
        """
        url = "/poller_group"
        if poller_group is not None:
            url += f"/{poller_group}"
        data = await self._client._get(url)
        return PollerGroupsResponse.model_validate(data)


PollerGroupsSync = synchronizer.wrap(
    PollerGroups, name="PollerGroupsSync", target_module=__name__
)
