"""Device Groups routes — async implementation."""

from __future__ import annotations

import typing

from ..models import ApiResponse
from ..models.device_groups import (
    DeviceGroupDevicesResponse,
    DeviceGroupsResponse,
)
from ._types import ClientProtocol, _compact, _validate_maintenance_params


def _validate_group_type(
    type: str | None, rules: str | None, devices: list | None
) -> tuple[str | None, list | None]:
    """Validate and sanitize rules/devices based on group type.

    :returns: Sanitized (rules, devices) tuple.
    :raises ValueError: If required parameters are missing for the given type.
    """
    if type == "dynamic" and not rules:
        raise ValueError("'rules' is required when type is 'dynamic'")
    if type == "static" and not devices:
        raise ValueError("'devices' is required when type is 'static'")
    if type == "dynamic" and devices:
        print(
            "WARNING: 'devices' is ignored when type is 'dynamic', discarding"
        )
        devices = None
    if type == "static" and rules:
        print("WARNING: 'rules' is ignored when type is 'static', discarding")
        rules = None
    return rules, devices


class DeviceGroups:
    """Device Groups route namespace bound to a client transport."""

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client

    async def get_devicegroups(self) -> DeviceGroupsResponse:
        """List all device groups.

        Route: GET /api/v0/devicegroups
        """
        data = await self._client._get("/devicegroups")
        return DeviceGroupsResponse.model_validate(data)

    async def add_devicegroup(
        self,
        name: str,
        type: typing.Literal["static", "dynamic"],
        desc: str | None = None,
        rules: str | None = None,
        devices: list | None = None,
    ) -> ApiResponse:
        """Add a new device group.

        Route: POST /api/v0/devicegroups

        :param name: Name of the device group.
        :param type: 'static' or 'dynamic'.
        :param desc: Optional description.
        :param rules: Required if type is 'dynamic'. JSON-encoded rule set.
        :param devices: Required if type is 'static'. List of device ids.
        :raises ValueError: If required parameters are missing for the given type.
        """
        rules, devices = _validate_group_type(type, rules, devices)
        payload: dict = {
            "name": name,
            "type": type,
            **_compact(desc=desc, rules=rules, devices=devices),
        }
        data = await self._client._post("/devicegroups", json=payload)
        return ApiResponse.model_validate(data)

    async def update_devicegroup(
        self,
        name: str,
        new_name: str | None = None,
        type: typing.Literal["static", "dynamic"] | None = None,
        desc: str | None = None,
        rules: str | None = None,
        devices: list | None = None,
    ) -> ApiResponse:
        """Update a device group.

        Route: PATCH /api/v0/devicegroups/:name

        :param name: The URL-encoded name of the device group to update.
        :param new_name: Optional new name for the device group.
        :param type: Optional 'static' or 'dynamic'.
        :param desc: Optional description.
        :param rules: Required if type is 'dynamic'. JSON-encoded rule set.
        :param devices: Required if type is 'static'. List of device ids.
        :raises ValueError: If required parameters are missing for the given type.
        """
        if type is not None:
            rules, devices = _validate_group_type(type, rules, devices)
        payload = _compact(
            name=new_name, type=type, desc=desc, rules=rules, devices=devices
        )
        data = await self._client._patch(f"/devicegroups/{name}", json=payload)
        return ApiResponse.model_validate(data)

    async def delete_devicegroup(self, name: str) -> ApiResponse:
        """Delete a device group.

        Route: DELETE /api/v0/devicegroups/:name

        :param name: The URL-encoded name of the device group.
        """
        data = await self._client._delete(f"/devicegroups/{name}")
        return ApiResponse.model_validate(data)

    async def get_devices_by_group(
        self, name: str, full: bool = False
    ) -> DeviceGroupDevicesResponse:
        """List all devices matching the group provided.

        Route: GET /api/v0/devicegroups/:name

        :param name: URL-encoded device group name.
        :param full: If True, return all device data.
        """
        params = {}
        if full:
            params["full"] = 1
        data = await self._client._get(f"/devicegroups/{name}", params=params)
        return DeviceGroupDevicesResponse.model_validate(data)

    async def maintenance_devicegroup(
        self,
        name: str,
        duration: str,
        title: str | None = None,
        notes: str | None = None,
        start: str | None = None,
        behavior: int | None = None,
    ) -> ApiResponse:
        """Set a device group into maintenance mode.

        Route: POST /api/v0/devicegroups/:name/maintenance

        :param name: URL-encoded device group name.
        :param duration: Duration of maintenance in 'H:i' format, e.g. '02:00'.
        :param title: Optional title. Replaced with device group name if omitted.
        :param notes: Optional description for the maintenance.
        :param start: Optional start time in 'Y-m-d H:i:00' format, e.g. '2022-08-01 22:45:00'.
            Uses current system time if omitted.
        :param behavior: Optional maintenance behavior id.
            Defaults to alert.scheduled_maintenance_default_behavior if omitted.
        :raises ValueError: If duration or start format is invalid.
        """
        _validate_maintenance_params(duration, start)
        payload: dict = {
            "duration": duration,
            **_compact(
                title=title, notes=notes, start=start, behavior=behavior
            ),
        }
        data = await self._client._post(
            f"/devicegroups/{name}/maintenance", json=payload
        )
        return ApiResponse.model_validate(data)

    async def add_devices_to_group(
        self, name: str, devices: list
    ) -> ApiResponse:
        """Add devices to a device group.

        Route: POST /api/v0/devicegroups/:name/devices

        :param name: URL-encoded device group name.
        :param devices: List of device ids to add.
        """
        data = await self._client._post(
            f"/devicegroups/{name}/devices", json={"devices": devices}
        )
        return ApiResponse.model_validate(data)

    async def remove_devices_from_group(
        self, name: str, devices: list[int]
    ) -> ApiResponse:
        """Remove devices from a device group.

        Route: DELETE /api/v0/devicegroups/:name/devices

        :param name: URL-encoded device group name.
        :param devices: List of device ids to remove.
        """
        data = await self._client._delete(
            f"/devicegroups/{name}/devices", json={"devices": devices}
        )
        return ApiResponse.model_validate(data)
