"""
Base response models shared across all route modules.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ApiResponse(BaseModel):
    """Base response envelope — every API call returns at least these."""

    model_config = ConfigDict(populate_by_name=True)

    status: str = "ok"
    message: str = ""


class ApiResponseWithId(ApiResponse):
    """Response that includes a created/affected resource id."""

    id: int


class ListResponse(ApiResponse):
    """Response containing a counted list of resources.

    Subclass this and override ``data`` with the appropriate
    ``validation_alias`` for the API's response key.
    """

    count: int = 0
    data: list[Any] = Field(default_factory=list)
