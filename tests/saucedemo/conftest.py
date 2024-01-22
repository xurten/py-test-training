import pytest
from playwright.async_api import async_playwright

from pages.sauce.login_page import LoginPage
from pages.sauce.pages import Pages
from test_data.user_informations import STANDARD_USER, STANDARD_PASSWORD


@pytest.fixture
async def browser_page():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()
        yield page
        await browser.close()


@pytest.fixture
async def browser_page_and_browser():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()
        yield page, browser
        await browser.close()


async def get_first_page(browser_page):
    async for page in browser_page:
        return page


async def get_first_page_and_browser(browser_page):
    async for page, browser in browser_page:
        return page, browser


@pytest.fixture(scope='function')
async def log_as_standard_user(browser_page) -> None:
    page = await get_first_page(browser_page)
    login_page = LoginPage(page)
    await login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)
    yield page
    inventory_page = login_page.navigate_to(Pages.InventoryPage)
    await inventory_page.logout_user()
