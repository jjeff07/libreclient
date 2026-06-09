"""Unit tests for Index routes."""

import asyncio

from libreclient.models.index import IndexResponse
from libreclient.routes.index import Index


class TestListApiEndpoints:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {
            "list_bgp": "http://localhost/api/v0/bgp"
        }
        route = Index(mock_client)
        result = asyncio.run(route.list_api_endpoints())
        mock_client._get.assert_called_once_with("")
        assert isinstance(result, IndexResponse)
