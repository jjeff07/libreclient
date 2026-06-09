"""Unit tests for Ports routes."""

import asyncio

from libreclient.models._base import ApiResponse
from libreclient.models.ports import PortResponse, PortsResponse
from libreclient.routes.ports import Ports


class TestGetAllPorts:
    def test_no_params(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "ports": [],
        }
        route = Ports(mock_client)
        result = asyncio.run(route.get_all_ports())
        mock_client._get.assert_called_once_with("/ports", params={})
        assert isinstance(result, PortsResponse)

    def test_with_columns(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "ports": [],
        }
        route = Ports(mock_client)
        asyncio.run(route.get_all_ports(columns="ifName,ifAlias"))
        mock_client._get.assert_called_once_with(
            "/ports", params={"columns": "ifName,ifAlias"}
        )


class TestSearchPorts:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "ports": [],
        }
        route = Ports(mock_client)
        result = asyncio.run(route.search_ports("ifAlias", "uplink"))
        mock_client._get.assert_called_once_with(
            "/ports/search/ifAlias/uplink", params={}
        )
        assert isinstance(result, PortsResponse)


class TestGetPortInfo:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 1,
            "ports": [],
        }
        route = Ports(mock_client)
        result = asyncio.run(route.get_port_info(42))
        mock_client._get.assert_called_once_with("/ports/42", params={})
        assert isinstance(result, PortResponse)


class TestUpdatePortDescription:
    def test_patches_description(self, mock_client) -> None:
        mock_client._patch.return_value = {
            "status": "ok",
            "message": "updated",
        }
        route = Ports(mock_client)
        result = asyncio.run(route.update_port_description(10, "new desc"))
        mock_client._patch.assert_called_once_with(
            "/ports/10/description", json={"description": "new desc"}
        )
        assert isinstance(result, ApiResponse)
