"""Unit tests for Device Groups response models."""

from py_librenms.models.device_groups import (
    DeviceGroupDevicesResponse,
    DeviceGroupsResponse,
)


class TestDeviceGroupsResponse:
    def test_groups_list(self) -> None:
        data = {
            "status": "ok",
            "message": "",
            "count": 1,
            "groups": [{"id": 1, "name": "Core", "type": "dynamic"}],
        }
        r = DeviceGroupsResponse.model_validate(data)
        assert r.data[0]["name"] == "Core"


class TestDeviceGroupDevicesResponse:
    def test_devices_in_group(self) -> None:
        data = {
            "status": "ok",
            "message": "",
            "count": 2,
            "devices": [{"device_id": 1}, {"device_id": 2}],
        }
        r = DeviceGroupDevicesResponse.model_validate(data)
        assert len(r.data) == 2
