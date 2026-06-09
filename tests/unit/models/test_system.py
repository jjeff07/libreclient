"""Unit tests for System response models."""

from libreclient.models.system import SystemResponse


class TestSystemResponse:
    def test_system_list(self) -> None:
        data = {
            "status": "ok",
            "message": "",
            "system": [{"local_ver": "24.1.0", "db_schema": 2024}],
        }
        r = SystemResponse.model_validate(data)
        assert r.data[0]["local_ver"] == "24.1.0"
