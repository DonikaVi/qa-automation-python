import pytest
from playwright.sync_api import Page, expect

from pages.inventory_page import InventoryPage

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_valid_login(page: Page, login_page):
    login_page.login("standard_user", "secret_sauce")
    InventoryPage(page).expect_loaded()


@pytest.mark.parametrize(
    "user, pwd, message",
    [
        ("locked_out_user", "secret_sauce", "locked out"),
        ("standard_user", "wrong_password", "do not match"),
        ("", "", "Username is required"),
        ("standard_user", "", "Password is required"),
    ],
    ids=["locked-out", "wrong-password", "empty-username", "empty-password"],
)
def test_invalid_login(login_page, user, pwd, message):
    login_page.login(user, pwd)
    login_page.expect_error(message)


def test_inventory_is_not_available_without_login(page: Page, ui_base_url):
    page.goto(f"{ui_base_url}/inventory.html")
    expect(page.locator("[data-test='error']")).to_be_visible()
