"""Unit tests for Devices routes."""

import asyncio

from py_librenms.models._base import ApiResponse
from py_librenms.models.devices import (
    ComponentsResponse,
    DevicePortsResponse,
    DeviceResponse,
    DevicesResponse,
)
from py_librenms.routes.devices import Devices


class TestGetDevice:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 1,
            "devices": [],
        }
        route = Devices(mock_client)
        result = asyncio.run(route.get_device("router1"))
        mock_client._get.assert_called_once_with("/devices/router1")
        assert isinstance(result, DeviceResponse)


class TestDelDevice:
    def test_calls_delete(self, mock_client) -> None:
        mock_client._delete.return_value = {
            "status": "ok",
            "message": "removed",
        }
        route = Devices(mock_client)
        result = asyncio.run(route.del_device("old-switch"))
        mock_client._delete.assert_called_once_with("/devices/old-switch")
        assert isinstance(result, ApiResponse)


class TestListDevices:
    def test_no_params(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "devices": [],
        }
        route = Devices(mock_client)
        result = asyncio.run(route.list_devices())
        mock_client._get.assert_called_once_with("/devices", params={})
        assert isinstance(result, DevicesResponse)

    def test_with_type_filter(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "devices": [],
        }
        route = Devices(mock_client)
        asyncio.run(route.list_devices(type="active"))
        mock_client._get.assert_called_once_with(
            "/devices", params={"type": "active"}
        )


class TestAddDevice:
    def test_posts_payload(self, mock_client) -> None:
        mock_client._post.return_value = {"status": "ok", "message": "added"}
        route = Devices(mock_client)
        result = asyncio.run(
            route.add_device("newhost", snmpver="v2c", community="public")
        )
        mock_client._post.assert_called_once_with(
            "/devices",
            json={
                "hostname": "newhost",
                "snmpver": "v2c",
                "community": "public",
            },
        )
        assert isinstance(result, ApiResponse)


class TestGetDevicePorts:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "ports": [],
        }
        route = Devices(mock_client)
        result = asyncio.run(route.get_device_ports("sw1"))
        mock_client._get.assert_called_once_with(
            "/devices/sw1/ports", params={}
        )
        assert isinstance(result, DevicePortsResponse)


class TestGetComponents:
    def test_with_type_filter(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "components": [],
        }
        route = Devices(mock_client)
        result = asyncio.run(route.get_components("sw1", type="fan"))
        mock_client._get.assert_called_once_with(
            "/devices/sw1/components", params={"type": "fan"}
        )
        assert isinstance(result, ComponentsResponse)


class TestGetHealthGraph:
    def test_returns_bytes(self, mock_client) -> None:
        route = Devices(mock_client)
        result = asyncio.run(route.get_health_graph("sw1", "temperature"))
        mock_client._get_bytes.assert_called_once_with(
            "/devices/sw1/graphs/health/temperature"
        )
        assert isinstance(result, bytes)


class TestUpdateDeviceField:
    def test_patches_field(self, mock_client) -> None:
        mock_client._patch.return_value = {
            "status": "ok",
            "message": "updated",
        }
        route = Devices(mock_client)
        result = asyncio.run(
            route.update_device_field("sw1", "notes", "test note")
        )
        mock_client._patch.assert_called_once_with(
            "/devices/sw1", json={"field": "notes", "data": "test note"}
        )
        assert isinstance(result, ApiResponse)


class TestRenameDevice:
    def test_patches_rename(self, mock_client) -> None:
        mock_client._patch.return_value = {
            "status": "ok",
            "message": "renamed",
        }
        route = Devices(mock_client)
        result = asyncio.run(route.rename_device("old-name", "new-name"))
        mock_client._patch.assert_called_once_with(
            "/devices/old-name/rename/new-name"
        )
        assert isinstance(result, ApiResponse)
