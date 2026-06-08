"""Alerts routes — async implementation."""

from typing import Any, Literal

from ..models import ApiResponse
from ..models.alerts import (
    AlertsResponse,
    AlertTemplateCreatedResponse,
    AlertTemplatesResponse,
    RulesResponse,
)
from ._synchronicity import synchronizer
from ._types import ClientProtocol, _compact

_RULES = "/rules"
_ALERT_TEMPLATES = "/alert_templates"


class Alerts:
    """Alerts route namespace bound to a client transport."""

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client

    async def get_alert(self, alert_id: int) -> AlertsResponse:
        """Get details of an alert.

        Route: GET /api/v0/alerts/:id

        :param alert_id: The alert id.
        """
        data = await self._client._get(f"/alerts/{alert_id}")
        return AlertsResponse.model_validate(data)

    async def ack_alert(
        self, alert_id: int, note: str = "", until_clear: bool = True
    ) -> ApiResponse:
        """Acknowledge an alert.

        Route: PUT /api/v0/alerts/:id

        :param alert_id: The alert id.
        :param note: Note to add to the alert.
        :param until_clear: If False, the alert will re-alert if it worsens/changes.
        """
        data = await self._client._put(
            f"/alerts/{alert_id}", json={"note": note, "until_clear": until_clear}
        )
        return ApiResponse.model_validate(data)

    async def unmute_alert(self, alert_id: int) -> ApiResponse:
        """Unmute an alert.

        Route: PUT /api/v0/alerts/unmute/:id

        :param alert_id: The alert id.
        """
        data = await self._client._put(f"/alerts/unmute/{alert_id}")
        return ApiResponse.model_validate(data)

    async def list_alerts(
        self,
        state: Literal[0, 1, 2] | None = None,
        severity: Literal["ok", "warning", "critical"] | None = None,
        alert_rule: int | None = None,
        order: str | None = None,
    ) -> AlertsResponse:
        """List all alerts.

        Route: GET /api/v0/alerts

        :param state: Filter by state: 0=ok, 1=alert, 2=ack.
        :param severity: Filter by severity: 'ok', 'warning', 'critical'.
        :param alert_rule: Filter by alert rule ID.
        :param order: Order output, e.g. 'timestamp DESC'.
        """
        params = _compact(state=state, severity=severity, alert_rule=alert_rule, order=order)
        data = await self._client._get("/alerts", params=params)
        return AlertsResponse.model_validate(data)

    async def get_alert_rule(self, rule_id: int) -> RulesResponse:
        """Get the alert rule details.

        Route: GET /api/v0/rules/:id

        :param rule_id: The rule id.
        """
        data = await self._client._get(f"/rules/{rule_id}")
        return RulesResponse.model_validate(data)

    async def delete_rule(self, rule_id: int) -> ApiResponse:
        """Delete an alert rule by id.

        Route: DELETE /api/v0/rules/:id

        :param rule_id: The rule id.
        """
        data = await self._client._delete(f"/rules/{rule_id}")
        return ApiResponse.model_validate(data)

    async def list_alert_rules(self) -> RulesResponse:
        """List all alert rules.

        Route: GET /api/v0/rules
        """
        data = await self._client._get(_RULES)
        return RulesResponse.model_validate(data)

    async def add_rule(self, **kwargs) -> ApiResponse:
        """Add a new alert rule.

        Route: POST /api/v0/rules

        :param kwargs: Rule fields (devices, groups, locations, builder,
                       severity, disabled, name, notes, etc.).
        """
        data = await self._client._post(_RULES, json=kwargs)
        return ApiResponse.model_validate(data)

    async def edit_rule(self, **kwargs) -> ApiResponse:
        """Edit an existing alert rule.

        Route: PUT /api/v0/rules

        :param kwargs: Rule fields including rule_id to identify the rule.
        """
        data = await self._client._put(_RULES, json=kwargs)
        return ApiResponse.model_validate(data)

    async def get_alert_template(self, template_id: int) -> AlertTemplatesResponse:
        """Get the alert template details.

        Route: GET /api/v0/alert_templates/:id

        :param template_id: The alert template id.
        """
        data = await self._client._get(f"/alert_templates/{template_id}")
        return AlertTemplatesResponse.model_validate(data)

    async def list_alert_templates(self) -> AlertTemplatesResponse:
        """List all alert templates.

        Route: GET /api/v0/alert_templates
        """
        data = await self._client._get(_ALERT_TEMPLATES)
        return AlertTemplatesResponse.model_validate(data)

    async def add_alert_template(
        self,
        name: str,
        template: str,
        title: str | None = None,
        title_rec: str | None = None,
        alert_rules: list | None = None,
    ) -> AlertTemplateCreatedResponse:
        """Add a new alert template.

        Route: POST /api/v0/alert_templates

        :param name: Name for the template.
        :param template: Template code used to generate the alert message.
        :param title: Title used when an alert is generated.
        :param title_rec: Title used when an alert has recovered.
        :param alert_rules: List of rule_ids this template applies to.
        """
        payload: dict[str, Any] = {
            "name": name,
            "template": template,
            **_compact(title=title, title_rec=title_rec, alert_rules=alert_rules),
        }
        data = await self._client._post(_ALERT_TEMPLATES, json=payload)
        return AlertTemplateCreatedResponse.model_validate(data)

    async def edit_alert_template(
        self,
        template_id: int,
        name: str,
        template: str,
        title: str | None = None,
        title_rec: str | None = None,
        alert_rules: list | None = None,
    ) -> ApiResponse:
        """Edit an existing alert template.

        Route: POST /api/v0/alert_templates

        :param template_id: The template id to update.
        :param name: Name for the template.
        :param template: Template code used to generate the alert message.
        :param title: Title used when an alert is generated.
        :param title_rec: Title used when an alert has recovered.
        :param alert_rules: List of rule_ids this template applies to.
        """
        payload: dict[str, Any] = {
            "template_id": template_id,
            "name": name,
            "template": template,
            **_compact(title=title, title_rec=title_rec, alert_rules=alert_rules),
        }
        data = await self._client._post(_ALERT_TEMPLATES, json=payload)
        return ApiResponse.model_validate(data)


AlertsSync = synchronizer.wrap(Alerts, name="AlertsSync", target_module=__name__)
