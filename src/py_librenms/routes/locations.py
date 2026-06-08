"""Private async implementation for Locations routes."""

from __future__ import annotations

from ..models import ApiResponse
from ..models.locations import LocationsResponse
from ._synchronicity import synchronizer
from ._types import ClientProtocol, _compact, _validate_maintenance_params


class Locations:
    """Async route namespace bound to a client transport."""

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client

    async def list_locations(self) -> LocationsResponse:
        """Return a list of locations.

        Route: GET /api/v0/resources/locations
        """
        data = await self._client._get("/resources/locations")
        return LocationsResponse.model_validate(data)

    async def add_location(
        self,
        location: str,
        lat: float | None = None,
        lng: float | None = None,
        fixed_coordinates: int | None = None,
    ) -> ApiResponse:
        """Add a new location.

        Route: POST /api/v0/locations

        :param location: Location name.
        :param lat: Optional latitude.
        :param lng: Optional longitude.
        :param fixed_coordinates: Optional, if True lock coordinates.
        """
        payload: dict = {
            "location": location,
            **_compact(lat=lat, lng=lng, fixed_coordinates=fixed_coordinates),
        }
        data = await self._client._post("/locations", json=payload)
        return ApiResponse.model_validate(data)

    async def delete_location(self, location: str) -> ApiResponse:
        """Delete an existing location.

        Route: DELETE /api/v0/locations/:location

        :param location: Name or id of the location to delete.
        """
        data = await self._client._delete(f"/locations/{location}")
        return ApiResponse.model_validate(data)

    async def edit_location(
        self, location: str, lat: float | None = None, lng: float | None = None
    ) -> ApiResponse:
        """Edit a location.

        Route: PATCH /api/v0/locations/:location
        :param location: Location name to edit.
        :param lat: Optional new latitude.
        :param lng: Optional new longitude.
        """
        payload = _compact(lat=lat, lng=lng)
        data = await self._client._patch(f"/locations/{location}", json=payload)
        return ApiResponse.model_validate(data)

    async def get_location(self, location: str) -> LocationsResponse:
        """Get a specific location.

        Route: GET /api/v0/location/:location
        :param location: Location name.
        """
        data = await self._client._get(f"/location/{location}")
        return LocationsResponse.model_validate(data)

    async def maintenance_location(
        self,
        location: str,
        duration: str,
        title: str | None = None,
        notes: str | None = None,
        start: str | None = None,
        behavior: int | None = None,
    ) -> ApiResponse:
        """Set a location into maintenance mode.

        Route: POST /api/v0/locations/:location/maintenance

        :param duration: Duration in 'H:i' format (required).
        :param title: Optional title.
        :param notes: Optional notes.
        :param start: Optional start time in 'Y-m-d H:i:00' format.
        :param behavior: Optional maintenance behavior id.
        :param location: Location name.
        :raises ValueError: If duration or start format is invalid.
        """
        _validate_maintenance_params(duration, start)
        payload: dict = {
            "duration": duration,
            **_compact(title=title, notes=notes, start=start, behavior=behavior),
        }
        data = await self._client._post(f"/locations/{location}/maintenance", json=payload)
        return ApiResponse.model_validate(data)


LocationsSync = synchronizer.wrap(Locations, name="LocationsSync", target_module=__name__)
