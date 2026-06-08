"""Unit tests for Pollers routes."""

import asyncio

from py_librenms.models.pollers import PollersResponse
from py_librenms.routes.pollers import Pollers


class TestListPollers:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "pollers": [],
        }
        route = Pollers(mock_client)
        result = asyncio.run(route.list_pollers())
        mock_client._get.assert_called_once_with("/pollers")
        assert isinstance(result, PollersResponse)


class TestListPollerLog:
    def test_no_params(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "pollers": [],
        }
        route = Pollers(mock_client)
        asyncio.run(route.list_poller_log())
        mock_client._get.assert_called_once_with("/pollers/log", params={})

    def test_unpolled_filter(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "pollers": [],
        }
        route = Pollers(mock_client)
        asyncio.run(route.list_poller_log(unpolled=True))
        mock_client._get.assert_called_once_with(
            "/pollers/log", params={"unpolled": 1}
        )
