"""Private async implementation for Ports routes."""

from __future__ import annotations

from typing import Literal

from ..models import ApiResponse
from ..models.ports import (
    PortDescriptionResponse,
    PortIpResponse,
    PortResponse,
    PortsResponse,
    PortTransceiverResponse,
)
from ._synchronicity import synchronizer
from ._types import ClientProtocol


class Ports:
    """Async route namespace bound to a client transport."""

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client

    async def get_all_ports(self, columns: str | None = None) -> PortsResponse:
        """Get info for all ports on all devices.

        Route: GET /api/v0/ports

        :param columns: Comma-separated list of columns to return.
        """
        params = {}
        if columns is not None:
            params["columns"] = columns
        data = await self._client._get("/ports", params=params)
        return PortsResponse.model_validate(data)

    async def search_ports(
        self, field: str, search: str, columns: str | None = None
    ) -> PortsResponse:
        """Search for ports matching the query.

        Route: GET /api/v0/ports/search/:field/:search

        :param field: Field to search.
        :param search: Search value.
        :param columns: Optional comma-separated columns to return.
        """
        params = {}
        if columns is not None:
            params["columns"] = columns
        data = await self._client._get(
            f"/ports/search/{field}/{search}", params=params
        )
        return PortsResponse.model_validate(data)

    async def ports_with_associated_mac(
        self, mac: str, filter: str | None = None
    ) -> PortResponse:
        """Search for ports matching a MAC address.

        Route: GET /api/v0/ports/mac/:search

        :param mac: MAC address to search.
        :param filter: Optional filter.
        """
        params = {}
        if filter is not None:
            params["filter"] = filter
        data = await self._client._get(f"/ports/mac/{mac}", params=params)
        return PortResponse.model_validate(data)

    async def get_port_info(
        self,
        port_id: int,
        with_relations: Literal["vlans", "device", "statistics"] | None = None,
    ) -> PortResponse:
        """Get all info for a particular port.

        Route: GET /api/v0/ports/:portid

        :param port_id: Port ID.
        :param with_relations: Optional, include relations.
        """
        params = {}
        if with_relations is not None:
            params["with"] = with_relations
        data = await self._client._get(f"/ports/{port_id}", params=params)
        return PortResponse.model_validate(data)

    async def get_port_ip_info(self, port_id: int) -> PortIpResponse:
        """Get all IP info (v4 and v6) for a given port id.

        Route: GET /api/v0/ports/:portid/ip
        :param port_id: Port ID.
        """
        data = await self._client._get(f"/ports/{port_id}/ip")
        return PortIpResponse.model_validate(data)

    async def get_port_transceiver(
        self, port_id: int
    ) -> PortTransceiverResponse:
        """Get transceiver info with metrics for a port.

        Route: GET /api/v0/ports/:portid/transceiver
        :param port_id: Port ID.
        """
        data = await self._client._get(f"/ports/{port_id}/transceiver")
        return PortTransceiverResponse.model_validate(data)

    async def get_port_description(
        self, port_id: int
    ) -> PortDescriptionResponse:
        """Get the description (ifAlias) for a given port id.

        Route: GET /api/v0/ports/:portid/description
        :param port_id: Port ID.
        """
        data = await self._client._get(f"/ports/{port_id}/description")
        return PortDescriptionResponse.model_validate(data)

    async def update_port_description(
        self, port_id: int, description: str
    ) -> ApiResponse:
        """Change the description (ifAlias) for a given port id.

        Route: PATCH /api/v0/ports/:portid/description

        :param description: New port description. Send empty string to reset to default.
        :param port_id: Port ID.
        """
        data = await self._client._patch(
            f"/ports/{port_id}/description", json={"description": description}
        )
        return ApiResponse.model_validate(data)


PortsSync = synchronizer.wrap(Ports, name="PortsSync", target_module=__name__)
