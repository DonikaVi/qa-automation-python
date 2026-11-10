"""Same site, mobile viewport (Pixel 7 emulation)."""
import pytest
from playwright.sync_api import Page, expect

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

pytestmark = pytest.mark.ui


@pytest.fixture
def mobile_page(playwright):
    browser = playwright.chromium.launch()
    context = browser.new_context(**playwright.devices["Pixel 7"])
    page = context.new_page()
    yield page
    context.close()
    browser.close()


def test_viewport_is_mobile(mobile_page: Page, ui_base_url):
    mobile_page.goto(ui_base_url)
    assert mobile_page.viewport_size["width"] < 500


def test_login_and_cart_on_mobile(mobile_page: Page, ui_base_url):
    LoginPage(mobile_page, ui_base_url).open().login("standard_user", "secret_sauce")
    inv = InventoryPage(mobile_page)
    inv.expect_loaded()
    inv.add_to_cart("sauce-labs-backpack")
    expect(inv.cart_badge).to_have_text("1")
