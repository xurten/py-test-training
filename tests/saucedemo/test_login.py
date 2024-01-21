import pytest
from pages.sauce.base_page import Pages
from pages.sauce.login_page import LoginPage
from test_data.user_informations import STANDARD_PASSWORD, STANDARD_USER, LOCKED_USER
from tests.saucedemo.conftest import get_first_page


@pytest.mark.asyncio
async def test_login_flow_with_standard_user(browser_page) -> None:
    """
        Scenario 1. Check login flow for standard user
    """
    page = await get_first_page(browser_page)
    login_page = LoginPage(page)
    login_page = await login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)
    login_page = await login_page.verify_url('https://www.saucedemo.com/inventory.html')
    login_page = login_page.navigate_to(Pages.InventoryPage)
    login_page = await login_page.logout_user()
    await login_page.verify_url('https://www.saucedemo.com/')


@pytest.mark.asyncio
async def test_incorrect_login(browser_page) -> None:
    """
        # Scenario 2. Check wrong login
    """
    page = await get_first_page(browser_page)
    login_page = LoginPage(page)
    login_page = await login_page.login_as_user('aaaa', 'bbb')
    await login_page.verify_error_message('Epic sadface: Username and password do not match any user in this service')


@pytest.mark.asyncio
async def test_locked_out_user_login(browser_page) -> None:
    """
        # Scenario 3. Check locked user
    """
    page = await get_first_page(browser_page)
    login_page = LoginPage(page)
    login_page = await login_page.login_as_user(LOCKED_USER, STANDARD_PASSWORD)
    await login_page.verify_error_message('Epic sadface: Sorry, this user has been locked out.')
