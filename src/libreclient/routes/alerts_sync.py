"""Alerts routes — sync implementation."""

from ._synchronicity import synchronizer
from .alerts import Alerts


AlertsSync = synchronizer.wrap(
    Alerts, name="AlertsSync", target_module=__name__
)
