"""Device inventory script — list devices in a table.

Usage::

    uv run python -m libreclient.scripts.device_inventory
    uv run python -m libreclient.scripts.device_inventory --columns hostname,ip,os
    uv run python -m libreclient.scripts.device_inventory --add-columns serial,notes
    uv run python -m libreclient.scripts.device_inventory --rm-columns disabled,last_polled
    uv run python -m libreclient.scripts.device_inventory --sort hostname:desc
    uv run python -m libreclient.scripts.device_inventory --format csv --output devices.csv
    uv run python -m libreclient.scripts.device_inventory --show-secrets --columns community
"""

from __future__ import annotations

import csv
import io
import json
import sys

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from libreclient import LibreClientSync

# Default columns in display order
DEFAULT_COLUMNS: list[str] = [
    "device_id",
    "hostname",
    "sysName",
    "display",
    "ip",
    "location",
    "snmpver",
    "serial",
    "type",
    "os",
    "version",
    "hardware",
    "status",
    "disabled",
    "last_polled",
    "last_polled_timetaken",
]

# Column rename mapping for display headers
COLUMN_ALIASES: dict[str, str] = {
    "device_id": "id",
    "last_polled_timetaken": "poll_time",
}

# Sensitive fields — require --show-secrets to display
SECRET_FIELDS: set[str] = {"community", "authpass", "cryptopass"}


# All known device fields (for case-insensitive matching)
_KNOWN_FIELDS: list[str] = [
    "device_id",
    "inserted",
    "hostname",
    "sysName",
    "display",
    "display_template",
    "ip",
    "overwrite_ip",
    "community",
    "authlevel",
    "authname",
    "authpass",
    "authalgo",
    "cryptopass",
    "cryptoalgo",
    "snmpver",
    "port",
    "transport",
    "timeout",
    "retries",
    "snmp_disable",
    "bgpLocalAs",
    "sysObjectID",
    "sysDescr",
    "sysContact",
    "version",
    "hardware",
    "features",
    "location_id",
    "os",
    "status",
    "status_reason",
    "ignore",
    "disabled",
    "uptime",
    "agent_uptime",
    "last_polled",
    "last_poll_attempted",
    "last_polled_timetaken",
    "last_discovered_timetaken",
    "last_discovered",
    "last_ping",
    "last_ping_timetaken",
    "purpose",
    "type",
    "serial",
    "icon",
    "poller_group",
    "override_sysLocation",
    "notes",
    "port_association_mode",
    "max_depth",
    "disable_notify",
    "ignore_status",
    "mtu_status",
    "dependency_parent_id",
    "dependency_parent_hostname",
    "location",
    "lat",
    "lng",
]

# Build case-insensitive lookup: lowercase -> actual field name
_FIELD_LOOKUP: dict[str, str] = {f.lower(): f for f in _KNOWN_FIELDS}


def _normalize_field(name: str) -> str:
    """Resolve a field name case-insensitively. Returns original if not found."""
    return _FIELD_LOOKUP.get(name.lower().strip(), name.strip())


class InventorySettings(BaseSettings):
    """Device inventory CLI settings."""

    model_config = SettingsConfigDict(
        cli_parse_args=True,
        cli_prog_name="device-inventory",
        cli_kebab_case=True,
    )

    columns: str | None = Field(
        default=None,
        description="Override default columns (comma-separated).",
    )
    add_columns: str | None = Field(
        default=None,
        description="Add columns to the defaults (comma-separated).",
    )
    rm_columns: str | None = Field(
        default=None,
        description="Remove columns from the defaults (comma-separated).",
    )
    sort: str | None = Field(
        default=None,
        description="Sort by column. Format: 'column' or 'column:asc' / 'column:desc'. Default direction is asc.",
    )
    show_secrets: bool = Field(
        default=False,
        description="Show sensitive fields (community, authpass, cryptopass). Required to display these columns.",
    )
    format: str = Field(
        default="rich",
        description="Output format: rich (default), plain, md, json, csv.",
    )
    output: str | None = Field(
        default=None,
        description="Write output to a file instead of stdout.",
    )

    def get_columns(self) -> list[str]:
        """Parse comma-separated column string into a list."""
        if self.columns:
            return [
                _normalize_field(c)
                for c in self.columns.split(",")
                if c.strip()
            ]
        return []

    def get_add_columns(self) -> list[str]:
        """Parse comma-separated add_columns string into a list."""
        if self.add_columns:
            return [
                _normalize_field(c)
                for c in self.add_columns.split(",")
                if c.strip()
            ]
        return []

    def get_rm_columns(self) -> list[str]:
        """Parse comma-separated rm_columns string into a list."""
        if self.rm_columns:
            return [
                _normalize_field(c)
                for c in self.rm_columns.split(",")
                if c.strip()
            ]
        return []


def _resolve_columns(settings: InventorySettings) -> list[str]:
    """Resolve the final column list from CLI flags."""
    override = settings.get_columns()
    if override:
        # Explicit override — always include device_id first
        cols = list(dict.fromkeys(["device_id", *override]))
    else:
        cols = list(DEFAULT_COLUMNS)

    # Add extra columns (preserving order, deduplicating)
    for col in settings.get_add_columns():
        if col not in cols:
            cols.append(col)

    # Remove columns (never remove device_id)
    for col in settings.get_rm_columns():
        if col in cols and col != "device_id":
            cols.remove(col)

    # Strip secret fields unless --show-secrets is set
    if not settings.show_secrets:
        cols = [c for c in cols if c not in SECRET_FIELDS]

    return cols


def _format_value(key: str, value) -> str:
    """Format a device field value for display."""
    if key == "status":
        if value == 1:
            return "up"
        if value == 0:
            return "down"
        return str(value) if value is not None else ""
    if key == "last_polled_timetaken":
        if value is not None:
            return f"{float(value):.2f}s"
        return ""
    if value is None:
        return ""
    return str(value)


def _get_header(key: str) -> str:
    """Get display header for a column key."""
    return COLUMN_ALIASES.get(key, key)


def _render_rich(
    devices: list[dict], columns: list[str], base_url: str
) -> None:
    """Render table using rich with hyperlinked device IDs."""
    from rich.console import Console
    from rich.table import Table

    console = Console()
    table = Table(title="Device Inventory", show_lines=False)

    for col in columns:
        table.add_column(_get_header(col), overflow="fold")

    for device in devices:
        row: list[str] = []
        for col in columns:
            value = device.get(col)
            formatted = _format_value(col, value)

            if col == "device_id" and value is not None:
                # Rich hyperlink: [link=URL]text[/link]
                url = f"{base_url}device/{value}"
                formatted = f"[link={url}]{formatted}[/link]"

            row.append(formatted)
        table.add_row(*row)

    console.print(table)
    console.print(
        "\n[dim]💡 Device IDs are hyperlinked → Ctrl+click to open in LibreNMS[/dim]"
    )


def _render_plain(devices: list[dict], columns: list[str]) -> None:
    """Render table as plain text."""
    headers = [_get_header(col) for col in columns]

    # Calculate column widths
    widths = [len(h) for h in headers]
    rows: list[list[str]] = []
    for device in devices:
        row = [_format_value(col, device.get(col)) for col in columns]
        rows.append(row)
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    # Print header
    header_line = "  ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    print(header_line)
    print("  ".join("-" * w for w in widths))

    # Print rows
    for row in rows:
        print("  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)))


def _render_md(devices: list[dict], columns: list[str]) -> str:
    """Render table as Markdown."""
    headers = [_get_header(col) for col in columns]
    lines = ["| " + " | ".join(headers) + " |"]
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for device in devices:
        row = [_format_value(col, device.get(col)) for col in columns]
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def _render_json(devices: list[dict], columns: list[str]) -> str:
    """Render as JSON array with only selected columns."""
    filtered = [
        {col: device.get(col) for col in columns} for device in devices
    ]
    return json.dumps(filtered, indent=2)


def _render_csv(devices: list[dict], columns: list[str]) -> str:
    """Render as CSV."""
    output = io.StringIO()
    headers = [_get_header(col) for col in columns]
    writer = csv.writer(output)
    writer.writerow(headers)
    for device in devices:
        writer.writerow(
            [_format_value(col, device.get(col)) for col in columns]
        )
    return output.getvalue()


def _sort_devices(devices: list[dict], sort_spec: str | None) -> list[dict]:
    """Sort devices by a column. Format: 'column' or 'column:asc'/'column:desc'."""
    if not sort_spec:
        return devices

    parts = sort_spec.split(":", 1)
    column = _normalize_field(parts[0])
    direction = parts[1].strip().lower() if len(parts) > 1 else "asc"
    reverse = direction == "desc"

    def sort_key(device: dict):
        val = device.get(column)
        if val is None:
            return ("",) if not reverse else ("\xff",)
        if isinstance(val, (int, float)):
            return (val,)
        return (str(val).lower(),)

    return sorted(devices, key=sort_key, reverse=reverse)


# TODO: Refactor
def main() -> None:  # complexipy: ignore
    """Run the device inventory script."""
    settings = InventorySettings()
    columns = _resolve_columns(settings)

    client = LibreClientSync()
    response = client.devices.list_devices()

    if not response.data:
        print("No devices found.")
        sys.exit(0)

    devices = _sort_devices(response.data, settings.sort)

    # Derive base URL from client config for hyperlinks
    base_url = str(client.url).rstrip("/") + "/"

    fmt = settings.format.lower()

    # Text-based formats that can be written to file
    if fmt in ("md", "json", "csv"):
        if fmt == "md":
            content = _render_md(devices, columns)
        elif fmt == "json":
            content = _render_json(devices, columns)
        else:
            content = _render_csv(devices, columns)

        if settings.output:
            with open(settings.output, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Written to {settings.output}")
        else:
            print(content)
        return

    # Plain text table
    if fmt == "plain":
        if settings.output:
            from contextlib import redirect_stdout

            with (
                open(settings.output, "w", encoding="utf-8") as f,
                redirect_stdout(f),
            ):
                _render_plain(devices, columns)
            print(f"Written to {settings.output}")
        else:
            _render_plain(devices, columns)
        return

    # Rich table (default)
    try:
        import rich  # noqa: F401

        if settings.output:
            from rich.console import Console
            from rich.table import Table

            with open(settings.output, "w", encoding="utf-8") as f:
                console = Console(file=f, force_terminal=False)
                table = Table(title="Device Inventory", show_lines=False)
                for col in columns:
                    table.add_column(_get_header(col), overflow="fold")
                for device in devices:
                    row: list[str] = []
                    for col in columns:
                        value = device.get(col)
                        row.append(_format_value(col, value))
                    table.add_row(*row)
                console.print(table)
            print(f"Written to {settings.output}")
        else:
            _render_rich(devices, columns, base_url)
    except ImportError:
        _render_plain(devices, columns)


if __name__ == "__main__":
    main()
