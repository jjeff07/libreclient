"""Unit tests for Port Groups routes."""

import asyncio

from py_librenms.models._base import ApiResponse
from py_librenms.models.port_groups import PortGroupsResponse
from py_librenms.routes.port_groups import PortGroups


class TestGetPortGroups:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {"status": "ok", "message": "", "count": 0, "groups": []}
        route = PortGroups(mock_client)
        result = asyncio.run(route.get_port_groups())
        mock_client._get.assert_called_once_with("/port_groups")
        assert isinstance(result, PortGroupsResponse)


class TestAddPortGroup:
    def test_posts_payload(self, mock_client) -> None:
        mock_client._post.return_value = {"status": "ok", "message": "created"}
        route = PortGroups(mock_client)
        result = asyncio.run(route.add_port_group("Uplinks", desc="Uplink ports"))
        mock_client._post.assert_called_once_with(
            "/port_groups", json={"name": "Uplinks", "desc": "Uplink ports"}
        )
        assert isinstance(result, ApiResponse)


class TestAssignPortGroup:
    def test_posts_port_ids(self, mock_client) -> None:
        mock_client._post.return_value = {"status": "ok", "message": "assigned"}
        route = PortGroups(mock_client)
        result = asyncio.run(route.assign_port_group(1, [10, 20, 30]))
        mock_client._post.assert_called_once_with(
            "/port_groups/1/assign", json={"port_ids": [10, 20, 30]}
        )
        assert isinstance(result, ApiResponse)
