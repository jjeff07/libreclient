"""Unit tests for Services response models."""

from py_librenms.models.services import ServicesResponse


class TestServicesResponse:
    def test_services_list(self) -> None:
        data = {
            "status": "ok",
            "message": "",
            "count": 1,
            "services": [
                {"service_id": 1, "service_type": "http", "service_status": 0}
            ],
        }
        r = ServicesResponse.model_validate(data)
        assert r.data[0]["service_type"] == "http"
