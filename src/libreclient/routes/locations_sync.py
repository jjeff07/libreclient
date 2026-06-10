"""Private async implementation for Locations routes — sync implementation."""

from ._synchronicity import synchronizer
from .locations import Locations

LocationsSync = synchronizer.wrap(
    Locations, name="LocationsSync", target_module=__name__
)
