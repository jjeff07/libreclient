"""Private async implementation for Portgroups routes — sync implementation."""

from ._synchronicity import synchronizer
from .portgroups import Portgroups


PortgroupsSync = synchronizer.wrap(
    Portgroups, name="PortgroupsSync", target_module=__name__
)
