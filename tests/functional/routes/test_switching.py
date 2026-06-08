"""Functional tests for Switching routes."""

import pytest


class TestSwitching:
    @pytest.mark.xfail(reason="May fail if no VLANs exist")
    def test_list_vlans(self, client):
        response = client.switching.list_vlans()
        assert response.status == "ok"

    @pytest.mark.xfail(reason="May fail if no links exist")
    def test_list_links(self, client):
        response = client.switching.list_links()
        assert response.status == "ok"

    @pytest.mark.xfail(reason="May fail if no FDB entries exist")
    def test_list_fdb(self, client):
        response = client.switching.list_fdb()
        assert response.status == "ok"

    @pytest.mark.xfail(reason="May fail if no NAC entries exist")
    def test_list_nac(self, client):
        response = client.switching.list_nac()
        assert response.status == "ok"
