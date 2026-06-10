"""Private async implementation for Logs routes — sync implementation."""

from ._synchronicity import synchronizer
from .logs import Logs

LogsSync = synchronizer.wrap(Logs, name="LogsSync", target_module=__name__)
