"""Functional tests for Inventory routes."""

import pytest


class TestInventory:
    @pytest.mark.xfail(reason="Requires a device hostname")
    def test_get_inventory(self, client):
        devices = client.devices.list_devices()
        assert len(devices.data) > 0
        hostname = devices.data[0]["hostname"]
        response = client.inventory.get_inventory(hostname)
        assert response.status == "ok"
