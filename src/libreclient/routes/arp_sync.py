"""ARP routes — sync implementation."""

from ._synchronicity import synchronizer
from .arp import Arp

ArpSync = synchronizer.wrap(Arp, name="ArpSync", target_module=__name__)
