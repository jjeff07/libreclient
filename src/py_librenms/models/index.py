"""Response models for Index routes."""

from __future__ import annotations

from pydantic import BaseModel


class IndexResponse(BaseModel):
    """Response from list_api_endpoints.

    The /api/v0 endpoint returns a flat dict of route_name → URL,
    not the standard status/message envelope.
    """

    endpoints: dict[str, str] = {}
