"""Functional test configuration — requires a live LibreNMS instance.

Set LIBRENMS_URL and LIBRENMS_TOKEN as environment variables or in a .env file.
"""

import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

from py_librenms import LibreClientSync

# Load .env from project root
_env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(_env_path)


def pytest_collection_modifyitems(items):
    """Auto-mark all tests in this directory as 'functional'."""
    for item in items:
        if "functional" in str(item.fspath):
            item.add_marker(pytest.mark.functional)


@pytest.fixture(scope="session")
def client():
    """Create a sync client for the live LibreNMS instance."""
    url = os.environ.get("LIBRENMS_URL")
    token = os.environ.get("LIBRENMS_TOKEN")
    if not url or not token:
        pytest.skip(
            "LIBRENMS_URL and LIBRENMS_TOKEN must be set for functional tests"
        )
    c = LibreClientSync(url=url, token=token)
    yield c
    c.close()
