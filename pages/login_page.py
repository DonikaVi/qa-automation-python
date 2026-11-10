from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.username = page.locator("[data-test='username']")
        self.password = page.locator("[data-test='password']")
        self.submit = page.locator("[data-test='login-button']")
        self.error = page.locator("[data-test='error']")

    def open(self) -> "LoginPage":
        self.page.goto(self.base_url)
        return self

    def login(self, user: str, pwd: str) -> None:
        self.username.fill(user)
        self.password.fill(pwd)
        self.submit.click()

    def expect_error(self, text: str) -> None:
        expect(self.error).to_contain_text(text)
