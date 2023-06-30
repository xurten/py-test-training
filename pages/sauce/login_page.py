from playwright.sync_api import Page

from library.helper import remove_html_tags_from_string
from pages.sauce.base_page import BasePage


class LoginPage(BasePage):
    URL = 'https://saucedemo.com'

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username = page.locator("[data-test=\"username\"]")
        self.password = page.locator("[data-test=\"password\"]")
        self.login_button = page.locator("[data-test=\"login-button\"]")
        self.error_message = page.locator("[data-test=\"error\"]")

    def login_as_user(self, username: str, password: str) -> 'LoginPage':
        self.page.goto(self.URL)
        self.page.expect_navigation()
        self.set_credentials(username, password)
        self.click_login()
        return self

    def _get_error_message(self) -> str:
        self.error_message.text_content()
        return remove_html_tags_from_string(self.error_message.inner_html())

    def verify_url(self, expected_url) -> 'LoginPage':
        assert self.page.url == expected_url
        return self

    def verify_error_message(self, expected_error_message) -> None:
        assert self._get_error_message() == expected_error_message

    def set_credentials(self, username: str, password: str) -> 'LoginPage':
        self.username.fill(username)
        self.password.fill(password)
        return self

    def click_login(self) -> 'LoginPage':
        self.login_button.click()
        return self
