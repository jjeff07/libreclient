"""Device Groups routes — sync implementation."""

from ._synchronicity import synchronizer
from .device_groups import DeviceGroups

DeviceGroupsSync = synchronizer.wrap(
    DeviceGroups, name="DeviceGroupsSync", target_module=__name__
)
