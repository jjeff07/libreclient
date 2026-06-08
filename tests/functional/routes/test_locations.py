"""Functional tests for Locations routes."""

import pytest


class TestLocations:
    def test_list_locations(self, client):
        response = client.locations.list_locations()
        assert response.status == "ok"

    @pytest.mark.xfail(reason="May fail if no locations exist")
    def test_get_location(self, client):
        locations = client.locations.list_locations()
        assert len(locations.data) > 0
        loc = locations.data[0]["location"]
        response = client.locations.get_location(loc)
        assert response.status == "ok"
