"""Functional tests for Ports routes."""

import pytest


class TestPorts:
    @pytest.mark.xfail(reason="May fail if no ports exist")
    def test_get_all_ports(self, client):
        response = client.ports.get_all_ports()
        assert response.status == "ok"

    @pytest.mark.xfail(reason="May fail if no ports exist")
    def test_get_port_info(self, client):
        ports = client.ports.get_all_ports()
        assert len(ports.data) > 0
        port_id = ports.data[0]["port_id"]
        response = client.ports.get_port_info(port_id)
        assert response.status == "ok"

    @pytest.mark.xfail(reason="May fail if no ports exist")
    def test_get_port_ip_info(self, client):
        ports = client.ports.get_all_ports()
        assert len(ports.data) > 0
        port_id = ports.data[0]["port_id"]
        response = client.ports.get_port_ip_info(port_id)
        assert response.status == "ok"

    @pytest.mark.xfail(reason="May fail if no ports exist")
    def test_get_port_description(self, client):
        ports = client.ports.get_all_ports()
        assert len(ports.data) > 0
        port_id = ports.data[0]["port_id"]
        response = client.ports.get_port_description(port_id)
        assert response.status == "ok"
