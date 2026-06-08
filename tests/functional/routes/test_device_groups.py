"""Functional tests for DeviceGroups routes."""

import pytest


class TestDeviceGroups:
    @pytest.mark.xfail(reason="May fail if no device groups exist")
    def test_get_devicegroups(self, client):
        response = client.device_groups.get_devicegroups()
        assert response.status == "ok"

    @pytest.mark.xfail(reason="May fail if no device groups exist")
    def test_get_devices_by_group(self, client):
        groups = client.device_groups.get_devicegroups()
        assert len(groups.data) > 0
        name = groups.data[0]["name"]
        response = client.device_groups.get_devices_by_group(name)
        assert response.status == "ok"
