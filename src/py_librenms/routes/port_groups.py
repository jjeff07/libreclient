"""Private async implementation for PortGroups routes."""

from __future__ import annotations

from ..models import ApiResponse
from ..models.port_groups import PortGroupsResponse
from ._synchronicity import synchronizer
from ._types import ClientProtocol, _compact


class PortGroups:
    """Async route namespace bound to a client transport."""

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client

    async def get_port_groups(self) -> PortGroupsResponse:
        """List all port groups.

        Route: GET /api/v0/port_groups
        """
        data = await self._client._get("/port_groups")
        return PortGroupsResponse.model_validate(data)

    async def get_ports_by_group(
        self, name: str, full: bool = False
    ) -> PortGroupsResponse:
        """List all ports matching the given group.

        Route: GET /api/v0/port_groups/:name

        :param name: Port group name.
        :param full: If True, return full port data.
        """
        params = {}
        if full:
            params["full"] = 1
        data = await self._client._get(f"/port_groups/{name}", params=params)
        return PortGroupsResponse.model_validate(data)

    async def add_port_group(
        self, name: str, desc: str | None = None
    ) -> ApiResponse:
        """Add a new port group.

        Route: POST /api/v0/port_groups

        :param desc: Optional description.
        :param name: Name for the port group.
        """
        payload: dict = {"name": name, **_compact(desc=desc)}
        data = await self._client._post("/port_groups", json=payload)
        return ApiResponse.model_validate(data)

    async def assign_port_group(
        self, port_group_id: int, port_ids: list[str]
    ) -> ApiResponse:
        """Assign a port group to a list of ports.

        Route: POST /api/v0/port_groups/:port_group_id/assign

        :param port_group_id: Port group ID.
        :param port_ids: List of port IDs to assign.
        """
        data = await self._client._post(
            f"/port_groups/{port_group_id}/assign", json={"port_ids": port_ids}
        )
        return ApiResponse.model_validate(data)

    async def remove_port_group(
        self, port_group_id: int, port_ids: list[str]
    ) -> ApiResponse:
        """Remove a port group from a list of ports.

        Route: POST /api/v0/port_groups/:port_group_id/remove
        :param port_group_id: Port group ID.
        :param port_ids: List of port IDs to remove.
        """
        data = await self._client._post(
            f"/port_groups/{port_group_id}/remove", json={"port_ids": port_ids}
        )
        return ApiResponse.model_validate(data)


PortGroupsSync = synchronizer.wrap(
    PortGroups, name="PortGroupsSync", target_module=__name__
)
