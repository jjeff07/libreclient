"""Private async implementation for PortGroups routes — sync implementation."""

from ._synchronicity import synchronizer
from .port_groups import PortGroups

PortGroupsSync = synchronizer.wrap(
    PortGroups, name="PortGroupsSync", target_module=__name__
)
