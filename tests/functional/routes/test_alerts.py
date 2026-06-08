"""Functional tests for Alerts routes."""

import pytest


class TestAlerts:
    def test_list_alerts(self, client):
        response = client.alerts.list_alerts()
        assert response.status == "ok"

    def test_list_alert_rules(self, client):
        response = client.alerts.list_alert_rules()
        assert response.status == "ok"

    def test_list_alert_templates(self, client):
        response = client.alerts.list_alert_templates()
        assert response.status == "ok"

    @pytest.mark.xfail(reason="May fail if no alerts exist")
    def test_get_alert(self, client):
        alerts = client.alerts.list_alerts()
        assert len(alerts.data) > 0
        alert_id = alerts.data[0]["id"]
        response = client.alerts.get_alert(alert_id)
        assert response.status == "ok"
