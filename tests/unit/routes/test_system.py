"""Unit tests for System routes."""

import asyncio

from py_librenms.models._base import ApiResponse
from py_librenms.models.system import SystemResponse
from py_librenms.routes.system import System


class TestPing:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {"status": "ok", "message": ""}
        route = System(mock_client)
        result = asyncio.run(route.ping())
        mock_client._get.assert_called_once_with("/ping")
        assert isinstance(result, ApiResponse)


class TestSystem:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "system": [],
        }
        route = System(mock_client)
        result = asyncio.run(route.system())
        mock_client._get.assert_called_once_with("/system")
        assert isinstance(result, SystemResponse)
