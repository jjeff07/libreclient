"""Functional tests for ARP routes."""

import pytest


class TestArp:
    @pytest.mark.xfail(reason="May fail if no ARP entries exist")
    def test_list_arp(self, client):
        response = client.arp.list_arp("all")
        assert response.status == "ok"
