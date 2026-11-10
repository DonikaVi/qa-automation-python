import os

import pytest
import requests

UI_BASE_URL = os.getenv("UI_BASE_URL", "https://www.saucedemo.com")
API_BASE_URL = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")


@pytest.fixture(scope="session")
def ui_base_url() -> str:
    return UI_BASE_URL


@pytest.fixture(scope="session")
def api() -> requests.Session:
    """Shared HTTP session for API tests."""
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    session.base_url = API_BASE_URL
    yield session
    session.close()


BOOKER_URL = os.getenv("BOOKER_URL", "https://restful-booker.herokuapp.com")
BOOKER_USER = os.getenv("BOOKER_USER", "admin")
BOOKER_PASSWORD = os.getenv("BOOKER_PASSWORD", "password123")  # public demo credentials
