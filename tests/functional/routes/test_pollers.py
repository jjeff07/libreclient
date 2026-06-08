"""Functional tests for Pollers routes."""

import pytest


class TestPollers:
    @pytest.mark.xfail(reason="May fail if no pollers configured")
    def test_list_pollers(self, client):
        response = client.pollers.list_pollers()
        assert response.status == "ok"

    @pytest.mark.xfail(reason="May fail if no poller log entries")
    def test_list_poller_log(self, client):
        response = client.pollers.list_poller_log()
        assert response.status == "ok"
