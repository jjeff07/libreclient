"""Response models for Portgroups routes."""

from __future__ import annotations

from ._base import ListResponse


class PortgroupsResponse(ListResponse):
    """Response from get_portgroups (graph endpoints — returns bytes, not JSON)."""
