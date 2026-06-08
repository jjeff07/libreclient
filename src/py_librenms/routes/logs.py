"""Private async implementation for Logs routes."""

from __future__ import annotations

from ..models import ApiResponse
from ..models.logs import LogsResponse
from ._synchronicity import synchronizer
from ._types import ClientProtocol


class Logs:
    """Async route namespace bound to a client transport."""

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client

    async def list_eventlog(
        self,
        hostname: str | None = None,
        start: int | None = None,
        limit: int | None = None,
        from_time: str | None = None,
        to_time: str | None = None,
        sortorder: str | None = None,
    ) -> LogsResponse:
        """Retrieve event logs, optionally for a specific device.

        Route: GET /api/v0/logs/eventlog(/:hostname)

        :param hostname: Optional device hostname filter.
        :param start: Optional offset.
        :param limit: Optional record limit.
        :param from_time: Optional start time.
        :param to_time: Optional end time.
        :param sortorder: Optional sort 'ASC' or 'DESC'.
        """
        url = "/logs/eventlog"
        if hostname is not None:
            url += f"/{hostname}"
        params = _build_log_params(start, limit, from_time, to_time, sortorder)
        data = await self._client._get(url, params=params)
        return LogsResponse.model_validate(data)

    async def list_syslog(
        self,
        hostname: str | None = None,
        start: int | None = None,
        limit: int | None = None,
        from_time: str | None = None,
        to_time: str | None = None,
        sortorder: str | None = None,
    ) -> LogsResponse:
        """Retrieve syslog entries, optionally for a specific device.

        Route: GET /api/v0/logs/syslog(/:hostname)
        :param hostname: Optional device hostname filter.
        :param start: Optional offset.
        :param limit: Optional record limit.
        :param from_time: Optional start time.
        :param to_time: Optional end time.
        :param sortorder: Optional sort 'ASC' or 'DESC'.
        """
        url = "/logs/syslog"
        if hostname is not None:
            url += f"/{hostname}"
        params = _build_log_params(start, limit, from_time, to_time, sortorder)
        data = await self._client._get(url, params=params)
        return LogsResponse.model_validate(data)

    async def list_alertlog(
        self,
        hostname: str | None = None,
        start: int | None = None,
        limit: int | None = None,
        from_time: str | None = None,
        to_time: str | None = None,
        sortorder: str | None = None,
    ) -> LogsResponse:
        """Retrieve alert logs, optionally for a specific device.

        Route: GET /api/v0/logs/alertlog(/:hostname)
        :param hostname: Optional device hostname filter.
        :param start: Optional offset.
        :param limit: Optional record limit.
        :param from_time: Optional start time.
        :param to_time: Optional end time.
        :param sortorder: Optional sort 'ASC' or 'DESC'.
        """
        url = "/logs/alertlog"
        if hostname is not None:
            url += f"/{hostname}"
        params = _build_log_params(start, limit, from_time, to_time, sortorder)
        data = await self._client._get(url, params=params)
        return LogsResponse.model_validate(data)

    async def list_authlog(
        self,
        start: int | None = None,
        limit: int | None = None,
        from_time: str | None = None,
        to_time: str | None = None,
        sortorder: str | None = None,
    ) -> LogsResponse:
        """Retrieve authentication logs.

        Route: GET /api/v0/logs/authlog
        :param start: Optional offset.
        :param limit: Optional record limit.
        :param from_time: Optional start time.
        :param to_time: Optional end time.
        :param sortorder: Optional sort 'ASC' or 'DESC'.
        """
        params = _build_log_params(start, limit, from_time, to_time, sortorder)
        data = await self._client._get("/logs/authlog", params=params)
        return LogsResponse.model_validate(data)

    async def syslogsink(self, messages: list | dict) -> ApiResponse:
        """Accept JSON syslog messages and pass them for further processing.

        Route: POST /api/v0/syslogsink

        :param messages: A single message dict or a list of message dicts.
        """
        if isinstance(messages, dict):
            messages = [messages]
        data = await self._client._post("/syslogsink", json=messages)
        return ApiResponse.model_validate(data)

    async def add_eventlog(
        self, hostname: str, text: str, severity: str, type: str | None = None
    ) -> ApiResponse:
        """Add events to a device's eventlog.

        Route: POST /api/v0/devices/:hostname/eventlog

        :param text: Event log message.
        :param severity: Optional severity level (1-5).
        :param type: Optional event type.
        :param hostname: Device hostname.
        """
        payload: dict = {"text": text, "severity": severity}
        if type is not None:
            payload["type"] = type
        data = await self._client._post(f"/devices/{hostname}/eventlog", json=payload)
        return ApiResponse.model_validate(data)


def _build_log_params(start, limit, from_time, to_time, sortorder):
    params = {}
    if start is not None:
        params["start"] = start
    if limit is not None:
        params["limit"] = limit
    if from_time is not None:
        params["from"] = from_time
    if to_time is not None:
        params["to"] = to_time
    if sortorder is not None:
        params["sortorder"] = sortorder
    return params


LogsSync = synchronizer.wrap(Logs, name="LogsSync", target_module=__name__)
