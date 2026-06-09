"""Unit tests for base response models."""

import pytest
from pydantic import ValidationError

from libreclient.models import ApiResponse, ApiResponseWithId, ListResponse


class TestApiResponse:
    def test_minimal_response(self) -> None:
        r = ApiResponse(status="ok", message="")
        assert r.status == "ok"
        assert r.message == ""

    def test_message_defaults_to_empty(self) -> None:
        r = ApiResponse(status="ok")
        assert r.message == ""

    def test_from_dict(self) -> None:
        data = {"status": "ok", "message": "Alert has been acknowledged"}
        r = ApiResponse.model_validate(data)
        assert r.status == "ok"
        assert r.message == "Alert has been acknowledged"

    def test_extra_fields_ignored(self) -> None:
        data = {"status": "ok", "message": "", "extra_stuff": 123}
        r = ApiResponse.model_validate(data)
        assert r.status == "ok"

    def test_missing_status_uses_default(self) -> None:
        r = ApiResponse.model_validate({"message": "oops"})
        assert r.status == "ok"


class TestApiResponseWithId:
    def test_includes_id(self) -> None:
        data = {"status": "ok", "message": "created", "id": 5}
        r = ApiResponseWithId.model_validate(data)
        assert r.id == 5
        assert r.status == "ok"

    def test_missing_id_raises(self) -> None:
        with pytest.raises(ValidationError):
            ApiResponseWithId.model_validate({"status": "ok", "message": ""})


class TestListResponse:
    def test_count_defaults_to_zero(self) -> None:
        r = ListResponse(status="ok")
        assert r.count == 0

    def test_count_from_data(self) -> None:
        r = ListResponse.model_validate(
            {"status": "ok", "message": "", "count": 42}
        )
        assert r.count == 42
