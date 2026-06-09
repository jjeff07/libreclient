"""Unit tests for Alerts response models."""

from libreclient.models.alerts import (
    AlertsResponse,
    AlertTemplateCreatedResponse,
    AlertTemplatesResponse,
    RulesResponse,
)


class TestAlertsResponse:
    def test_alerts_list(self) -> None:
        data = {
            "status": "ok",
            "message": "",
            "count": 2,
            "alerts": [
                {"id": 1, "state": 1, "hostname": "sw1"},
                {"id": 2, "state": 0, "hostname": "sw2"},
            ],
        }
        r = AlertsResponse.model_validate(data)
        assert r.count == 2
        assert len(r.data) == 2
        assert r.data[0]["hostname"] == "sw1"

    def test_alerts_defaults_empty(self) -> None:
        data = {"status": "ok", "message": "", "count": 0}
        r = AlertsResponse.model_validate(data)
        assert r.data == []


class TestRulesResponse:
    def test_rules_list(self) -> None:
        data = {
            "status": "ok",
            "message": "",
            "count": 1,
            "rules": [{"id": 1, "name": "test rule", "severity": "critical"}],
        }
        r = RulesResponse.model_validate(data)
        assert r.count == 1
        assert r.data[0]["name"] == "test rule"


class TestAlertTemplatesResponse:
    def test_templates_list(self) -> None:
        data = {
            "status": "ok",
            "message": "",
            "count": 1,
            "alert_templates": [{"id": 4, "name": "Default Alert Template"}],
        }
        r = AlertTemplatesResponse.model_validate(data)
        assert r.data[0]["name"] == "Default Alert Template"


class TestAlertTemplateCreatedResponse:
    def test_created_response(self) -> None:
        data = {
            "status": "ok",
            "message": "Alert template has been created",
            "id": 2,
        }
        r = AlertTemplateCreatedResponse.model_validate(data)
        assert r.id == 2
