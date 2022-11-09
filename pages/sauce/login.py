from playwright.sync_api import Page


class SauceLoginPage:
    URL = 'https://saucedemo.com'

    def __init__(self, page: Page) -> None:
        self.page = page
        self.username = page.locator("[data-test=\"username\"]")
        self.password = page.locator("[data-test=\"password\"]")
        self.login_button = page.locator("[data-test=\"login-button\"]")
        self.page.goto(self.URL)

    def set_credentials(self, username, password):
        self.username.fill(username)
        self.password.fill(password)

    def click_login(self) -> None:
        self.login_button.click()
