"""Response models for Switching routes."""

from __future__ import annotations

from pydantic import Field

from ._base import ListResponse


class SwitchingResponse(ListResponse):
    """Response from switching list endpoints."""

    data: list[dict] = Field(default_factory=list, validation_alias="switching")
