"""Private async implementation for Services routes."""

from __future__ import annotations

from typing import Literal

from ..models import ApiResponse
from ..models.services import ServicesResponse
from ._synchronicity import synchronizer
from ._types import ClientProtocol, _compact


class Services:
    """Async route namespace bound to a client transport."""

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client

    async def list_services(
        self, state: Literal[0, 1, 2] | None = None, type: str | None = None
    ) -> ServicesResponse:
        """Retrieve all services.

        Route: GET /api/v0/services

        :param state: Optional filter by state (valid options are 0=Ok, 1=Warning, 2=Critical).
        :param type: Optional filter by service type.
        """
        data = await self._client._get(
            "/services", params=_compact(state=state, type=type)
        )
        return ServicesResponse.model_validate(data)

    async def get_service_for_host(
        self,
        hostname: str,
        state: Literal[0, 1, 2] | None = None,
        type: str | None = None,
    ) -> ServicesResponse:
        """Retrieve services for a specific device.

        Route: GET /api/v0/services/:hostname

        :param hostname: Device hostname or ID.
        :param state: Optional filter by state (valid options are 0=Ok, 1=Warning, 2=Critical).
        :param type: Optional filter by service type.
        """
        data = await self._client._get(
            f"/services/{hostname}", params=_compact(state=state, type=type)
        )
        return ServicesResponse.model_validate(data)

    async def add_service_for_host(
        self,
        hostname: str,
        type: str,
        ip: str,
        desc: str | None = None,
        param: str | None = None,
        ignore: int | None = None,
    ) -> ApiResponse:
        """Add a service to a device.

        Route: POST /api/v0/services/:hostname

        :param ip: IP to check against.
        :param desc: Optional description.
        :param param: Optional check parameters.
        :param ignore: Optional ignore state.
        :param hostname: Device hostname or ID.
        :param type: Service check type.
        """
        payload: dict = {
            "type": type,
            "ip": ip,
            **_compact(desc=desc, param=param, ignore=ignore),
        }
        data = await self._client._post(f"/services/{hostname}", json=payload)
        return ApiResponse.model_validate(data)

    async def edit_service_from_host(
        self, service_id: int, **kwargs
    ) -> ApiResponse:
        """Edit a service.

        Route: PATCH /api/v0/services/:service_id

        :param service_id: Service ID to edit.
        :param kwargs: Service fields to update.
        """
        data = await self._client._patch(
            f"/services/{service_id}", json=kwargs
        )
        return ApiResponse.model_validate(data)

    async def delete_service_from_host(self, service_id: int) -> ApiResponse:
        """Delete a service from a device.

        Route: DELETE /api/v0/services/:service_id
        :param service_id: Service ID to delete.
        """
        data = await self._client._delete(f"/services/{service_id}")
        return ApiResponse.model_validate(data)


ServicesSync = synchronizer.wrap(
    Services, name="ServicesSync", target_module=__name__
)
