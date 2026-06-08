"""Unit tests for Switching routes."""

import asyncio

from py_librenms.models.switching import SwitchingResponse
from py_librenms.routes.switching import Switching


class TestListVlans:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "switching": [],
        }
        route = Switching(mock_client)
        result = asyncio.run(route.list_vlans())
        mock_client._get.assert_called_once_with("/resources/vlans")
        assert isinstance(result, SwitchingResponse)


class TestGetVlans:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "switching": [],
        }
        route = Switching(mock_client)
        result = asyncio.run(route.get_vlans("sw1"))
        mock_client._get.assert_called_once_with("/devices/sw1/vlans")
        assert isinstance(result, SwitchingResponse)


class TestListLinks:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "switching": [],
        }
        route = Switching(mock_client)
        result = asyncio.run(route.list_links())
        mock_client._get.assert_called_once_with("/resources/links")
        assert isinstance(result, SwitchingResponse)


class TestListFdb:
    def test_all(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "switching": [],
        }
        route = Switching(mock_client)
        asyncio.run(route.list_fdb())
        mock_client._get.assert_called_once_with("/resources/fdb")

    def test_by_mac(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "switching": [],
        }
        route = Switching(mock_client)
        asyncio.run(route.list_fdb(mac="aa:bb:cc:dd:ee:ff"))
        mock_client._get.assert_called_once_with(
            "/resources/fdb/aa:bb:cc:dd:ee:ff"
        )


class TestListNac:
    def test_all(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "switching": [],
        }
        route = Switching(mock_client)
        asyncio.run(route.list_nac())
        mock_client._get.assert_called_once_with("/resources/nac")
