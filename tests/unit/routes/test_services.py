"""Unit tests for Services routes."""

import asyncio

from py_librenms.models._base import ApiResponse
from py_librenms.models.services import ServicesResponse
from py_librenms.routes.services import Services


class TestListServices:
    def test_no_params(self, mock_client) -> None:
        mock_client._get.return_value = {"status": "ok", "message": "", "count": 0, "services": []}
        route = Services(mock_client)
        result = asyncio.run(route.list_services())
        mock_client._get.assert_called_once_with("/services", params={})
        assert isinstance(result, ServicesResponse)

    def test_with_state_filter(self, mock_client) -> None:
        mock_client._get.return_value = {"status": "ok", "message": "", "count": 0, "services": []}
        route = Services(mock_client)
        asyncio.run(route.list_services(state=2, type="http"))
        mock_client._get.assert_called_once_with("/services", params={"state": 2, "type": "http"})


class TestGetServiceForHost:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {"status": "ok", "message": "", "count": 0, "services": []}
        route = Services(mock_client)
        result = asyncio.run(route.get_service_for_host("web01"))
        mock_client._get.assert_called_once_with("/services/web01", params={})
        assert isinstance(result, ServicesResponse)


class TestAddServiceForHost:
    def test_posts_payload(self, mock_client) -> None:
        mock_client._post.return_value = {"status": "ok", "message": "created"}
        route = Services(mock_client)
        result = asyncio.run(route.add_service_for_host("web01", "http", "10.0.0.1"))  # noqa: S1313
        mock_client._post.assert_called_once_with(
            "/services/web01", json={"type": "http", "ip": "10.0.0.1"}  # noqa: S1313
        )
        assert isinstance(result, ApiResponse)


class TestDeleteServiceFromHost:
    def test_calls_delete(self, mock_client) -> None:
        mock_client._delete.return_value = {"status": "ok", "message": "deleted"}
        route = Services(mock_client)
        result = asyncio.run(route.delete_service_from_host(5))
        mock_client._delete.assert_called_once_with("/services/5")
        assert isinstance(result, ApiResponse)
