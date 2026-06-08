"""Functional tests for Services routes."""

import pytest


class TestServices:
    @pytest.mark.xfail(reason="May fail if no services configured")
    def test_list_services(self, client):
        response = client.services.list_services()
        assert response.status == "ok"
