"""Unit tests for Switching response models."""

from libreclient.models.switching import SwitchingResponse


class TestSwitchingResponse:
    def test_switching_list(self) -> None:
        data = {
            "status": "ok",
            "message": "",
            "count": 1,
            "switching": [{"vlan_id": 100, "vlan_name": "Management"}],
        }
        r = SwitchingResponse.model_validate(data)
        assert r.data[0]["vlan_name"] == "Management"
