"""Private async implementation for Portgroups routes."""

from __future__ import annotations

from ._types import ClientProtocol, _graph_params


class Portgroups:
    """Async route namespace bound to a client transport."""

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client

    async def get_graph_by_portgroup(
        self,
        group: str,
        from_time: str | None = None,
        to_time: str | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> bytes:
        """Get a graph based on a port group type (e.g. Transit, Peering).

        Route: GET /api/v0/portgroups/:group

        :param group: Port group type(s), comma-separated (e.g. 'transit,peering').
        :param from_time: Start time.
        :param to_time: End time.
        :param width: Graph width in pixels.
        :param height: Graph height in pixels.
        """
        params = _graph_params(from_time, to_time, width, height)
        return await self._client._get_bytes(
            f"/portgroups/{group}", params=params
        )

    async def get_graph_by_portgroup_multiport_bits(
        self,
        port_ids: str,
        from_time: str | None = None,
        to_time: str | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> bytes:
        """Get a graph based on multiple port ids.

        Route: GET /api/v0/portgroups/multiport/bits/:id

        :param port_ids: Comma-separated list of port ids (e.g. '1,2,3').
        :param from_time: Start time.
        :param to_time: End time.
        :param width: Graph width in pixels.
        :param height: Graph height in pixels.
        """
        params = _graph_params(from_time, to_time, width, height)
        return await self._client._get_bytes(
            f"/portgroups/multiport/bits/{port_ids}", params=params
        )
