import pytest
from playwright.async_api import Page

from pages.sauce.inventory import SauceInventoryPage
from pages.sauce.login import SauceLoginPage
from tests.saucedemo.user_informations import STANDARD_PASSWORD, STANDARD_USER


@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    page.context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield
    page.context.tracing.stop(path="trace.zip")
    page.close()


# Scenario 1 Check login flow for standard user
@pytest.mark.regression
def test_login_flow_with_standard_user(page: Page, login_page: SauceLoginPage,
                                       inventory_page: SauceInventoryPage) -> None:
    login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)
    assert page.url == 'https://www.saucedemo.com/inventory.html'
    inventory_page.logout_user()
    assert page.url == 'https://www.saucedemo.com/'


# Scenario 2 Check wrong login
@pytest.mark.regression
def test_wrong_login(login_page: SauceLoginPage):
    login_page.login_as_user('aaaa', 'bbb')
    assert login_page.get_error_message() == 'Epic sadface: Username and password do not match any user in this service'
