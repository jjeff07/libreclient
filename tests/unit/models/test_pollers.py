"""Unit tests for Pollers response models."""

from libreclient.models.pollers import PollersResponse


class TestPollersResponse:
    def test_pollers_list(self) -> None:
        data = {
            "status": "ok",
            "message": "",
            "count": 1,
            "pollers": [{"id": 1, "poller_name": "poller01"}],
        }
        r = PollersResponse.model_validate(data)
        assert r.data[0]["poller_name"] == "poller01"
