"""Functional tests for Devices routes."""

import pytest


class TestDevices:
    def test_list_devices(self, client):
        response = client.devices.list_devices()
        assert response.status == "ok"

    @pytest.mark.xfail(reason="May fail if no devices exist yet")
    def test_get_device(self, client):
        # Get first device from list
        devices = client.devices.list_devices()
        assert len(devices.data) > 0
        hostname = devices.data[0]["hostname"]
        response = client.devices.get_device(hostname)
        assert response.status == "ok"

    def test_list_sensors(self, client):
        response = client.devices.list_sensors()
        assert response.status == "ok"

    @pytest.mark.xfail(reason="May fail if no devices with Oxidized configured")
    def test_list_oxidized(self, client):
        response = client.devices.list_oxidized()
        assert isinstance(response, list)
