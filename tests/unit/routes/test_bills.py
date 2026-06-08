"""Unit tests for Bills routes."""

import asyncio

from py_librenms.models._base import ApiResponse
from py_librenms.models.bills import BillHistoryResponse, BillsResponse
from py_librenms.routes.bills import Bills


class TestListBills:
    def test_no_params(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "bills": [],
        }
        route = Bills(mock_client)
        result = asyncio.run(route.list_bills())
        mock_client._get.assert_called_once_with("/bills", params={})
        assert isinstance(result, BillsResponse)

    def test_with_period(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "bills": [],
        }
        route = Bills(mock_client)
        asyncio.run(route.list_bills(period="previous"))
        mock_client._get.assert_called_once_with(
            "/bills", params={"period": "previous"}
        )


class TestGetBill:
    def test_by_id(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 1,
            "bills": [],
        }
        route = Bills(mock_client)
        result = asyncio.run(route.get_bill(bill_id=5))
        mock_client._get.assert_called_once_with("/bills/5", params={})
        assert isinstance(result, BillsResponse)

    def test_by_ref(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 1,
            "bills": [],
        }
        route = Bills(mock_client)
        asyncio.run(route.get_bill(ref="REF123"))
        mock_client._get.assert_called_once_with(
            "/bills", params={"ref": "REF123"}
        )


class TestGetBillGraph:
    def test_returns_bytes(self, mock_client) -> None:
        route = Bills(mock_client)
        result = asyncio.run(route.get_bill_graph(1, "day"))
        mock_client._get_bytes.assert_called_once_with(
            "/bills/1/graphs/day", params={}
        )
        assert isinstance(result, bytes)


class TestGetBillHistory:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "bill_history": [],
        }
        route = Bills(mock_client)
        result = asyncio.run(route.get_bill_history(2))
        mock_client._get.assert_called_once_with("/bills/2/history")
        assert isinstance(result, BillHistoryResponse)


class TestDeleteBill:
    def test_calls_delete(self, mock_client) -> None:
        mock_client._delete.return_value = {
            "status": "ok",
            "message": "deleted",
        }
        route = Bills(mock_client)
        result = asyncio.run(route.delete_bill(3))
        mock_client._delete.assert_called_once_with("/bills/3")
        assert isinstance(result, ApiResponse)


class TestCreateEditBill:
    def test_posts_kwargs(self, mock_client) -> None:
        mock_client._post.return_value = {"status": "ok", "message": "created"}
        route = Bills(mock_client)
        result = asyncio.run(
            route.create_edit_bill(bill_name="Transit", bill_type="cdr")
        )
        mock_client._post.assert_called_once_with(
            "/bills", json={"bill_name": "Transit", "bill_type": "cdr"}
        )
        assert isinstance(result, ApiResponse)
