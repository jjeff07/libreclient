"""Unit tests for Locations routes."""

import asyncio

from libreclient.models._base import ApiResponse
from libreclient.models.locations import LocationsResponse
from libreclient.routes.locations import Locations


class TestListLocations:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "locations": [],
        }
        route = Locations(mock_client)
        result = asyncio.run(route.list_locations())
        mock_client._get.assert_called_once_with("/resources/locations")
        assert isinstance(result, LocationsResponse)


class TestAddLocation:
    def test_posts_payload(self, mock_client) -> None:
        mock_client._post.return_value = {"status": "ok", "message": "created"}
        route = Locations(mock_client)
        result = asyncio.run(route.add_location("DC1", lat=40.0, lng=-74.0))
        mock_client._post.assert_called_once_with(
            "/locations", json={"location": "DC1", "lat": 40.0, "lng": -74.0}
        )
        assert isinstance(result, ApiResponse)


class TestDeleteLocation:
    def test_calls_delete(self, mock_client) -> None:
        mock_client._delete.return_value = {
            "status": "ok",
            "message": "deleted",
        }
        route = Locations(mock_client)
        result = asyncio.run(route.delete_location("DC1"))
        mock_client._delete.assert_called_once_with("/locations/DC1")
        assert isinstance(result, ApiResponse)


class TestGetLocation:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "locations": [],
        }
        route = Locations(mock_client)
        result = asyncio.run(route.get_location("DC1"))
        mock_client._get.assert_called_once_with("/location/DC1")
        assert isinstance(result, LocationsResponse)
