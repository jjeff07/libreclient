"""Unit tests for Inventory response models."""

from py_librenms.models.inventory import InventoryResponse


class TestInventoryResponse:
    def test_inventory_list(self) -> None:
        data = {
            "status": "ok",
            "message": "",
            "count": 1,
            "inventory": [
                {"entPhysicalIndex": 1, "entPhysicalClass": "chassis"}
            ],
        }
        r = InventoryResponse.model_validate(data)
        assert r.data[0]["entPhysicalClass"] == "chassis"
