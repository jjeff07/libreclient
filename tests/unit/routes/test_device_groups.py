"""Unit tests for Device Groups routes."""

import asyncio

from libreclient.models._base import ApiResponse
from libreclient.models.device_groups import (
    DeviceGroupDevicesResponse,
    DeviceGroupsResponse,
)
from libreclient.routes.device_groups import DeviceGroups


class TestGetDevicegroups:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "groups": [],
        }
        route = DeviceGroups(mock_client)
        result = asyncio.run(route.get_devicegroups())
        mock_client._get.assert_called_once_with("/devicegroups")
        assert isinstance(result, DeviceGroupsResponse)


class TestAddDevicegroup:
    def test_posts_payload(self, mock_client) -> None:
        mock_client._post.return_value = {"status": "ok", "message": "created"}
        route = DeviceGroups(mock_client)
        result = asyncio.run(
            route.add_devicegroup("Core", "static", devices=[1, 2])
        )
        mock_client._post.assert_called_once_with(
            "/devicegroups",
            json={"name": "Core", "type": "static", "devices": [1, 2]},
        )
        assert isinstance(result, ApiResponse)


class TestGetDevicesByGroup:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "devices": [],
        }
        route = DeviceGroups(mock_client)
        result = asyncio.run(route.get_devices_by_group("Core"))
        mock_client._get.assert_called_once_with(
            "/devicegroups/Core", params={}
        )
        assert isinstance(result, DeviceGroupDevicesResponse)

    def test_with_full_flag(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "devices": [],
        }
        route = DeviceGroups(mock_client)
        asyncio.run(route.get_devices_by_group("Core", full=True))
        mock_client._get.assert_called_once_with(
            "/devicegroups/Core", params={"full": 1}
        )


class TestDeleteDevicegroup:
    def test_calls_delete(self, mock_client) -> None:
        mock_client._delete.return_value = {
            "status": "ok",
            "message": "deleted",
        }
        route = DeviceGroups(mock_client)
        result = asyncio.run(route.delete_devicegroup("OldGroup"))
        mock_client._delete.assert_called_once_with("/devicegroups/OldGroup")
        assert isinstance(result, ApiResponse)
