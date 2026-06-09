"""Response models for Pollers routes."""

from __future__ import annotations

from pydantic import Field

from ._base import ListResponse


class PollersResponse(ListResponse):
    """Response from list_pollers."""

    data: list[dict] = Field(default_factory=list, validation_alias="pollers")
