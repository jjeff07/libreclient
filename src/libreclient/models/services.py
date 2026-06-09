"""Response models for Services routes."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from ._base import ListResponse


class ServicesResponse(ListResponse):
    """Response from list_services / get_service.

    Note: LibreNMS returns ``[[]]`` when no services exist.
    """

    data: list[Any] = Field(default_factory=list, validation_alias="services")
