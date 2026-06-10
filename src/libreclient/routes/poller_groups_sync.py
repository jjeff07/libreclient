"""Private async implementation for PollerGroups routes — sync implementation."""

from ._synchronicity import synchronizer
from .poller_groups import PollerGroups

PollerGroupsSync = synchronizer.wrap(
    PollerGroups, name="PollerGroupsSync", target_module=__name__
)
