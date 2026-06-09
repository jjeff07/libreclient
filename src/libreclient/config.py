"""
LibreNMS client configuration via Pydantic Settings.
"""

import re

from pydantic import AnyHttpUrl, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class LibreConfig(BaseSettings):
    """Configuration for the LibreNMS API client.

    Values can be supplied directly or via environment variables prefixed
    with ``LIBRENMS_`` (e.g. ``LIBRENMS_URL``, ``LIBRENMS_TOKEN``).
    """

    model_config = SettingsConfigDict(
        env_prefix="LIBRENMS_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    url: AnyHttpUrl = Field(
        ...,
        description="Base URL of the LibreNMS instance, e.g. https://librenms.example.com",
    )
    token: str = Field(..., description="LibreNMS API token (X-Auth-Token)")
    verify_ssl: bool = Field(True, description="Verify TLS/SSL certificates")
    api_version: str = Field(
        "v0", description="API version segment, e.g. 'v0'"
    )

    @model_validator(mode="before")
    @classmethod
    def normalize_url_and_api_version(cls, data):
        """If `url` includes `/api/vN`, strip it from url and set `api_version`."""
        if not isinstance(data, dict):
            return data

        raw_url = data.get("url")
        if raw_url is None:
            return data

        url_str = str(raw_url)
        # Find embedded API version path, e.g. https://host/api/v1
        match = re.search(r"/api/(v\d+)(?:/|$)", url_str)
        if not match:
            return data

        data["api_version"] = match.group(1)
        data["url"] = url_str[: match.start()].rstrip("/")
        return data

    @property
    def base_url(self) -> str:
        """Full API base URL, e.g. https://librenms.example.com/api/v0."""
        return f"{str(self.url).rstrip('/')}/api/{self.api_version}"
