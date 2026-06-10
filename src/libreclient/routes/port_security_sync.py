"""Private async implementation for PortSecurity routes — sync implementation."""

from ._synchronicity import synchronizer
from .port_security import PortSecurity


PortSecuritySync = synchronizer.wrap(
    PortSecurity, name="PortSecuritySync", target_module=__name__
)
