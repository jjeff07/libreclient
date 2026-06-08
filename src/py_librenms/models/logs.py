"""Response models for Logs routes."""

from __future__ import annotations

from pydantic import Field

from ._base import ListResponse


class LogsResponse(ListResponse):
    """Response from list_eventlog / list_alertlog / list_syslog / list_authlog."""

    data: list[dict] = Field(default_factory=list, validation_alias="logs")
