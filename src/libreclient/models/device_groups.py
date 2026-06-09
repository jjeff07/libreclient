"""Response models for Device Groups routes."""

from __future__ import annotations

from pydantic import Field

from ._base import ListResponse


class DeviceGroupsResponse(ListResponse):
    """Response from get_devicegroups."""

    data: list[dict] = Field(default_factory=list, validation_alias="groups")


class DeviceGroupDevicesResponse(ListResponse):
    """Response from get_devices_by_group."""

    data: list[dict] = Field(default_factory=list, validation_alias="devices")
