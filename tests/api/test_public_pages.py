"""Availability checks for public web pages: status code, content type, key text."""
import pytest
import requests

pytestmark = [pytest.mark.api, pytest.mark.smoke]

PAGES = [
    ("https://www.saucedemo.com", "Swag Labs"),
    ("https://playwright.dev/python/", "Playwright"),
    ("https://docs.pytest.org/en/stable/", "pytest"),
    ("https://the-internet.herokuapp.com", "Welcome to the-internet"),
]


@pytest.mark.parametrize("page_url, expected_text", PAGES, ids=[p[0] for p in PAGES])
def test_page_is_available(page_url, expected_text):
    r = requests.get(page_url, timeout=15)
    assert r.status_code == 200
    assert "text/html" in r.headers["Content-Type"]
    assert expected_text in r.text
