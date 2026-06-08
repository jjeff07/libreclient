"""Response models for Port Security routes."""

from __future__ import annotations

from pydantic import Field

from ._base import ListResponse


class PortSecurityResponse(ListResponse):
    """Response from get_port_security."""

    data: list[dict] = Field(default_factory=list, validation_alias="port_security")
