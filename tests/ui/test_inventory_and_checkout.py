import pytest
from playwright.sync_api import Page, expect

from pages.cart_page import CartPage

pytestmark = pytest.mark.ui


def test_inventory_has_six_products(inventory):
    expect(inventory.items).to_have_count(6)


def test_sort_by_price_low_to_high(inventory):
    inventory.sort_by("lohi")
    prices = inventory.price_values()
    assert prices == sorted(prices)


def test_add_item_updates_cart_badge(inventory):
    inventory.add_to_cart("sauce-labs-backpack")
    expect(inventory.cart_badge).to_have_text("1")


@pytest.mark.smoke
def test_full_checkout_flow(page: Page, inventory):
    inventory.add_to_cart("sauce-labs-backpack")
    inventory.cart_link.click()
    cart = CartPage(page)
    expect(cart.items).to_have_count(1)
    cart.checkout("Test", "User", "12345")
    expect(cart.complete).to_have_text("Thank you for your order!")
