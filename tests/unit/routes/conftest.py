"""Shared fixtures for route unit tests."""

from unittest.mock import AsyncMock

import pytest


class MockClient:
    """Fake client that records calls to HTTP helper methods."""

    def __init__(self):
        self._get = AsyncMock()
        self._post = AsyncMock()
        self._put = AsyncMock()
        self._patch = AsyncMock()
        self._delete = AsyncMock()
        self._get_bytes = AsyncMock(return_value=b"\x89PNG")


@pytest.fixture
def mock_client():
    return MockClient()
