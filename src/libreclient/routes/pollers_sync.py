"""Private async implementation for Pollers routes — sync implementation."""

from ._synchronicity import synchronizer
from .pollers import Pollers

PollersSync = synchronizer.wrap(
    Pollers, name="PollersSync", target_module=__name__
)
