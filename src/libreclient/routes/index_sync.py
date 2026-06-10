"""Private async implementation for Index routes — sync implementation."""

from ._synchronicity import synchronizer
from .index import Index

IndexSync = synchronizer.wrap(Index, name="IndexSync", target_module=__name__)
