"""Response models for Routing routes."""

from __future__ import annotations

from pydantic import Field

from ._base import ListResponse


class RoutingResponse(ListResponse):
    """Response from routing list endpoints."""

    data: list[dict] = Field(default_factory=list, validation_alias="routing")
