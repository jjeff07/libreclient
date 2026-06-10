"""Private async implementation for Routing routes — sync implementation."""

from ._synchronicity import synchronizer
from .routing import Routing

RoutingSync = synchronizer.wrap(
    Routing, name="RoutingSync", target_module=__name__
)
