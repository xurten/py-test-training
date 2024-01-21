from playwright.async_api import Page

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

    async def login_as_user(self, username: str, password: str) -> bool:
        await self.page.goto(self.URL)
        self.page.expect_navigation()
        await self.enter_credentials(username, password)
        await self.click_login()
        self._is_login_successful()
        return self

    def _is_login_successful(self) -> bool:
        return self.page.url != self.URL

    async def verify_url(self, expected_url) -> 'LoginPage':
        assert self.page.url == expected_url
        return self

    async def _get_error_message(self) -> str:
        inner_html = await self.error_message.inner_html()
        return remove_html_tags_from_string(inner_html)

    async def verify_error_message(self, expected_error_message) -> None:
        actual_error_message = await self._get_error_message()
        assert actual_error_message == expected_error_message

    async def enter_credentials(self, username: str, password: str) -> 'LoginPage':
        await self.username.fill(username)
        await self.password.fill(password)
        return self

    async def click_login(self) -> 'LoginPage':
        await self.login_button.click()
        return self

