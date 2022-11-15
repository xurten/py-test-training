from playwright.sync_api import Page

from tests.saucedemo.helper import remove_html_tags_from_string


class SauceLoginPage:
    URL = 'https://saucedemo.com'

    def __init__(self, page: Page) -> None:
        self.page = page
        self.username = page.locator("[data-test=\"username\"]")
        self.password = page.locator("[data-test=\"password\"]")
        self.login_button = page.locator("[data-test=\"login-button\"]")
        self.page.goto(self.URL)

    def login_as_user(self, username, password):
        self.set_credentials(username, password)
        self.click_login()

    def set_credentials(self, username, password):
        self.username\
            .fill(username)
        self.password\
            .fill(password)

    def click_login(self) -> None:
        self.login_button\
            .click()

    def get_error_message(self):
        self.page.locator("[data-test=\"error\"]")\
            .text_content()
        return remove_html_tags_from_string(self.page
                                            .locator("[data-test=\"error\"]")
                                            .inner_html())
