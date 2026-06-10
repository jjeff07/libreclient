"""Private async implementation for Ports routes — sync implementation."""

from ._synchronicity import synchronizer
from .ports import Ports

PortsSync = synchronizer.wrap(Ports, name="PortsSync", target_module=__name__)
