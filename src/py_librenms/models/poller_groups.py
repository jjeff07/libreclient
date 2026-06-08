"""Response models for Poller Groups routes."""

from __future__ import annotations

from pydantic import Field

from ._base import ListResponse


class PollerGroupsResponse(ListResponse):
    """Response from get_poller_groups."""

    data: list[dict] = Field(default_factory=list, validation_alias="get_poller_group")
