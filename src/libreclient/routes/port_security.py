"""Private async implementation for PortSecurity routes."""

from __future__ import annotations

from ..models.port_security import PortSecurityResponse
from ._synchronicity import synchronizer
from ._types import ClientProtocol


class PortSecurity:
    """Async route namespace bound to a client transport."""

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client

    async def get_all_port_security(self) -> PortSecurityResponse:
        """Get all port security info across all ports.

        Route: GET /api/v0/port_security
        """
        data = await self._client._get("/port_security")
        return PortSecurityResponse.model_validate(data)

    async def get_port_security_by_port(
        self, port_id: int
    ) -> PortSecurityResponse:
        """Get port security info for a specific port.

        Route: GET /api/v0/port_security/port/:port_id

        :param port_id: Port ID.
        """
        data = await self._client._get(f"/port_security/port/{port_id}")
        return PortSecurityResponse.model_validate(data)

    async def get_port_security_by_hostname(
        self, hostname: str
    ) -> PortSecurityResponse:
        """Get port security info for all ports on a device.

        Route: GET /api/v0/port_security/device/:hostname

        :param hostname: Device hostname or ID.
        """
        data = await self._client._get(f"/port_security/device/{hostname}")
        return PortSecurityResponse.model_validate(data)


PortSecuritySync = synchronizer.wrap(
    PortSecurity, name="PortSecuritySync", target_module=__name__
)
