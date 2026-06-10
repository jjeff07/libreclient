"""Private async implementation for Bills routes — sync implementation."""

from ._synchronicity import synchronizer
from .bills import Bills


BillsSync = synchronizer.wrap(
    Bills, name="BillsSync", target_module=__name__
)
