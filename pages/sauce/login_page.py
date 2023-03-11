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

    def login_as_user(self, username: str, password: str) -> None:
        self.page.goto(self.URL)
        self.set_credentials(username, password)
        self.click_login()
        return LoginPage(self.page)

    def _get_error_message(self) -> str:
        self.page.locator("[data-test=\"error\"]")\
            .text_content()
        return remove_html_tags_from_string(self.page
                                            .locator("[data-test=\"error\"]")
                                            .inner_html())

    def verify_url(self, expected_url):
        assert self.page.url == expected_url
        return LoginPage(self.page)

    def verify_error_message(self, expected_error_message):
        assert self._get_error_message() == expected_error_message

    def set_credentials(self, username: str, password: str) -> None:
        self.username.fill(username)
        self.password.fill(password)
        return LoginPage(self.page)

    def click_login(self) -> None:
        self.login_button.click()
        return LoginPage(self.page)


