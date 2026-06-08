"""Response models for System routes."""

from __future__ import annotations

from pydantic import Field

from ._base import ApiResponse


class SystemResponse(ApiResponse):
    """Response from system info endpoints."""

    data: list[dict] = Field(default_factory=list, validation_alias="system")
