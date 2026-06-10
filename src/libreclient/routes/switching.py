"""Private async implementation for Switching routes."""

from __future__ import annotations

from ..models.switching import SwitchingResponse
from ._types import ClientProtocol


class Switching:
    """Async route namespace bound to a client transport."""

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client

    async def list_vlans(self) -> SwitchingResponse:
        """Get a list of all VLANs.

        Route: GET /api/v0/resources/vlans
        """
        data = await self._client._get("/resources/vlans")
        return SwitchingResponse.model_validate(data)

    async def get_vlans(self, hostname: str) -> SwitchingResponse:
        """Get a list of all VLANs for a given device.

        Route: GET /api/v0/devices/:hostname/vlans

        :param hostname: Device hostname or ID.
        """
        data = await self._client._get(f"/devices/{hostname}/vlans")
        return SwitchingResponse.model_validate(data)

    async def list_links(self) -> SwitchingResponse:
        """Get a list of all links.

        Route: GET /api/v0/resources/links
        """
        data = await self._client._get("/resources/links")
        return SwitchingResponse.model_validate(data)

    async def get_links(self, hostname: str) -> SwitchingResponse:
        """Get a list of links for a given device.

        Route: GET /api/v0/devices/:hostname/links
        :param hostname: Optional device hostname filter.
        """
        data = await self._client._get(f"/devices/{hostname}/links")
        return SwitchingResponse.model_validate(data)

    async def get_link(self, link_id: int) -> SwitchingResponse:
        """Retrieve a link by ID.

        Route: GET /api/v0/resources/links/:id

        :param link_id: Link ID.
        """
        data = await self._client._get(f"/resources/links/{link_id}")
        return SwitchingResponse.model_validate(data)

    async def list_fdb(self, mac: str | None = None) -> SwitchingResponse:
        """Get a list of all ports FDB, optionally filtered by MAC address.

        Route: GET /api/v0/resources/fdb(/:mac)

        :param mac: Optional MAC address filter.
        """
        url = "/resources/fdb"
        if mac is not None:
            url += f"/{mac}"
        data = await self._client._get(url)
        return SwitchingResponse.model_validate(data)

    async def list_fdb_detail(self, mac: str) -> SwitchingResponse:
        """Get a list of all ports FDB with human-readable device and interface names.

        Route: GET /api/v0/resources/fdb/:mac/detail
        :param mac: Optional MAC address filter.
        """
        data = await self._client._get(f"/resources/fdb/{mac}/detail")
        return SwitchingResponse.model_validate(data)

    async def list_nac(self, mac: str | None = None) -> SwitchingResponse:
        """Get a list of all ports NAC, optionally filtered by MAC address.

        Route: GET /api/v0/resources/nac(/:mac)
        :param mac: Optional MAC address filter.
        """
        url = "/resources/nac"
        if mac is not None:
            url += f"/{mac}"
        data = await self._client._get(url)
        return SwitchingResponse.model_validate(data)
