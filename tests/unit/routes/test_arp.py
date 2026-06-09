"""Unit tests for ARP routes."""

import asyncio

from libreclient.models.arp import ArpResponse
from libreclient.routes.arp import Arp


class TestListArp:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 1,
            "arp": [],
        }
        route = Arp(mock_client)
        result = asyncio.run(route.list_arp("10.0.0.1"))  # noqa: S1313
        mock_client._get.assert_called_once_with(
            "/resources/ip/arp/10.0.0.1",
            params={},  # noqa: S1313
        )
        assert isinstance(result, ArpResponse)

    def test_with_device_param(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "arp": [],
        }
        route = Arp(mock_client)
        asyncio.run(route.list_arp("all", device="sw1"))
        mock_client._get.assert_called_once_with(
            "/resources/ip/arp/all", params={"device": "sw1"}
        )
