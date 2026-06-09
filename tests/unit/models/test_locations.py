"""Unit tests for Locations response models."""

from libreclient.models.locations import LocationsResponse


class TestLocationsResponse:
    def test_locations_list(self) -> None:
        data = {
            "status": "ok",
            "message": "",
            "count": 1,
            "locations": [
                {"id": 1, "location": "DC1", "lat": 40.0, "lng": -74.0}
            ],
        }
        r = LocationsResponse.model_validate(data)
        assert r.data[0]["location"] == "DC1"
