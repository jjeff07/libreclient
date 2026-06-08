"""Response models for Devices routes."""

from __future__ import annotations

from pydantic import Field

from ._base import ListResponse


class DevicesResponse(ListResponse):
    """Response from list_devices."""

    data: list[dict] = Field(default_factory=list, validation_alias="devices")


class DeviceResponse(ListResponse):
    """Response from get_device."""

    data: list[dict] = Field(default_factory=list, validation_alias="devices")


class DevicePortsResponse(ListResponse):
    """Response from get_device_ports."""

    data: list[dict] = Field(default_factory=list, validation_alias="ports")


class DeviceFdbResponse(ListResponse):
    """Response from get_device_fdb."""

    data: list[dict] = Field(
        default_factory=list, validation_alias="ports_fdb"
    )


class ComponentsResponse(ListResponse):
    """Response from get_components."""

    data: list[dict] = Field(
        default_factory=list, validation_alias="components"
    )
