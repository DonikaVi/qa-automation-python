import pytest
from playwright.sync_api import Page

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.fixture
def login_page(page: Page, ui_base_url: str) -> LoginPage:
    return LoginPage(page, ui_base_url).open()


@pytest.fixture
def inventory(page: Page, login_page: LoginPage) -> InventoryPage:
    """Logged-in user on the inventory page."""
    login_page.login("standard_user", "secret_sauce")
    inv = InventoryPage(page)
    inv.expect_loaded()
    return inv
