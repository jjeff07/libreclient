"""Private async implementation for Routing routes."""

from __future__ import annotations

from typing import Literal

from ..models import ApiResponse
from ..models.routing import RoutingResponse
from ._synchronicity import synchronizer
from ._types import ClientProtocol, _compact


class Routing:
    """Async route namespace bound to a client transport."""

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client

    async def list_bgp(
        self,
        hostname: str | None = None,
        asn: int | None = None,
        remote_asn: int | None = None,
        remote_address: str | None = None,
        local_address: str | None = None,
        bgp_descr: str | None = None,
        bgp_state: str | None = None,
        bgp_adminstate: str | None = None,
        bgp_family: int | None = None,
    ) -> RoutingResponse:
        """List current BGP sessions.

        Route: GET /api/v0/bgp

        :param hostname: Optional filter by hostname.
        :param asn: Optional filter by ASN.
        :param remote_asn: Optional filter by remote ASN.
        :param remote_address: Optional filter by remote address.
        :param local_address: Optional filter by local address.
        :param bgp_descr: Optional filter by description.
        :param bgp_state: Optional filter by state.
        :param bgp_adminstate: Optional filter by admin state.
        :param bgp_family: Optional filter by address family.
        """
        params = _compact(
            hostname=hostname,
            asn=asn,
            remote_asn=remote_asn,
            remote_address=remote_address,
            local_address=local_address,
            bgp_descr=bgp_descr,
            bgp_state=bgp_state,
            bgp_adminstate=bgp_adminstate,
            bgp_family=bgp_family,
        )
        data = await self._client._get("/bgp", params=params)
        return RoutingResponse.model_validate(data)

    async def get_bgp(self, bgp_id: int) -> RoutingResponse:
        """Retrieve a BGP session by ID.

        Route: GET /api/v0/bgp/:id

        :param bgp_id: BGP session ID.
        """
        data = await self._client._get(f"/bgp/{bgp_id}")
        return RoutingResponse.model_validate(data)

    async def edit_bgp_descr(self, bgp_id: int, bgp_descr: str) -> ApiResponse:
        """Set the BGP session description by ID.

        Route: POST /api/v0/bgp/:id
        :param bgp_id: BGP session ID.
        :param bgp_descr: New description.
        """
        data = await self._client._post(f"/bgp/{bgp_id}", json={"bgp_descr": bgp_descr})
        return ApiResponse.model_validate(data)

    async def list_cbgp(self, hostname: str | None = None) -> RoutingResponse:
        """List current BGP session counters.

        Route: GET /api/v0/routing/bgp/cbgp
        :param hostname: Optional filter by hostname.
        """
        data = await self._client._get("/routing/bgp/cbgp", params=_compact(hostname=hostname))
        return RoutingResponse.model_validate(data)

    async def list_ip_addresses(
        self, address_family: Literal["ipv4", "ipv6"] | None = None
    ) -> RoutingResponse:
        """List all IPv4 and IPv6 (or version-specific) addresses.

        Route: GET /api/v0/resources/ip/addresses(/:address_family)

        :param address_family: Optional 'ipv4' or 'ipv6'.
        """
        url = "/resources/ip/addresses"
        if address_family is not None:
            url += f"/{address_family}"
        data = await self._client._get(url)
        return RoutingResponse.model_validate(data)

    async def get_network_ip_addresses(self, network_id: int) -> RoutingResponse:
        """Get all IPv4 and IPv6 addresses for a particular network.

        Route: GET /api/v0/resources/ip/networks/:id/ip

        :param network_id: Network ID.
        """
        data = await self._client._get(f"/resources/ip/networks/{network_id}/ip")
        return RoutingResponse.model_validate(data)

    async def list_ip_networks(
        self, address_family: Literal["ipv4", "ipv6"] | None = None
    ) -> RoutingResponse:
        """List all IPv4 and IPv6 (or version-specific) networks.

        Route: GET /api/v0/resources/ip/networks(/:address_family)

        :param address_family: Optional 'ipv4' or 'ipv6'.
        """
        url = "/resources/ip/networks"
        if address_family is not None:
            url += f"/{address_family}"
        data = await self._client._get(url)
        return RoutingResponse.model_validate(data)

    async def list_ipsec(self, hostname: str) -> RoutingResponse:
        """List the current active IPSec tunnels for a device.

        Route: GET /api/v0/routing/ipsec/data/:hostname
        :param hostname: Optional filter by hostname.
        """
        data = await self._client._get(f"/routing/ipsec/data/{hostname}")
        return RoutingResponse.model_validate(data)

    async def list_ospf(self, hostname: str | None = None) -> RoutingResponse:
        """List current OSPF neighbours.

        Route: GET /api/v0/ospf
        :param hostname: Optional filter by hostname.
        """
        data = await self._client._get("/ospf", params=_compact(hostname=hostname))
        return RoutingResponse.model_validate(data)

    async def list_ospf_ports(self) -> RoutingResponse:
        """List current OSPF ports.

        Route: GET /api/v0/ospf_ports
        """
        data = await self._client._get("/ospf_ports")
        return RoutingResponse.model_validate(data)

    async def list_ospfv3(self, hostname: str | None = None) -> RoutingResponse:
        """List current OSPFv3 neighbours.

        Route: GET /api/v0/ospfv3
        :param hostname: Optional filter by hostname.
        """
        data = await self._client._get("/ospfv3", params=_compact(hostname=hostname))
        return RoutingResponse.model_validate(data)

    async def list_ospfv3_ports(self, hostname: str | None = None) -> RoutingResponse:
        """List current OSPFv3 ports.

        Route: GET /api/v0/ospfv3_ports
        :param hostname: Optional filter by hostname.
        """
        data = await self._client._get("/ospfv3_ports", params=_compact(hostname=hostname))
        return RoutingResponse.model_validate(data)

    async def list_vrf(
        self, hostname: str | None = None, vrfname: str | None = None
    ) -> RoutingResponse:
        """List current VRFs.

        Route: GET /api/v0/routing/vrf(/:hostname)

        :param hostname: Optional filter by hostname. Cannot be combined with vrfname.
        :param vrfname: Optional filter by VRF name. Cannot be combined with hostname.
        :raises ValueError: If both hostname and vrfname are provided.
        """
        if hostname is not None and vrfname is not None:
            raise ValueError("hostname and vrfname cannot both be set")
        data = await self._client._get(
            "/routing/vrf", params=_compact(hostname=hostname, vrfname=vrfname)
        )
        return RoutingResponse.model_validate(data)

    async def get_vrf(self, vrf_id: int) -> RoutingResponse:
        """Retrieve a VRF by ID.

        Route: GET /api/v0/routing/vrf/:id

        :param vrf_id: VRF ID.
        """
        data = await self._client._get(f"/routing/vrf/{vrf_id}")
        return RoutingResponse.model_validate(data)

    async def list_mpls_services(self, hostname: str | None = None) -> RoutingResponse:
        """List MPLS services.

        Route: GET /api/v0/routing/mpls/services
        :param hostname: Optional filter by hostname.
        """
        data = await self._client._get("/routing/mpls/services", params=_compact(hostname=hostname))
        return RoutingResponse.model_validate(data)

    async def list_mpls_saps(self, hostname: str | None = None) -> RoutingResponse:
        """List MPLS SAPs.

        Route: GET /api/v0/routing/mpls/saps
        :param hostname: Optional filter by hostname.
        """
        data = await self._client._get("/routing/mpls/saps", params=_compact(hostname=hostname))
        return RoutingResponse.model_validate(data)


RoutingSync = synchronizer.wrap(Routing, name="RoutingSync", target_module=__name__)
