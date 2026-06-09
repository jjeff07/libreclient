"""Unit tests for Poller Groups routes."""

import asyncio

from libreclient.models.poller_groups import PollerGroupsResponse
from libreclient.routes.poller_groups import PollerGroups


class TestGetPollerGroup:
    def test_all_groups(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "poller_groups": [],
        }
        route = PollerGroups(mock_client)
        result = asyncio.run(route.get_poller_group())
        mock_client._get.assert_called_once_with("/poller_group")
        assert isinstance(result, PollerGroupsResponse)

    def test_specific_group(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 1,
            "poller_groups": [],
        }
        route = PollerGroups(mock_client)
        asyncio.run(route.get_poller_group(1))
        mock_client._get.assert_called_once_with("/poller_group/1")
