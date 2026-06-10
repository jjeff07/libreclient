"""Private async implementation for Inventory routes — sync implementation."""

from ._synchronicity import synchronizer
from .inventory import Inventory


InventorySync = synchronizer.wrap(
    Inventory, name="InventorySync", target_module=__name__
)
