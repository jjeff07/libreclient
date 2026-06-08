"""ARP routes — async implementation."""

from __future__ import annotations

from ..models.arp import ArpResponse
from ._synchronicity import synchronizer
from ._types import ClientProtocol


class Arp:
    """ARP route namespace bound to a client transport."""

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client

    async def list_arp(self, query: str, device: str | None = None) -> ArpResponse:
        """Retrieve a specific ARP entry or all ARP entries for a device.

        Route: GET /api/v0/resources/ip/arp/:query

        :param query: An IP address, MAC address, CIDR network, or 'all' (requires device param).
        :param device: Hostname or device id; required when query is 'all'.
        """
        params = {}
        if device is not None:
            params["device"] = device
        data = await self._client._get(f"/resources/ip/arp/{query}", params=params)
        return ArpResponse.model_validate(data)


ArpSync = synchronizer.wrap(Arp, name="ArpSync", target_module=__name__)
