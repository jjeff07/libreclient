"""Response models for Inventory routes."""

from __future__ import annotations

from pydantic import Field

from ._base import ListResponse


class InventoryResponse(ListResponse):
    """Response from get_inventory."""

    data: list[dict] = Field(default_factory=list, validation_alias="inventory")
