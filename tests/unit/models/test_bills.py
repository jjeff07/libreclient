"""Unit tests for Bills response models."""

from py_librenms.models.bills import BillHistoryResponse, BillsResponse


class TestBillsResponse:
    def test_bills_list(self) -> None:
        data = {
            "status": "ok",
            "message": "",
            "count": 1,
            "bills": [{"bill_id": 1, "bill_name": "Transit"}],
        }
        r = BillsResponse.model_validate(data)
        assert r.data[0]["bill_name"] == "Transit"

    def test_bills_defaults_empty(self) -> None:
        data = {"status": "ok", "message": "", "count": 0}
        r = BillsResponse.model_validate(data)
        assert r.data == []


class TestBillHistoryResponse:
    def test_history_list(self) -> None:
        data = {
            "status": "ok",
            "message": "",
            "count": 1,
            "bill_history": [{"bill_hist_id": 1, "bill_id": 1}],
        }
        r = BillHistoryResponse.model_validate(data)
        assert r.data[0]["bill_hist_id"] == 1
