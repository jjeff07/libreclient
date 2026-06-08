"""Unit tests for Port Security routes."""

import asyncio

from py_librenms.models.port_security import PortSecurityResponse
from py_librenms.routes.port_security import PortSecurity


class TestGetAllPortSecurity:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "port_security": [],
        }
        route = PortSecurity(mock_client)
        result = asyncio.run(route.get_all_port_security())
        mock_client._get.assert_called_once_with("/port_security")
        assert isinstance(result, PortSecurityResponse)


class TestGetPortSecurityByPort:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "port_security": [],
        }
        route = PortSecurity(mock_client)
        result = asyncio.run(route.get_port_security_by_port(42))
        mock_client._get.assert_called_once_with("/port_security/port/42")
        assert isinstance(result, PortSecurityResponse)


class TestGetPortSecurityByHostname:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "port_security": [],
        }
        route = PortSecurity(mock_client)
        result = asyncio.run(route.get_port_security_by_hostname("sw1"))
        mock_client._get.assert_called_once_with("/port_security/device/sw1")
        assert isinstance(result, PortSecurityResponse)
