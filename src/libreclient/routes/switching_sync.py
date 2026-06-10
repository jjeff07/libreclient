"""Private async implementation for Switching routes — sync implementation."""

from ._synchronicity import synchronizer
from .switching import Switching


SwitchingSync = synchronizer.wrap(
    Switching, name="SwitchingSync", target_module=__name__
)
