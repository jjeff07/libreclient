"""Private async implementation for Services routes — sync implementation."""

from ._synchronicity import synchronizer
from .services import Services


ServicesSync = synchronizer.wrap(
    Services, name="ServicesSync", target_module=__name__
)
