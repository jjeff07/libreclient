"""Response and request models for Devices routes."""

from __future__ import annotations

import typing

from pydantic import BaseModel, Field

from ._base import ListResponse

SnmpV3AuthLevel = typing.Literal["noAuthNoPriv", "authNoPriv", "authPriv"]
SnmpV3AuthAlgo = typing.Literal[
    "MD5", "SHA", "SHA-224", "SHA-256", "SHA-384", "SHA-512"
]
SnmpV3CryptoAlgo = typing.Literal[
    "AES", "AES-192", "AES-256", "AES-256-C", "DES"
]


class SnmpV3Credentials(BaseModel):
    """SNMPv3 authentication and encryption credentials.

    Use this when adding a device with ``snmpver='v3'``.

    Example::

        creds = SnmpV3Credentials(
            authlevel="authPriv",
            authname="myuser",
            authpass="secret",
            authalgo="SHA",
            cryptopass="encrypt_secret",
            cryptoalgo="AES",
        )
        client.devices.add_device("10.0.0.1", snmpver="v3", snmp_v3=creds)
    """

    authlevel: SnmpV3AuthLevel = "noAuthNoPriv"
    """SNMP auth level (noAuthNoPriv, authNoPriv, authPriv)."""

    authname: str | None = None
    """SNMP auth username. Required for authNoPriv and authPriv."""

    authpass: str | None = None
    """SNMP auth password. Required for authNoPriv and authPriv."""

    authalgo: SnmpV3AuthAlgo = "SHA"
    """SNMP auth algorithm (MD5, SHA, SHA-224, SHA-256, SHA-384, SHA-512)."""

    cryptopass: str | None = None
    """SNMP crypto password. Required for authPriv."""

    cryptoalgo: SnmpV3CryptoAlgo = "AES"
    """SNMP crypto algorithm (AES, AES-192, AES-256, AES-256-C, DES)."""


class IcmpOnlyDevice(BaseModel):
    """Additional fields for ICMP-only (snmp_disable) devices.

    Use this when adding a device with ``snmp_disable=True``.

    Example::

        icmp = IcmpOnlyDevice(os="linux", sys_name="myhost", hardware="x86_64")
        client.devices.add_device("10.0.0.1", snmp_disable=True, icmp_device=icmp)
    """

    model_config = {"populate_by_name": True}

    os: str = "ping"
    """OS short name for the device. Defaults to 'ping'."""

    sys_name: str | None = Field(default=None, alias="sysName")
    """sysName for the device."""

    hardware: str | None = None
    """Device hardware."""


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
