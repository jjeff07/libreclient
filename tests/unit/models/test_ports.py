"""Unit tests for Ports response models."""

from libreclient.models.ports import PortsResponse


class TestPortsResponse:
    def test_ports_list(self) -> None:
        data = {
            "status": "ok",
            "message": "",
            "count": 1,
            "ports": [{"port_id": 1, "ifName": "eth0"}],
        }
        r = PortsResponse.model_validate(data)
        assert r.data[0]["ifName"] == "eth0"

    def test_ports_defaults_empty(self) -> None:
        data = {"status": "ok", "message": "", "count": 0}
        r = PortsResponse.model_validate(data)
        assert r.data == []
