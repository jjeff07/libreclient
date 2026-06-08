"""Unit tests for Routing response models."""

from py_librenms.models.routing import RoutingResponse


class TestRoutingResponse:
    def test_routing_list(self) -> None:
        data = {
            "status": "ok",
            "message": "",
            "count": 1,
            "routing": [{"bgpPeer_id": 1, "bgpPeerState": "established"}],
        }
        r = RoutingResponse.model_validate(data)
        assert r.data[0]["bgpPeerState"] == "established"
