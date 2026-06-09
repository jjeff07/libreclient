"""Response models for Ports routes."""

from __future__ import annotations

from pydantic import Field

from ._base import ApiResponse, ListResponse


class PortsResponse(ListResponse):
    """Response from get_all_ports / search_ports."""

    data: list[dict] = Field(default_factory=list, validation_alias="ports")


class PortResponse(ListResponse):
    """Response from get_port_info / ports_with_associated_mac."""

    data: list[dict] = Field(default_factory=list, validation_alias="port")


class PortIpResponse(ListResponse):
    """Response from get_port_ip_info."""

    data: list[dict] = Field(
        default_factory=list, validation_alias="addresses"
    )


class PortTransceiverResponse(ApiResponse):
    """Response from get_port_transceiver."""

    data: list[dict] = Field(
        default_factory=list, validation_alias="transceivers"
    )


class PortDescriptionResponse(ApiResponse):
    """Response from get_port_description."""

    port_description: str = ""
