"""Functional tests for Bills routes."""

import pytest


class TestBills:
    @pytest.mark.xfail(reason="May fail if no bills exist")
    def test_list_bills(self, client):
        response = client.bills.list_bills()
        assert response.status == "ok"
