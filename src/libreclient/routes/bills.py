"""Private async implementation for Bills routes."""

from __future__ import annotations

import typing

from ..models import ApiResponse
from ..models.bills import BillHistoryResponse, BillsResponse
from ._types import ClientProtocol, _compact, _graph_params

_BILLS = "/bills"


class Bills:
    """Async route namespace bound to a client transport."""

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client

    async def list_bills(
        self, period: typing.Literal["previous"] | None = None
    ) -> BillsResponse:
        """Retrieve the list of bills currently in the system.

        Route: GET /api/v0/bills

        :param period: Optional period, e.g. 'previous'.
        """
        data = await self._client._get(_BILLS, params=_compact(period=period))
        return BillsResponse.model_validate(data)

    async def get_bill(
        self,
        bill_id: int | None = None,
        ref: str | None = None,
        custid: str | None = None,
        period: typing.Literal["previous"] | None = None,
    ) -> BillsResponse:
        """Retrieve a specific bill.

        Route: GET /api/v0/bills/:id  OR  /api/v0/bills?ref=:ref  OR  /api/v0/bills?custid=:custid

        :param bill_id: Optional bill ID.
        :param ref: Optional bill reference.
        :param custid: Optional customer ID.
        :param period: Optional period, e.g. 'previous'.
        """
        params = {}
        if period is not None:
            params["period"] = period
        if bill_id is not None:
            data = await self._client._get(f"/bills/{bill_id}", params=params)
            return BillsResponse.model_validate(data)
        if ref is not None:
            params["ref"] = ref
        if custid is not None:
            params["custid"] = custid
        data = await self._client._get(_BILLS, params=params)
        return BillsResponse.model_validate(data)

    async def get_bill_graph(
        self,
        bill_id: int,
        graph_type: str,
        from_time: str | None = None,
        to_time: str | None = None,
    ) -> bytes:
        """Retrieve a graph image associated with a bill.

        Route: GET /api/v0/bills/:id/graphs/:graph_type

        :param graph_type: Type of graph.
        :param from_time: Start time.
        :param to_time: End time.
        :param bill_id: Bill ID.
        """
        params = _graph_params(from_time, to_time)
        return await self._client._get_bytes(
            f"/bills/{bill_id}/graphs/{graph_type}", params=params
        )

    async def get_bill_graphdata(
        self,
        bill_id: int,
        graph_type: str,
        from_time: str | None = None,
        to_time: str | None = None,
        reducefactor: int | None = None,
    ) -> BillsResponse:
        """Retrieve the data used to draw a graph for a bill.

        Route: GET /api/v0/bills/:id/graphdata/:graph_type

        :param reducefactor: Optional data reduction factor.
        :param bill_id: Bill ID.
        :param graph_type: Type of graph.
        :param from_time: Start time.
        :param to_time: End time.
        """
        params = _graph_params(from_time, to_time, reducefactor=reducefactor)
        data = await self._client._get(
            f"/bills/{bill_id}/graphdata/{graph_type}", params=params
        )
        return BillsResponse.model_validate(data)

    async def get_bill_history(self, bill_id: int) -> BillHistoryResponse:
        """Retrieve the history of a specific bill.

        Route: GET /api/v0/bills/:id/history
        :param bill_id: Bill ID.
        """
        data = await self._client._get(f"/bills/{bill_id}/history")
        return BillHistoryResponse.model_validate(data)

    async def get_bill_history_graph(
        self, bill_id: int, bill_hist_id: int, graph_type: str
    ) -> bytes:
        """Retrieve a graph of a previous period of a bill.

        Route: GET /api/v0/bills/:id/history/:bill_hist_id/graphs/:graph_type

        :param bill_hist_id: Bill history entry ID.
        :param bill_id: Bill ID.
        :param graph_type: Type of graph.
        """
        return await self._client._get_bytes(
            f"/bills/{bill_id}/history/{bill_hist_id}/graphs/{graph_type}"
        )

    async def get_bill_history_graphdata(
        self, bill_id: int, bill_hist_id: int, graph_type: str
    ) -> BillsResponse:
        """Retrieve data for a graph of a previous period of a bill.

        Route: GET /api/v0/bills/:id/history/:bill_hist_id/graphdata/:graph_type
        :param bill_id: Bill ID.
        :param bill_hist_id: Bill history entry ID.
        :param graph_type: Type of graph.
        """
        data = await self._client._get(
            f"/bills/{bill_id}/history/{bill_hist_id}/graphdata/{graph_type}"
        )
        return BillsResponse.model_validate(data)

    async def delete_bill(self, bill_id: int) -> ApiResponse:
        """Delete a specific bill and all dependent data.

        Route: DELETE /api/v0/bills/:id
        :param bill_id: Bill ID to delete.
        """
        data = await self._client._delete(f"/bills/{bill_id}")
        return ApiResponse.model_validate(data)

    async def create_edit_bill(self, **kwargs) -> ApiResponse:
        """Create a new bill or update an existing one.

        Route: POST /api/v0/bills

        :param kwargs: Bill fields (bill_id for update, ports, bill_name, bill_day,
                       bill_type, bill_quota, bill_cdr, bill_custid, bill_ref, bill_notes).
        """
        data = await self._client._post(_BILLS, json=kwargs)
        return ApiResponse.model_validate(data)
