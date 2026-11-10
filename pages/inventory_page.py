import re

from playwright.sync_api import Page, expect


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.items = page.locator("[data-test='inventory-item']")
        self.cart_badge = page.locator("[data-test='shopping-cart-badge']")
        self.cart_link = page.locator("[data-test='shopping-cart-link']")
        self.sort = page.locator("[data-test='product-sort-container']")
        self.prices = page.locator("[data-test='inventory-item-price']")

    def expect_loaded(self) -> None:
        expect(self.page).to_have_url(re.compile(r"/inventory\.html$"))
        expect(self.items.first).to_be_visible()

    def add_to_cart(self, slug: str) -> None:
        self.page.locator(f"[data-test='add-to-cart-{slug}']").click()

    def sort_by(self, value: str) -> None:
        self.sort.select_option(value)

    def price_values(self) -> list[float]:
        return [float(t.replace("$", "")) for t in self.prices.all_inner_texts()]
