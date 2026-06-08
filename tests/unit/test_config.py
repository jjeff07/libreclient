import pytest
from pydantic import ValidationError

from py_librenms.config import LibreConfig


def test_config_defaults_without_api_in_url() -> None:
    cfg = LibreConfig(url="https://nms.example.com", token="secret")

    assert str(cfg.url) == "https://nms.example.com/"
    assert cfg.api_version == "v0"
    assert cfg.verify_ssl is True
    assert cfg.base_url == "https://nms.example.com/api/v0"


def test_config_extracts_api_version_from_url() -> None:
    cfg = LibreConfig(url="https://nms.example.com/api/v3", token="secret")

    assert str(cfg.url) == "https://nms.example.com/"
    assert cfg.api_version == "v3"
    assert cfg.base_url == "https://nms.example.com/api/v3"


def test_config_extracts_api_version_with_trailing_slash() -> None:
    cfg = LibreConfig(url="https://nms.example.com/some/base/api/v12/", token="secret")

    assert str(cfg.url) == "https://nms.example.com/some/base"
    assert cfg.api_version == "v12"
    assert cfg.base_url == "https://nms.example.com/some/base/api/v12"


def test_config_invalid_url_raises_validation_error() -> None:
    with pytest.raises(ValidationError):
        LibreConfig(url="not-a-url", token="secret")
