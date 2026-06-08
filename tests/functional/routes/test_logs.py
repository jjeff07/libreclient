"""Functional tests for Logs routes."""

import pytest


class TestLogs:
    @pytest.mark.xfail(reason="May fail if no event logs exist")
    def test_list_eventlog(self, client):
        response = client.logs.list_eventlog()
        assert response.status == "ok"

    @pytest.mark.xfail(reason="May fail if syslog not configured")
    def test_list_syslog(self, client):
        response = client.logs.list_syslog()
        assert response.status == "ok"

    @pytest.mark.xfail(reason="May fail if no alert logs exist")
    def test_list_alertlog(self, client):
        response = client.logs.list_alertlog()
        assert response.status == "ok"

    @pytest.mark.xfail(reason="May fail if no auth logs exist")
    def test_list_authlog(self, client):
        response = client.logs.list_authlog()
        assert response.status == "ok"
