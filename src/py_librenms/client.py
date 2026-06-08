"""
LibreNMS API clients — synchronous and asynchronous.
"""

from typing import Any

import niquests
from pydantic import PrivateAttr

from ._base_client import BaseLibreClient
from .routes import (
    AlertsAsync,
    AlertsSync,
    ArpAsync,
    ArpSync,
    BillsAsync,
    BillsSync,
    DeviceGroupsAsync,
    DeviceGroupsSync,
    DevicesAsync,
    DevicesSync,
    IndexAsync,
    IndexSync,
    InventoryAsync,
    InventorySync,
    LocationsAsync,
    LocationsSync,
    LogsAsync,
    LogsSync,
    PollerGroupsAsync,
    PollerGroupsSync,
    PollersAsync,
    PollersSync,
    PortGroupsAsync,
    PortgroupsAsync,
    PortGroupsSync,
    PortgroupsSync,
    PortsAsync,
    PortSecurityAsync,
    PortSecuritySync,
    PortsSync,
    RoutingAsync,
    RoutingSync,
    ServicesAsync,
    ServicesSync,
    SwitchingAsync,
    SwitchingSync,
    SystemAsync,
    SystemSync,
)


class LibreClientSync(BaseLibreClient):
    """Synchronous LibreNMS API client backed by :class:`niquests.Session`."""

    _session: niquests.Session = PrivateAttr()
    _alerts: AlertsSync = PrivateAttr()
    _arp: ArpSync = PrivateAttr()
    _bills: BillsSync = PrivateAttr()
    _device_groups: DeviceGroupsSync = PrivateAttr()
    _devices: DevicesSync = PrivateAttr()
    _index: IndexSync = PrivateAttr()
    _inventory: InventorySync = PrivateAttr()
    _locations: LocationsSync = PrivateAttr()
    _logs: LogsSync = PrivateAttr()
    _poller_groups: PollerGroupsSync = PrivateAttr()
    _pollers: PollersSync = PrivateAttr()
    _port_groups: PortGroupsSync = PrivateAttr()
    _port_security: PortSecuritySync = PrivateAttr()
    _portgroups: PortgroupsSync = PrivateAttr()
    _ports: PortsSync = PrivateAttr()
    _routing: RoutingSync = PrivateAttr()
    _services: ServicesSync = PrivateAttr()
    _switching: SwitchingSync = PrivateAttr()
    _system: SystemSync = PrivateAttr()

    def model_post_init(self, __context) -> None:
        self._session = niquests.Session()
        self._session.headers.update({"X-Auth-Token": self.token})
        self._session.verify = self.verify_ssl
        self._alerts = AlertsSync(self)
        self._arp = ArpSync(self)
        self._bills = BillsSync(self)
        self._device_groups = DeviceGroupsSync(self)
        self._devices = DevicesSync(self)
        self._index = IndexSync(self)
        self._inventory = InventorySync(self)
        self._locations = LocationsSync(self)
        self._logs = LogsSync(self)
        self._poller_groups = PollerGroupsSync(self)
        self._pollers = PollersSync(self)
        self._port_groups = PortGroupsSync(self)
        self._port_security = PortSecuritySync(self)
        self._portgroups = PortgroupsSync(self)
        self._ports = PortsSync(self)
        self._routing = RoutingSync(self)
        self._services = ServicesSync(self)
        self._switching = SwitchingSync(self)
        self._system = SystemSync(self)

    async def _request_raw(self, method: str, url: str, **kwargs) -> Any:
        return self._session.request(method, url, **kwargs)

    @property
    def alerts(self) -> AlertsSync:
        return self._alerts

    @property
    def arp(self) -> ArpSync:
        return self._arp

    @property
    def bills(self) -> BillsSync:
        return self._bills

    @property
    def device_groups(self) -> DeviceGroupsSync:
        return self._device_groups

    @property
    def devices(self) -> DevicesSync:
        return self._devices

    @property
    def index(self) -> IndexSync:
        return self._index

    @property
    def inventory(self) -> InventorySync:
        return self._inventory

    @property
    def locations(self) -> LocationsSync:
        return self._locations

    @property
    def logs(self) -> LogsSync:
        return self._logs

    @property
    def poller_groups(self) -> PollerGroupsSync:
        return self._poller_groups

    @property
    def pollers(self) -> PollersSync:
        return self._pollers

    @property
    def port_groups(self) -> PortGroupsSync:
        return self._port_groups

    @property
    def port_security(self) -> PortSecuritySync:
        return self._port_security

    @property
    def portgroups(self) -> PortgroupsSync:
        return self._portgroups

    @property
    def ports(self) -> PortsSync:
        return self._ports

    @property
    def routing(self) -> RoutingSync:
        return self._routing

    @property
    def services(self) -> ServicesSync:
        return self._services

    @property
    def switching(self) -> SwitchingSync:
        return self._switching

    @property
    def system(self) -> SystemSync:
        return self._system

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> "LibreClientSync":
        return self

    def __exit__(self, *_) -> None:
        self.close()


class LibreClientAsync(BaseLibreClient):
    """Asynchronous LibreNMS API client backed by :class:`niquests.AsyncSession`."""

    _session: niquests.AsyncSession = PrivateAttr()
    _alerts: AlertsAsync = PrivateAttr()
    _arp: ArpAsync = PrivateAttr()
    _bills: BillsAsync = PrivateAttr()
    _device_groups: DeviceGroupsAsync = PrivateAttr()
    _devices: DevicesAsync = PrivateAttr()
    _index: IndexAsync = PrivateAttr()
    _inventory: InventoryAsync = PrivateAttr()
    _locations: LocationsAsync = PrivateAttr()
    _logs: LogsAsync = PrivateAttr()
    _poller_groups: PollerGroupsAsync = PrivateAttr()
    _pollers: PollersAsync = PrivateAttr()
    _port_groups: PortGroupsAsync = PrivateAttr()
    _port_security: PortSecurityAsync = PrivateAttr()
    _portgroups: PortgroupsAsync = PrivateAttr()
    _ports: PortsAsync = PrivateAttr()
    _routing: RoutingAsync = PrivateAttr()
    _services: ServicesAsync = PrivateAttr()
    _switching: SwitchingAsync = PrivateAttr()
    _system: SystemAsync = PrivateAttr()

    def model_post_init(self, __context) -> None:
        self._session = niquests.AsyncSession()
        self._session.headers.update({"X-Auth-Token": self.token})
        self._session.verify = self.verify_ssl

        self._alerts = AlertsAsync(self)
        self._arp = ArpAsync(self)
        self._bills = BillsAsync(self)
        self._device_groups = DeviceGroupsAsync(self)
        self._devices = DevicesAsync(self)
        self._index = IndexAsync(self)
        self._inventory = InventoryAsync(self)
        self._locations = LocationsAsync(self)
        self._logs = LogsAsync(self)
        self._poller_groups = PollerGroupsAsync(self)
        self._pollers = PollersAsync(self)
        self._port_groups = PortGroupsAsync(self)
        self._port_security = PortSecurityAsync(self)
        self._portgroups = PortgroupsAsync(self)
        self._ports = PortsAsync(self)
        self._routing = RoutingAsync(self)
        self._services = ServicesAsync(self)
        self._switching = SwitchingAsync(self)
        self._system = SystemAsync(self)

    async def _request_raw(self, method: str, url: str, **kwargs) -> Any:
        return await self._session.request(method, url, **kwargs)

    @property
    def alerts(self) -> AlertsAsync:
        return self._alerts

    @property
    def arp(self) -> ArpAsync:
        return self._arp

    @property
    def bills(self) -> BillsAsync:
        return self._bills

    @property
    def device_groups(self) -> DeviceGroupsAsync:
        return self._device_groups

    @property
    def devices(self) -> DevicesAsync:
        return self._devices

    @property
    def index(self) -> IndexAsync:
        return self._index

    @property
    def inventory(self) -> InventoryAsync:
        return self._inventory

    @property
    def locations(self) -> LocationsAsync:
        return self._locations

    @property
    def logs(self) -> LogsAsync:
        return self._logs

    @property
    def poller_groups(self) -> PollerGroupsAsync:
        return self._poller_groups

    @property
    def pollers(self) -> PollersAsync:
        return self._pollers

    @property
    def port_groups(self) -> PortGroupsAsync:
        return self._port_groups

    @property
    def port_security(self) -> PortSecurityAsync:
        return self._port_security

    @property
    def portgroups(self) -> PortgroupsAsync:
        return self._portgroups

    @property
    def ports(self) -> PortsAsync:
        return self._ports

    @property
    def routing(self) -> RoutingAsync:
        return self._routing

    @property
    def services(self) -> ServicesAsync:
        return self._services

    @property
    def switching(self) -> SwitchingAsync:
        return self._switching

    @property
    def system(self) -> SystemAsync:
        return self._system

    async def close(self) -> None:
        await self._session.close()

    async def __aenter__(self) -> "LibreClientAsync":
        return self

    async def __aexit__(self, *_) -> None:
        await self.close()
