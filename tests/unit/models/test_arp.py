"""Unit tests for ARP response models."""

from py_librenms.models.arp import ArpResponse


class TestArpResponse:
    def test_arp_list(self) -> None:
        data = {
            "status": "ok",
            "message": "",
            "count": 1,
            "arp": [{"ip": "10.0.0.1", "mac": "aa:bb:cc:dd:ee:ff"}],  # noqa: S1313
        }
        r = ArpResponse.model_validate(data)
        assert r.data[0]["ip"] == "10.0.0.1"  # noqa: S1313

    def test_arp_defaults_empty(self) -> None:
        data = {"status": "ok", "message": "", "count": 0}
        r = ArpResponse.model_validate(data)
        assert r.data == []
