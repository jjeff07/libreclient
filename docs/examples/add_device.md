# Adding a Device

The `add_device` method provides a fully typed interface for adding devices to LibreNMS.
It supports SNMP v1/v2c/v3 discovery, ICMP-only (ping) devices, and all optional
configuration the LibreNMS API accepts.

## Quick Start

```python
from libreclient import LibreClient

client = LibreClient()
```

---

## Default (Auto-detect SNMP)

When `snmpver` is not specified, LibreNMS uses its global configuration defaults
and auto-detects the SNMP version during discovery.

```python
# Let LibreNMS use its configured defaults
response = client.devices.add_device("10.0.0.1")

# With a display name
response = client.devices.add_device(
    "switch-core-01.example.com",
    display="{{ $sysName }}",
)
```

---

## SNMP v1 / v2c

When using SNMP v1 or v2c, the `community` string is **required**.

=== "v2c"

    ```python
    response = client.devices.add_device(
        "10.0.0.1",
        snmpver="v2c",
        community="public",
    )
    ```

=== "v1"

    ```python
    response = client.devices.add_device(
        "10.0.0.1",
        snmpver="v1",
        community="public",
    )
    ```

---

## SNMP v3

When using SNMP v3, you must provide an `SnmpV3Credentials` instance via the
`snmp_v3` parameter.

```python
from libreclient.models import SnmpV3Credentials

creds = SnmpV3Credentials(
    authlevel="authPriv",
    authname="snmpuser",
    authpass="authSecret123",
    authalgo="SHA",
    cryptopass="cryptoSecret456",
    cryptoalgo="AES",
)

response = client.devices.add_device(
    "10.0.0.1",
    snmpver="v3",
    snmp_v3=creds,
)
```

### Auth Levels

| Level          | Description                      | Required Fields                                                |
|----------------|----------------------------------|----------------------------------------------------------------|
| `noAuthNoPriv` | No authentication, no encryption | —                                                              |
| `authNoPriv`   | Authentication only              | `authname`, `authpass`, `authalgo`                             |
| `authPriv`     | Authentication + encryption      | `authname`, `authpass`, `authalgo`, `cryptopass`, `cryptoalgo` |

### Supported Algorithms

- **Auth**: `MD5`, `SHA`, `SHA-224`, `SHA-256`, `SHA-384`, `SHA-512`
- **Crypto**: `AES`, `AES-192`, `AES-256`, `AES-256-C`, `DES`

---

## ICMP Only (Disable SNMP)

For devices that don't support SNMP, set `snmp_disable=True`. You can optionally
provide device metadata via the `icmp_device` parameter.

```python
from libreclient.models import IcmpOnlyDevice

response = client.devices.add_device(
    "10.0.0.50",
    snmp_disable=True,
)

# With device metadata
icmp = IcmpOnlyDevice(
    os="linux",
    sys_name="web-server-01",
    hardware="x86_64",
)

response = client.devices.add_device(
    "10.0.0.50",
    snmp_disable=True,
    icmp_device=icmp,
)
```

!!! note
When `snmp_disable=True` and no `icmp_device` is provided, the device OS
defaults to `"ping"`.

---

## Common Options

All examples above support these additional parameters:

```python
response = client.devices.add_device(
    "10.0.0.1",
    snmpver="v2c",
    community="public",
    # Display name (supports templates)
    display="{{ $hostname }}",
    # SNMP connection settings
    port=161,
    transport="udp",  # udp, tcp, udp6, tcp6
    # Port identification method
    port_association_mode="ifIndex",  # ifIndex, ifName, ifDescr, ifAlias
    # Distributed polling
    poller_group=1,
    # Location (mutually exclusive — use one or the other)
    location="DC1 Row A Rack 5",
    # location_id=42,
    # Skip discovery checks
    force_add=True,
    # Fall back to ping if SNMP fails
    ping_fallback=True,
)
```

| Parameter               | Type   | Default        | Description                                                                                          |
|-------------------------|--------|----------------|------------------------------------------------------------------------------------------------------|
| `display`               | `str`  | hostname       | Display name. Templates: `{{ $hostname }}`, `{{ $sysName }}`, `{{ $sysName_fallback }}`, `{{ $ip }}` |
| `port`                  | `int`  | config default | SNMP port                                                                                            |
| `transport`             | `str`  | config default | `udp`, `tcp`, `udp6`, `tcp6`                                                                         |
| `port_association_mode` | `str`  | `ifIndex`      | `ifIndex`, `ifName`, `ifDescr`, `ifAlias`                                                            |
| `poller_group`          | `int`  | `0`            | Poller group ID for distributed polling                                                              |
| `force_add`             | `bool` | `False`        | Skip all checks, add directly (credentials required)                                                 |
| `ping_fallback`         | `bool` | `False`        | Add as ping-only if SNMP fails                                                                       |
| `location`              | `str`  | —              | Set location by text                                                                                 |
| `location_id`           | `int`  | —              | Set location by ID                                                                                   |

!!! warning
You cannot specify both `location` and `location_id` — a `ValueError` will be raised.
When either is set, `override_sysLocation` is automatically enabled.

---

## API Reference

::: libreclient.routes.devices.Devices.add_device
handler: python
options:
show_root_heading: false
show_source: false
heading_level: 3

::: libreclient.models.devices.SnmpV3Credentials
handler: python
options:
show_root_heading: true
show_source: false
heading_level: 3

::: libreclient.models.devices.IcmpOnlyDevice
handler: python
options:
show_root_heading: true
show_source: false
heading_level: 3
