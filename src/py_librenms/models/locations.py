"""Response models for Locations routes."""

from __future__ import annotations

from pydantic import Field

from ._base import ListResponse


class LocationsResponse(ListResponse):
    """Response from list_locations."""

    data: list[dict] = Field(default_factory=list, validation_alias="locations")
