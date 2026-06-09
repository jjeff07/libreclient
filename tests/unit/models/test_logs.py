"""Unit tests for Logs response models."""

from libreclient.models.logs import LogsResponse


class TestLogsResponse:
    def test_logs_list(self) -> None:
        data = {
            "status": "ok",
            "message": "",
            "count": 1,
            "logs": [{"event_id": 1, "message": "Device up"}],
        }
        r = LogsResponse.model_validate(data)
        assert r.data[0]["message"] == "Device up"
