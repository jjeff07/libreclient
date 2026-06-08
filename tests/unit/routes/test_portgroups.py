"""Unit tests for Portgroups routes."""

import asyncio

from py_librenms.routes.portgroups import Portgroups


class TestGetGraphByPortgroup:
    def test_returns_bytes(self, mock_client) -> None:
        route = Portgroups(mock_client)
        result = asyncio.run(route.get_graph_by_portgroup("transit"))
        mock_client._get_bytes.assert_called_once_with("/portgroups/transit", params={})
        assert isinstance(result, bytes)

    def test_with_params(self, mock_client) -> None:
        route = Portgroups(mock_client)
        asyncio.run(route.get_graph_by_portgroup("peering", width=800, height=300))
        mock_client._get_bytes.assert_called_once_with(
            "/portgroups/peering", params={"width": 800, "height": 300}
        )


class TestGetGraphByPortgroupMultiportBits:
    def test_returns_bytes(self, mock_client) -> None:
        route = Portgroups(mock_client)
        result = asyncio.run(route.get_graph_by_portgroup_multiport_bits("1,2,3"))
        mock_client._get_bytes.assert_called_once_with(
            "/portgroups/multiport/bits/1,2,3", params={}
        )
        assert isinstance(result, bytes)
