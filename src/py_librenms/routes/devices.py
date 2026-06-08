"""Private async implementation for Devices routes."""

from __future__ import annotations

from typing import Literal

from ..models import ApiResponse
from ..models.devices import (
    ComponentsResponse,
    DeviceFdbResponse,
    DevicePortsResponse,
    DeviceResponse,
    DevicesResponse,
)
from ._synchronicity import synchronizer
from ._types import ClientProtocol, _compact, _graph_params, _validate_maintenance_params

DeviceListType = Literal[
    "all",
    "active",
    "ignored",
    "up",
    "down",
    "disabled",
    "os",
    "mac",
    "ipv4",
    "ipv6",
    "location",
    "location_id",
    "hostname",
    "sysName",
    "display",
    "device_id",
    "type",
    "serial",
    "version",
    "hardware",
    "features",
]


class Devices:
    """Async route namespace bound to a client transport."""

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client

    async def del_device(self, hostname: str) -> ApiResponse:
        """Delete a given device.

        Route: DELETE /api/v0/devices/:hostname

        :param hostname: Device hostname or ID.
        """
        data = await self._client._delete(f"/devices/{hostname}")
        return ApiResponse.model_validate(data)

    async def get_device(self, hostname: str) -> DeviceResponse:
        """Get details of a given device.

        Route: GET /api/v0/devices/:hostname

        :param hostname: Device hostname or ID.
        """
        data = await self._client._get(f"/devices/{hostname}")
        return DeviceResponse.model_validate(data)

    async def discover_device(self, hostname: str) -> ApiResponse:
        """Trigger a discovery of given device.

        Route: GET /api/v0/devices/:hostname/discover

        :param hostname: Device hostname or ID.
        """
        data = await self._client._get(f"/devices/{hostname}/discover")
        return ApiResponse.model_validate(data)

    async def availability(self, hostname: str) -> ApiResponse:
        """Get calculated availabilities of given device.

        Route: GET /api/v0/devices/:hostname/availability

        :param hostname: Device hostname or ID.
        """
        data = await self._client._get(f"/devices/{hostname}/availability")
        return ApiResponse.model_validate(data)

    async def outages(self, hostname: str) -> ApiResponse:
        """Get detected outages of given device.

        Route: GET /api/v0/devices/:hostname/outages

        :param hostname: Device hostname or ID.
        """
        data = await self._client._get(f"/devices/{hostname}/outages")
        return ApiResponse.model_validate(data)

    async def get_graphs(self, hostname: str) -> ApiResponse:
        """Get a list of available graphs for a device (excluding ports).

        Route: GET /api/v0/devices/:hostname/graphs

        :param hostname: Device hostname or ID.
        """
        data = await self._client._get(f"/devices/{hostname}/graphs")
        return ApiResponse.model_validate(data)

    async def list_available_health_graphs(
        self, hostname: str, type: str | None = None, sensor_id: int | None = None
    ) -> ApiResponse:
        """List available health graphs for a device.

        Route: GET /api/v0/devices/:hostname/health(/:type)(/:sensor_id)

        :param hostname: Device hostname or ID.
        :param type: Optional health sensor type to filter by.
        :param sensor_id: Optional specific sensor ID.
        """
        url = f"/devices/{hostname}/health"
        if type is not None:
            url += f"/{type}"
            if sensor_id is not None:
                url += f"/{sensor_id}"
        data = await self._client._get(url)
        return ApiResponse.model_validate(data)

    async def list_available_wireless_graphs(
        self, hostname: str, type: str | None = None, sensor_id: int | None = None
    ) -> ApiResponse:
        """List available wireless graphs for a device.

        Route: GET /api/v0/devices/:hostname/wireless(/:type)(/:sensor_id)

        :param hostname: Device hostname or ID.
        :param type: Optional wireless sensor type to filter by.
        :param sensor_id: Optional specific sensor ID.
        """
        url = f"/devices/{hostname}/wireless"
        if type is not None:
            url += f"/{type}"
            if sensor_id is not None:
                url += f"/{sensor_id}"
        data = await self._client._get(url)
        return ApiResponse.model_validate(data)

    async def get_device_wireless_sensors(
        self, hostname: str, cls: str | None = None, columns: str | None = None
    ) -> ApiResponse:
        """Get wireless sensors recorded for a device.

        Route: GET /api/v0/devices/:hostname/wireless-sensors

        :param hostname: Device hostname or ID.
        :param cls: Optional sensor class to filter by.
        :param columns: Comma-separated list of columns to return.
        """
        params = {}
        if cls is not None:
            params["class"] = cls
        if columns is not None:
            params["columns"] = columns
        data = await self._client._get(f"/devices/{hostname}/wireless-sensors", params=params)
        return ApiResponse.model_validate(data)

    async def get_health_graph(
        self, hostname: str, type: str, sensor_id: int | None = None
    ) -> bytes:
        """Get a health class graph for a device.

        Route: GET /api/v0/devices/:hostname/graphs/health/:type(/:sensor_id)

        :param hostname: Device hostname or ID.
        :param type: Health sensor type.
        :param sensor_id: Optional specific sensor ID.
        """
        url = f"/devices/{hostname}/graphs/health/{type}"
        if sensor_id is not None:
            url += f"/{sensor_id}"
        return await self._client._get_bytes(url)

    async def get_wireless_graph(
        self, hostname: str, type: str, sensor_id: int | None = None
    ) -> bytes:
        """Get a wireless class graph for a device.

        Route: GET /api/v0/devices/:hostname/graphs/wireless/:type(/:sensor_id)

        :param hostname: Device hostname or ID.
        :param type: Wireless sensor type.
        :param sensor_id: Optional specific sensor ID.
        """
        url = f"/devices/{hostname}/graphs/wireless/{type}"
        if sensor_id is not None:
            url += f"/{sensor_id}"
        return await self._client._get_bytes(url)

    async def get_graph_generic_by_hostname(
        self,
        hostname: str,
        type: str,
        from_time: str | None = None,
        to_time: str | None = None,
        width: int | None = None,
        height: int | None = None,
        output: str | None = None,
    ) -> bytes:
        """Get a specific graph for a device.

        Route: GET /api/v0/devices/:hostname/:type

        :param hostname: Device hostname or ID.
        :param type: Graph type.
        :param from_time: Start time for the graph.
        :param to_time: End time for the graph.
        :param width: Graph width in pixels.
        :param height: Graph height in pixels.
        :param output: Output format (e.g. 'base64').
        """
        params = _graph_params(from_time, to_time, width, height, output=output)
        return await self._client._get_bytes(f"/devices/{hostname}/{type}", params=params)

    async def get_graph_by_service(
        self,
        hostname: str,
        service_id: int,
        datasource: str,
        from_time: str | None = None,
        to_time: str | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> bytes:
        """Get the graph for a service on a device.

        Route: GET /api/v0/devices/:hostname/services/:service_id/graphs/:datasource

        :param hostname: Device hostname or ID.
        :param service_id: Service ID.
        :param datasource: The datasource to graph.
        :param from_time: Start time for the graph.
        :param to_time: End time for the graph.
        :param width: Graph width in pixels.
        :param height: Graph height in pixels.
        """
        params = _graph_params(from_time, to_time, width, height)
        return await self._client._get_bytes(
            f"/devices/{hostname}/services/{service_id}/graphs/{datasource}",
            params=params,
        )

    async def get_device_ports(
        self, hostname: str, columns: str | None = None, with_vlans: bool = False
    ) -> DevicePortsResponse:
        """Get a list of ports for a particular device.

        Route: GET /api/v0/devices/:hostname/ports

        :param hostname: Device hostname or ID.
        :param columns: Comma-separated list of columns to return.
        :param with_vlans: If True, include VLAN information.
        """
        params = {}
        if columns is not None:
            params["columns"] = columns
        if with_vlans:
            params["with"] = "vlans"
        data = await self._client._get(f"/devices/{hostname}/ports", params=params)
        return DevicePortsResponse.model_validate(data)

    async def get_device_fdb(self, hostname: str) -> DeviceFdbResponse:
        """Get a list of FDB entries associated with a device.

        Route: GET /api/v0/devices/:hostname/fdb

        :param hostname: Device hostname or ID.
        """
        data = await self._client._get(f"/devices/{hostname}/fdb")
        return DeviceFdbResponse.model_validate(data)

    async def get_device_nac(self, hostname: str) -> ApiResponse:
        """Get a list of NAC entries associated with a device.

        Route: GET /api/v0/devices/:hostname/nac

        :param hostname: Device hostname or ID.
        """
        data = await self._client._get(f"/devices/{hostname}/nac")
        return ApiResponse.model_validate(data)

    async def get_device_ip_addresses(self, hostname: str) -> ApiResponse:
        """Get a list of IP addresses (v4 and v6) associated with a device.

        Route: GET /api/v0/devices/:hostname/ip

        :param hostname: Device hostname or ID.
        """
        data = await self._client._get(f"/devices/{hostname}/ip")
        return ApiResponse.model_validate(data)

    async def get_port_stack(self, hostname: str, valid_mappings: bool = False) -> ApiResponse:
        """Get a list of port mappings for a device.

        Route: GET /api/v0/devices/:hostname/port_stack

        :param hostname: Device hostname or ID.
        :param valid_mappings: If True, only return valid port mappings.
        """
        params = {}
        if valid_mappings:
            params["valid_mappings"] = 1
        data = await self._client._get(f"/devices/{hostname}/port_stack", params=params)
        return ApiResponse.model_validate(data)

    async def get_device_transceivers(self, hostname: str) -> ApiResponse:
        """Get a list of transceivers associated with a device.

        Route: GET /api/v0/devices/:hostname/transceivers

        :param hostname: Device hostname or ID.
        """
        data = await self._client._get(f"/devices/{hostname}/transceivers")
        return ApiResponse.model_validate(data)

    async def get_components(
        self,
        hostname: str,
        type: str | None = None,
        id: int | None = None,
        label: str | None = None,
        status: str | None = None,
        disabled: int | None = None,
        ignore: int | None = None,
    ) -> ComponentsResponse:
        """Get a list of components for a particular device.

        Route: GET /api/v0/devices/:hostname/components

        :param hostname: Device hostname or ID.
        :param type: Filter by component type.
        :param id: Filter by component ID.
        :param label: Filter by component label.
        :param status: Filter by component status.
        :param disabled: Filter by disabled state (0 or 1).
        :param ignore: Filter by ignore state (0 or 1).
        """
        params = _compact(
            type=type, id=id, label=label, status=status, disabled=disabled, ignore=ignore
        )
        data = await self._client._get(f"/devices/{hostname}/components", params=params)
        return ComponentsResponse.model_validate(data)

    async def add_components(self, hostname: str, type: str) -> ApiResponse:
        """Create a new component of a type on a particular device.

        Route: POST /api/v0/devices/:hostname/components/:type

        :param hostname: Device hostname or ID.
        :param type: Component type to create.
        """
        data = await self._client._post(f"/devices/{hostname}/components/{type}")
        return ApiResponse.model_validate(data)

    async def edit_components(self, hostname: str, components: dict) -> ApiResponse:
        """Edit an existing component on a particular device.

        Route: PUT /api/v0/devices/:hostname/components

        :param hostname: Device hostname or ID.
        :param components: Dict of component data keyed by component ID.
        """
        data = await self._client._put(f"/devices/{hostname}/components", json=components)
        return ApiResponse.model_validate(data)

    async def delete_components(self, hostname: str, component_id: int) -> ApiResponse:
        """Delete an existing component on a particular device.

        Route: DELETE /api/v0/devices/:hostname/components/:component

        :param hostname: Device hostname or ID.
        :param component_id: ID of the component to delete.
        """
        data = await self._client._delete(f"/devices/{hostname}/components/{component_id}")
        return ApiResponse.model_validate(data)

    async def get_port_stats_by_port_hostname(
        self, hostname: str, ifname: str, columns: str | None = None
    ) -> ApiResponse:
        """Get information about a particular port for a device.

        Route: GET /api/v0/devices/:hostname/ports/:ifname

        :param hostname: Device hostname or ID.
        :param ifname: Interface name (e.g. 'GigabitEthernet0/1').
        :param columns: Comma-separated list of columns to return.
        """
        params = {}
        if columns is not None:
            params["columns"] = columns
        data = await self._client._get(f"/devices/{hostname}/ports/{ifname}", params=params)
        return ApiResponse.model_validate(data)

    async def get_graph_by_port_hostname(
        self,
        hostname: str,
        ifname: str,
        type: str,
        width: int = 1075,
        height: int = 300,
        from_time: str | None = None,
        to_time: str | None = None,
        if_descr: bool = False,
        graph_type: str | None = None,
    ) -> bytes:
        """Get a graph of a port for a particular device.

        Route: GET /api/v0/devices/:hostname/ports/:ifname/:type

        :param hostname: Device hostname or ID.
        :param ifname: Interface name (e.g. 'GigabitEthernet0/1').
        :param type: Graph type (e.g. 'port_bits').
        :param width: Graph width in pixels.
        :param height: Graph height in pixels.
        :param from_time: Start time for the graph.
        :param to_time: End time for the graph.
        :param if_descr: If True, use ifDescr instead of ifName to match port.
        :param graph_type: Optional override graph type.
        """
        params = _graph_params(from_time, to_time, width, height, graph_type=graph_type)
        if if_descr:
            params["ifDescr"] = "true"
        return await self._client._get_bytes(
            f"/devices/{hostname}/ports/{ifname}/{type}", params=params
        )

    async def list_sensors(self) -> ApiResponse:
        """Get a list of all sensors.

        Route: GET /api/v0/resources/sensors
        """
        data = await self._client._get("/resources/sensors")
        return ApiResponse.model_validate(data)

    async def list_devices(
        self,
        order: str | None = None,
        type: DeviceListType | None = None,
        query: str | None = None,
    ) -> DevicesResponse:
        """Return a list of devices.

        Route: GET /api/v0/devices

        :param order: Order results, e.g. 'hostname ASC'.
        :param type: Filter type. For search types (os, mac, ipv4, ipv6, location,
            location_id, hostname, sysName, display, device_id, type, serial,
            version, hardware, features), the ``query`` param provides the search value.
        :param query: Search value when type is a search filter.
        :raises ValueError: If type requires a query but none is provided.
        """
        _search_types = {
            "os",
            "mac",
            "ipv4",
            "ipv6",
            "location",
            "location_id",
            "hostname",
            "sysName",
            "display",
            "device_id",
            "type",
            "serial",
            "version",
            "hardware",
            "features",
        }
        if type in _search_types and not query:
            raise ValueError(f"'query' is required when type is '{type}'")
        params = _compact(order=order, type=type, query=query)
        data = await self._client._get("/devices", params=params)
        return DevicesResponse.model_validate(data)

    async def device_under_maintenance(self, hostname: str) -> bool:
        """Get the current maintenance status of a device.

        Route: GET /api/v0/devices/:hostname/maintenance

        :param hostname: Device hostname or ID.
        :returns: True if the device is currently under maintenance.
        """
        data = await self._client._get(f"/devices/{hostname}/maintenance")
        return data.get("is_under_maintenance", False)

    async def maintenance_device(
        self,
        hostname: str,
        duration: str,
        title: str | None = None,
        notes: str | None = None,
        start: str | None = None,
        behavior: int | None = None,
    ) -> ApiResponse:
        """Set a device into maintenance mode.

        Route: POST /api/v0/devices/:hostname/maintenance

        :param hostname: Device hostname.
        :param duration: Duration of maintenance in 'HH:MM' format, e.g. '02:00'.
        :param title: Optional title. Replaced with hostname if omitted.
        :param notes: Optional description for the maintenance.
        :param start: Optional start time in 'Y-m-d H:i:00' format, e.g. '2022-08-01 22:45:00'.
            Uses current system time if omitted.
        :param behavior: Optional maintenance behavior id.
        :raises ValueError: If duration or start format is invalid.
        """
        _validate_maintenance_params(duration, start)
        payload: dict = {
            "duration": duration,
            **_compact(title=title, notes=notes, start=start, behavior=behavior),
        }
        data = await self._client._post(f"/devices/{hostname}/maintenance", json=payload)
        return ApiResponse.model_validate(data)

    async def add_device(self, hostname: str, **kwargs) -> ApiResponse:
        """Add a new device.

        Route: POST /api/v0/devices

        :param hostname: Hostname or IP of the device to add.
        :param kwargs: Additional device fields (snmpver, community, port, transport, etc.).
        """
        payload = {"hostname": hostname, **kwargs}
        data = await self._client._post("/devices", json=payload)
        return ApiResponse.model_validate(data)

    async def list_oxidized(self, hostname: str | None = None) -> list[dict]:
        """List devices for use with Oxidized.

        Route: GET /api/v0/oxidized(/:hostname)

        Note: This endpoint returns a raw JSON list, not the standard API envelope.

        :param hostname: Optional hostname to filter to a single device.
        """
        url = "/oxidized"
        if hostname is not None:
            url += f"/{hostname}"
        data = await self._client._get(url)
        # API returns a raw list (not wrapped in a dict)
        if isinstance(data, list):
            return data
        return ApiResponse.model_validate(data)

    async def update_device_field(
        self, hostname: str, field: str | list, data: str | list
    ) -> ApiResponse:
        """Update a device field in the database.

        Route: PATCH /api/v0/devices/:hostname

        :param hostname: Device hostname or ID.
        :param field: Field name or list of field names to update.
        :param data: New value or list of values corresponding to fields.
        """
        resp = await self._client._patch(
            f"/devices/{hostname}", json={"field": field, "data": data}
        )
        return ApiResponse.model_validate(resp)

    async def update_device_port_notes(self, hostname: str, portid: int, notes: str) -> ApiResponse:
        """Update a device port notes field.

        Route: PATCH /api/v0/devices/:hostname/port/:portid

        :param hostname: Device hostname or ID.
        :param portid: Port ID to update.
        :param notes: New notes value.
        """
        data = await self._client._patch(
            f"/devices/{hostname}/port/{portid}", json={"notes": notes}
        )
        return ApiResponse.model_validate(data)

    async def rename_device(self, hostname: str, new_hostname: str) -> ApiResponse:
        """Rename a device.

        Route: PATCH /api/v0/devices/:hostname/rename/:new_hostname

        :param hostname: Current device hostname or ID.
        :param new_hostname: New hostname for the device.
        """
        data = await self._client._patch(f"/devices/{hostname}/rename/{new_hostname}")
        return ApiResponse.model_validate(data)

    async def get_device_groups(self, hostname: str) -> ApiResponse:
        """List the device groups that a device is matched on.

        Route: GET /api/v0/devices/:hostname/groups

        :param hostname: Device hostname or ID.
        """
        data = await self._client._get(f"/devices/{hostname}/groups")
        return ApiResponse.model_validate(data)

    async def search_oxidized(self, searchstring: str) -> ApiResponse:
        """Search all Oxidized device configs for a string.

        Route: GET /api/v0/oxidized/config/search/:searchstring

        :param searchstring: String to search for in device configs.
        """
        data = await self._client._get(f"/oxidized/config/search/{searchstring}")
        return ApiResponse.model_validate(data)

    async def get_oxidized_config(self, hostname: str) -> ApiResponse:
        """Return a specific device's config from Oxidized.

        Route: GET /api/v0/oxidized/config/:hostname

        :param hostname: Device hostname.
        """
        data = await self._client._get(f"/oxidized/config/{hostname}")
        return ApiResponse.model_validate(data)

    async def add_parents_to_host(self, device: str, parent_ids: str) -> ApiResponse:
        """Add one or more parents to a host.

        Route: POST /api/v0/devices/:device/parents

        :param device: Device hostname or ID.
        :param parent_ids: Comma-separated list of parent device IDs.
        """
        data = await self._client._post(
            f"/devices/{device}/parents", json={"parent_ids": parent_ids}
        )
        return ApiResponse.model_validate(data)

    async def delete_parents_from_host(
        self, device: str, parent_ids: str | None = None
    ) -> ApiResponse:
        """Delete some or all parents from a host.

        Route: DELETE /api/v0/devices/:device/parents

        :param device: Device hostname or ID.
        :param parent_ids: Comma-separated parent device IDs to remove. If None, removes all.
        """
        payload = {}
        if parent_ids is not None:
            payload["parent_ids"] = parent_ids
        data = await self._client._delete(f"/devices/{device}/parents", json=payload)
        return ApiResponse.model_validate(data)


DevicesSync = synchronizer.wrap(Devices, name="DevicesSync", target_module=__name__)
