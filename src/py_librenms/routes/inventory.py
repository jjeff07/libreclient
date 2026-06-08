"""Private async implementation for Inventory routes."""

from __future__ import annotations

from ..models.inventory import InventoryResponse
from ._synchronicity import synchronizer
from ._types import ClientProtocol


class Inventory:
    """Async route namespace bound to a client transport."""

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client

    async def get_inventory(
        self,
        hostname: str,
        ent_physical_class: str | None = None,
        ent_physical_contained_in: int | None = None,
    ) -> InventoryResponse:
        """Retrieve the inventory for a device (paginated / nested lookup).

        Route: GET /api/v0/inventory/:hostname

        :param hostname: Device hostname or id.
        :param ent_physical_class: Restrict by class (e.g. 'chassis').
        :param ent_physical_contained_in: Retrieve items contained within this entPhysicalIndex.
        """
        params = {}
        if ent_physical_class is not None:
            params["entPhysicalClass"] = ent_physical_class
        if ent_physical_contained_in is not None:
            params["entPhysicalContainedIn"] = ent_physical_contained_in
        data = await self._client._get(f"/inventory/{hostname}", params=params)
        return InventoryResponse.model_validate(data)

    async def get_inventory_for_device(
        self, hostname: str, ent_physical_contained_in: int | None = None
    ) -> InventoryResponse:
        """Retrieve the flattened inventory for a device (all items, regardless of nesting).

        Route: GET /api/v0/inventory/:hostname/all
        :param hostname: Device hostname or ID.
        :param ent_physical_contained_in: Optional filter by parent entity.
        """
        params = {}
        if ent_physical_contained_in is not None:
            params["entPhysicalContainedIn"] = ent_physical_contained_in
        data = await self._client._get(
            f"/inventory/{hostname}/all", params=params
        )
        return InventoryResponse.model_validate(data)


InventorySync = synchronizer.wrap(
    Inventory, name="InventorySync", target_module=__name__
)
