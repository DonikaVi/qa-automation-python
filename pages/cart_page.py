from playwright.sync_api import Page


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.items = page.locator("[data-test='inventory-item']")
        self.checkout_btn = page.locator("[data-test='checkout']")
        self.first_name = page.locator("[data-test='firstName']")
        self.last_name = page.locator("[data-test='lastName']")
        self.postal = page.locator("[data-test='postalCode']")
        self.continue_btn = page.locator("[data-test='continue']")
        self.finish_btn = page.locator("[data-test='finish']")
        self.complete = page.locator("[data-test='complete-header']")

    def checkout(self, first: str, last: str, zip_code: str) -> None:
        self.checkout_btn.click()
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal.fill(zip_code)
        self.continue_btn.click()
        self.finish_btn.click()
