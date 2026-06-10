"""Private async implementation for Devices routes — sync implementation."""

from ._synchronicity import synchronizer
from .devices import Devices


DevicesSync = synchronizer.wrap(
    Devices, name="DevicesSync", target_module=__name__
)
