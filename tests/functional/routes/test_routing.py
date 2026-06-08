"""Functional tests for Routing routes."""

import pytest


class TestRouting:
    @pytest.mark.xfail(reason="May fail if no BGP sessions exist")
    def test_list_bgp(self, client):
        response = client.routing.list_bgp()
        assert response.status == "ok"

    @pytest.mark.xfail(reason="May fail if no OSPF configured")
    def test_list_ospf(self, client):
        response = client.routing.list_ospf()
        assert response.status == "ok"

    @pytest.mark.xfail(reason="May fail if no VRFs exist")
    def test_list_vrf(self, client):
        response = client.routing.list_vrf()
        assert response.status == "ok"

    @pytest.mark.xfail(reason="May fail if no IP addresses exist")
    def test_list_ip_addresses(self, client):
        response = client.routing.list_ip_addresses()
        assert response.status == "ok"

    @pytest.mark.xfail(reason="May fail if no IP networks exist")
    def test_list_ip_networks(self, client):
        response = client.routing.list_ip_networks()
        assert response.status == "ok"

    @pytest.mark.xfail(reason="May fail if no OSPF ports exist")
    def test_list_ospf_ports(self, client):
        response = client.routing.list_ospf_ports()
        assert response.status == "ok"
