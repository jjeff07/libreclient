"""Unit tests for Inventory routes."""

import asyncio

from py_librenms.models.inventory import InventoryResponse
from py_librenms.routes.inventory import Inventory


class TestGetInventory:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {"status": "ok", "message": "", "count": 0, "inventory": []}
        route = Inventory(mock_client)
        result = asyncio.run(route.get_inventory("sw1"))
        mock_client._get.assert_called_once_with("/inventory/sw1", params={})
        assert isinstance(result, InventoryResponse)

    def test_with_class_filter(self, mock_client) -> None:
        mock_client._get.return_value = {"status": "ok", "message": "", "count": 0, "inventory": []}
        route = Inventory(mock_client)
        asyncio.run(route.get_inventory("sw1", ent_physical_class="chassis"))
        mock_client._get.assert_called_once_with(
            "/inventory/sw1", params={"entPhysicalClass": "chassis"}
        )


class TestGetInventoryForDevice:
    def test_calls_all_path(self, mock_client) -> None:
        mock_client._get.return_value = {"status": "ok", "message": "", "count": 0, "inventory": []}
        route = Inventory(mock_client)
        result = asyncio.run(route.get_inventory_for_device("sw1"))
        mock_client._get.assert_called_once_with("/inventory/sw1/all", params={})
        assert isinstance(result, InventoryResponse)
