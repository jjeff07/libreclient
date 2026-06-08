"""Functional tests for Index routes."""


class TestIndex:
    def test_list_api_endpoints(self, client):
        response = client.index.list_api_endpoints()
        assert len(response.endpoints) > 0
