"""Private async implementation for System routes — sync implementation."""

from ._synchronicity import synchronizer
from .system import System

SystemSync = synchronizer.wrap(
    System, name="SystemSync", target_module=__name__
)
