"""Unit tests for Devices response models."""

from libreclient.models.devices import (
    ComponentsResponse,
    DeviceFdbResponse,
    DevicePortsResponse,
    DeviceResponse,
    DevicesResponse,
)


class TestDevicesResponse:
    def test_devices_list(self) -> None:
        data = {
            "status": "ok",
            "message": "",
            "count": 1,
            "devices": [{"device_id": 1, "hostname": "router1"}],
        }
        r = DevicesResponse.model_validate(data)
        assert r.data[0]["hostname"] == "router1"

    def test_devices_defaults_empty(self) -> None:
        data = {"status": "ok", "message": "", "count": 0}
        r = DevicesResponse.model_validate(data)
        assert r.data == []


class TestDeviceResponse:
    def test_single_device(self) -> None:
        data = {
            "status": "ok",
            "message": "",
            "count": 1,
            "devices": [{"device_id": 1, "hostname": "sw1", "os": "linux"}],
        }
        r = DeviceResponse.model_validate(data)
        assert r.data[0]["os"] == "linux"


class TestDevicePortsResponse:
    def test_ports_list(self) -> None:
        data = {
            "status": "ok",
            "message": "",
            "count": 2,
            "ports": [
                {"port_id": 1, "ifName": "eth0"},
                {"port_id": 2, "ifName": "eth1"},
            ],
        }
        r = DevicePortsResponse.model_validate(data)
        assert len(r.data) == 2


class TestDeviceFdbResponse:
    def test_fdb_list(self) -> None:
        data = {
            "status": "ok",
            "message": "",
            "count": 1,
            "ports_fdb": [{"mac_address": "aa:bb:cc:dd:ee:ff", "port_id": 1}],
        }
        r = DeviceFdbResponse.model_validate(data)
        assert r.data[0]["mac_address"] == "aa:bb:cc:dd:ee:ff"


class TestComponentsResponse:
    def test_components_list(self) -> None:
        data = {
            "status": "ok",
            "message": "",
            "count": 1,
            "components": [{"id": 1, "type": "chassis", "label": "Main"}],
        }
        r = ComponentsResponse.model_validate(data)
        assert r.data[0]["label"] == "Main"
