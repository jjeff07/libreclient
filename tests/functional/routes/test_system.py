"""Functional tests for System routes."""


class TestSystem:
    def test_ping(self, client):
        response = client.system.ping()
        assert response.message == "pong"

    def test_system_info(self, client):
        response = client.system.system()
        assert response.status == "ok"
