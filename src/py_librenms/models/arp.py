"""Response models for ARP routes."""

from __future__ import annotations

from pydantic import Field

from ._base import ListResponse


class ArpResponse(ListResponse):
    """Response from list_arp."""

    data: list[dict] = Field(default_factory=list, validation_alias="arp")
