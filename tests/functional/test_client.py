"""Functional tests for client connectivity."""


class TestClientConnection:
    def test_client_creates_successfully(self, client):
        """Client should instantiate without error."""
        assert client is not None

    def test_ping(self, client):
        """System ping should return 'pong'."""
        response = client.system.ping()
        assert response.message == "pong"
