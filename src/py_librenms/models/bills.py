"""Response models for Bills routes."""

from __future__ import annotations

from pydantic import Field

from ._base import ListResponse


class BillsResponse(ListResponse):
    """Response from list_bills / get_bill."""

    data: list[dict] = Field(default_factory=list, validation_alias="bills")


class BillHistoryResponse(ListResponse):
    """Response from get_bill_history."""

    data: list[dict] = Field(default_factory=list, validation_alias="bill_history")
