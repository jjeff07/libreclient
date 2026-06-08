import asyncio

from py_librenms.client import LibreClientAsync, LibreClientSync
from py_librenms.config import LibreConfig


def test_sync_client_sets_headers_and_verify() -> None:
    cfg = LibreConfig(
        url="https://nms.example.com/api/v2",
        token="token-123",
        verify_ssl=False,
        api_version="v2",
    )

    client = LibreClientSync(**cfg.model_dump())
    try:
        assert client.base_url == "https://nms.example.com/api/v2"
        assert client._session.headers["X-Auth-Token"] == "token-123"
        assert client._session.verify is False
    finally:
        client.close()


def test_sync_client_routes_are_available() -> None:
    client = LibreClientSync(url="https://nms.example.com", token="x")
    try:
        assert hasattr(client.system, "ping")
        assert hasattr(client.devices, "list_devices")
        assert hasattr(client.alerts, "get_alert")
    finally:
        client.close()


def test_legacy_route_namespace_is_bound() -> None:
    client = LibreClientSync(url="https://nms.example.com", token="x")
    try:
        assert hasattr(client.devices, "get_device")
        assert hasattr(client.system, "ping")
    finally:
        client.close()


def test_async_client_close_awaits_session(monkeypatch) -> None:
    cfg = LibreConfig(
        url="https://nms.example.com",
        token="token-abc",
        verify_ssl=True,
        api_version="v0",
    )
    client = LibreClientAsync(**cfg.model_dump())

    state = {"closed": False}

    class FakeAsyncSession:
        async def close(self):  # noqa: S7503
            state["closed"] = True

    monkeypatch.setattr(client, "_session", FakeAsyncSession())

    asyncio.run(client.close())
    assert state["closed"] is True
