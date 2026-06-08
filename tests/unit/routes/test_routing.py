"""Unit tests for Routing routes."""

import asyncio

import pytest

from py_librenms.models._base import ApiResponse
from py_librenms.models.routing import RoutingResponse
from py_librenms.routes.routing import Routing


class TestListBgp:
    def test_no_params(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "routing": [],
        }
        route = Routing(mock_client)
        result = asyncio.run(route.list_bgp())
        mock_client._get.assert_called_once_with("/bgp", params={})
        assert isinstance(result, RoutingResponse)

    def test_with_hostname(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "routing": [],
        }
        route = Routing(mock_client)
        asyncio.run(route.list_bgp(hostname="router1"))
        mock_client._get.assert_called_once_with(
            "/bgp", params={"hostname": "router1"}
        )


class TestGetBgp:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 1,
            "routing": [],
        }
        route = Routing(mock_client)
        result = asyncio.run(route.get_bgp(5))
        mock_client._get.assert_called_once_with("/bgp/5")
        assert isinstance(result, RoutingResponse)


class TestEditBgpDescr:
    def test_posts_description(self, mock_client) -> None:
        mock_client._post.return_value = {"status": "ok", "message": "updated"}
        route = Routing(mock_client)
        result = asyncio.run(route.edit_bgp_descr(3, "Transit peer"))
        mock_client._post.assert_called_once_with(
            "/bgp/3", json={"bgp_descr": "Transit peer"}
        )
        assert isinstance(result, ApiResponse)


class TestListOspf:
    def test_calls_correct_path(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "routing": [],
        }
        route = Routing(mock_client)
        result = asyncio.run(route.list_ospf())
        mock_client._get.assert_called_once_with("/ospf", params={})
        assert isinstance(result, RoutingResponse)


class TestListVrf:
    def test_no_params(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "routing": [],
        }
        route = Routing(mock_client)
        result = asyncio.run(route.list_vrf())
        mock_client._get.assert_called_once_with("/routing/vrf", params={})
        assert isinstance(result, RoutingResponse)

    def test_with_hostname(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "routing": [],
        }
        route = Routing(mock_client)
        asyncio.run(route.list_vrf(hostname="r1"))
        mock_client._get.assert_called_once_with(
            "/routing/vrf", params={"hostname": "r1"}
        )

    def test_with_vrfname(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "routing": [],
        }
        route = Routing(mock_client)
        asyncio.run(route.list_vrf(vrfname="MGMT"))
        mock_client._get.assert_called_once_with(
            "/routing/vrf", params={"vrfname": "MGMT"}
        )

    def test_raises_if_both_set(self, mock_client) -> None:
        route = Routing(mock_client)
        with pytest.raises(
            ValueError, match="hostname and vrfname cannot both be set"
        ):
            asyncio.run(route.list_vrf(hostname="r1", vrfname="MGMT"))


class TestListIpAddresses:
    def test_all(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "routing": [],
        }
        route = Routing(mock_client)
        asyncio.run(route.list_ip_addresses())
        mock_client._get.assert_called_once_with("/resources/ip/addresses")

    def test_ipv4_only(self, mock_client) -> None:
        mock_client._get.return_value = {
            "status": "ok",
            "message": "",
            "count": 0,
            "routing": [],
        }
        route = Routing(mock_client)
        asyncio.run(route.list_ip_addresses(address_family="ipv4"))
        mock_client._get.assert_called_once_with(
            "/resources/ip/addresses/ipv4"
        )
