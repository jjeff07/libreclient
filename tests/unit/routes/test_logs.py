"""Unit tests for Logs routes."""

import asyncio

from libreclient.models._base import ApiResponse
from libreclient.models.logs import LogsResponse
from libreclient.routes.logs import Logs


class TestListEventlog:
    def test_no_params(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "logs": [],
        }
        route = Logs(mock_client)
        result = asyncio.run(route.list_eventlog())
        mock_client._get.assert_called_once_with("/logs/eventlog", params={})
        assert isinstance(result, LogsResponse)

    def test_with_hostname(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "logs": [],
        }
        route = Logs(mock_client)
        asyncio.run(route.list_eventlog(hostname="sw1", limit=10))
        mock_client._get.assert_called_once_with(
            "/logs/eventlog/sw1", params={"limit": 10}
        )


class TestListSyslog:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "logs": [],
        }
        route = Logs(mock_client)
        asyncio.run(route.list_syslog())
        mock_client._get.assert_called_once_with("/logs/syslog", params={})


class TestListAlertlog:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "logs": [],
        }
        route = Logs(mock_client)
        asyncio.run(route.list_alertlog())
        mock_client._get.assert_called_once_with("/logs/alertlog", params={})


class TestSyslogsink:
    def test_posts_messages(self, mock_client) -> None:
        mock_client._post.return_value = {
            "status": "ok",
            "message": "accepted",
        }
        route = Logs(mock_client)
        result = asyncio.run(route.syslogsink([{"msg": "test"}]))
        mock_client._post.assert_called_once_with(
            "/syslogsink", json=[{"msg": "test"}]
        )
        assert isinstance(result, ApiResponse)

    def test_wraps_single_dict(self, mock_client) -> None:
        mock_client._post.return_value = {
            "status": "ok",
            "message": "accepted",
        }
        route = Logs(mock_client)
        asyncio.run(route.syslogsink({"msg": "single"}))
        mock_client._post.assert_called_once_with(
            "/syslogsink", json=[{"msg": "single"}]
        )


class TestAddEventlog:
    def test_posts_payload(self, mock_client) -> None:
        mock_client._post.return_value = {"status": "ok", "message": "added"}
        route = Logs(mock_client)
        result = asyncio.run(route.add_eventlog("sw1", "rebooted", "warning"))
        mock_client._post.assert_called_once_with(
            "/devices/sw1/eventlog",
            json={"text": "rebooted", "severity": "warning"},
        )
        assert isinstance(result, ApiResponse)
