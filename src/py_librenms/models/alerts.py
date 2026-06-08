"""Response models for Alerts routes."""

from __future__ import annotations

from pydantic import Field

from ._base import ApiResponseWithId, ListResponse


class AlertsResponse(ListResponse):
    """Response from get_alert / list_alerts."""

    data: list[dict] = Field(default_factory=list, validation_alias="alerts")


class RulesResponse(ListResponse):
    """Response from get_alert_rule / list_alert_rules."""

    data: list[dict] = Field(default_factory=list, validation_alias="rules")


class AlertTemplatesResponse(ListResponse):
    """Response from get_alert_template / list_alert_templates."""

    data: list[dict] = Field(default_factory=list, validation_alias="alert_templates")


class AlertTemplateCreatedResponse(ApiResponseWithId):
    """Response from add_alert_template (returns the new template id)."""
