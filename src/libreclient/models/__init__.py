"""Pydantic models for LibreNMS API responses.

Import from here for convenience, or directly from sub-modules for clarity.
"""

# Base models (shared across all routes)
from ._base import ApiResponse, ApiResponseWithId, ListResponse

# Per-route response models
from .alerts import (
    AlertsResponse,
    AlertTemplateCreatedResponse,
    AlertTemplatesResponse,
    RulesResponse,
)
from .arp import ArpResponse
from .bills import BillHistoryResponse, BillsResponse
from .device_groups import DeviceGroupDevicesResponse, DeviceGroupsResponse
from .devices import (
    ComponentsResponse,
    DeviceFdbResponse,
    DevicePortsResponse,
    DeviceResponse,
    DevicesResponse,
)
from .index import IndexResponse
from .inventory import InventoryResponse
from .locations import LocationsResponse
from .logs import LogsResponse
from .poller_groups import PollerGroupsResponse
from .pollers import PollersResponse
from .port_groups import PortGroupsResponse
from .port_security import PortSecurityResponse
from .portgroups import PortgroupsResponse
from .ports import (
    PortDescriptionResponse,
    PortIpResponse,
    PortResponse,
    PortsResponse,
    PortTransceiverResponse,
)
from .routing import RoutingResponse
from .services import ServicesResponse
from .switching import SwitchingResponse
from .system import SystemResponse

__all__ = [
    "AlertTemplateCreatedResponse",
    "AlertTemplatesResponse",
    "AlertsResponse",
    "ApiResponse",
    "ApiResponseWithId",
    "ArpResponse",
    "BillHistoryResponse",
    "BillsResponse",
    "ComponentsResponse",
    "DeviceFdbResponse",
    "DeviceGroupDevicesResponse",
    "DeviceGroupsResponse",
    "DevicePortsResponse",
    "DeviceResponse",
    "DevicesResponse",
    "IndexResponse",
    "InventoryResponse",
    "ListResponse",
    "LocationsResponse",
    "LogsResponse",
    "PollerGroupsResponse",
    "PollersResponse",
    "PortDescriptionResponse",
    "PortGroupsResponse",
    "PortIpResponse",
    "PortResponse",
    "PortSecurityResponse",
    "PortTransceiverResponse",
    "PortgroupsResponse",
    "PortsResponse",
    "RoutingResponse",
    "RulesResponse",
    "ServicesResponse",
    "SwitchingResponse",
    "SystemResponse",
]
