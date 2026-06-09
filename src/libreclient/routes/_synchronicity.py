"""Shared Synchronizer instance for all sync route wrappers."""

from synchronicity import Synchronizer

synchronizer = Synchronizer()

__all__ = ["synchronizer"]
