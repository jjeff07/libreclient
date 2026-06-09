"""Response models for Port Groups routes."""

from __future__ import annotations

from pydantic import Field

from ._base import ListResponse


class PortGroupsResponse(ListResponse):
    """Response from get_port_groups."""

    data: list[dict] = Field(default_factory=list, validation_alias="groups")
