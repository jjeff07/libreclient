"""Unit tests for Alerts routes."""

import asyncio

from py_librenms.models._base import ApiResponse
from py_librenms.models.alerts import (
    AlertsResponse,
    AlertTemplateCreatedResponse,
    AlertTemplatesResponse,
    RulesResponse,
)
from py_librenms.routes.alerts import Alerts


class TestGetAlert:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {"status": "ok", "message": "", "count": 1, "alerts": []}
        route = Alerts(mock_client)
        result = asyncio.run(route.get_alert(42))
        mock_client._get.assert_called_once_with("/alerts/42")
        assert isinstance(result, AlertsResponse)


class TestAckAlert:
    def test_calls_put_with_payload(self, mock_client) -> None:
        mock_client._put.return_value = {"status": "ok", "message": "Alert acknowledged"}
        route = Alerts(mock_client)
        result = asyncio.run(route.ack_alert(1, note="fixed", until_clear=False))
        mock_client._put.assert_called_once_with(
            "/alerts/1", json={"note": "fixed", "until_clear": False}
        )
        assert isinstance(result, ApiResponse)


class TestUnmuteAlert:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._put.return_value = {"status": "ok", "message": "unmuted"}
        route = Alerts(mock_client)
        result = asyncio.run(route.unmute_alert(5))
        mock_client._put.assert_called_once_with("/alerts/unmute/5")
        assert isinstance(result, ApiResponse)


class TestListAlerts:
    def test_no_params(self, mock_client) -> None:
        mock_client._get.return_value = {"status": "ok", "message": "", "count": 0, "alerts": []}
        route = Alerts(mock_client)
        result = asyncio.run(route.list_alerts())
        mock_client._get.assert_called_once_with("/alerts", params={})
        assert isinstance(result, AlertsResponse)

    def test_with_filters(self, mock_client) -> None:
        mock_client._get.return_value = {"status": "ok", "message": "", "count": 0, "alerts": []}
        route = Alerts(mock_client)
        asyncio.run(route.list_alerts(state=1, severity="critical"))
        mock_client._get.assert_called_once_with(
            "/alerts", params={"state": 1, "severity": "critical"}
        )


class TestGetAlertRule:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {"status": "ok", "message": "", "count": 1, "rules": []}
        route = Alerts(mock_client)
        result = asyncio.run(route.get_alert_rule(7))
        mock_client._get.assert_called_once_with("/rules/7")
        assert isinstance(result, RulesResponse)


class TestDeleteRule:
    def test_calls_delete(self, mock_client) -> None:
        mock_client._delete.return_value = {"status": "ok", "message": "removed"}
        route = Alerts(mock_client)
        result = asyncio.run(route.delete_rule(3))
        mock_client._delete.assert_called_once_with("/rules/3")
        assert isinstance(result, ApiResponse)


class TestListAlertRules:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {"status": "ok", "message": "", "count": 0, "rules": []}
        route = Alerts(mock_client)
        result = asyncio.run(route.list_alert_rules())
        mock_client._get.assert_called_once_with("/rules")
        assert isinstance(result, RulesResponse)


class TestAddRule:
    def test_posts_kwargs(self, mock_client) -> None:
        mock_client._post.return_value = {"status": "ok", "message": ""}
        route = Alerts(mock_client)
        asyncio.run(route.add_rule(name="test", severity="critical"))
        mock_client._post.assert_called_once_with(
            "/rules", json={"name": "test", "severity": "critical"}
        )


class TestEditRule:
    def test_puts_kwargs(self, mock_client) -> None:
        mock_client._put.return_value = {"status": "ok", "message": ""}
        route = Alerts(mock_client)
        asyncio.run(route.edit_rule(rule_id=1, name="updated"))
        mock_client._put.assert_called_once_with("/rules", json={"rule_id": 1, "name": "updated"})


class TestListAlertTemplates:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "alert_templates": [],
        }
        route = Alerts(mock_client)
        result = asyncio.run(route.list_alert_templates())
        mock_client._get.assert_called_once_with("/alert_templates")
        assert isinstance(result, AlertTemplatesResponse)


class TestAddAlertTemplate:
    def test_posts_payload(self, mock_client) -> None:
        mock_client._post.return_value = {"status": "ok", "message": "created", "id": 3}
        route = Alerts(mock_client)
        result = asyncio.run(route.add_alert_template(name="tmpl", template="body"))
        mock_client._post.assert_called_once_with(
            "/alert_templates", json={"name": "tmpl", "template": "body"}
        )
        assert isinstance(result, AlertTemplateCreatedResponse)
        assert result.id == 3
