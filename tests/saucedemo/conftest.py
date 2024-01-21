import pytest
from playwright.async_api import async_playwright

from pages.sauce.card_page import CardPage
from pages.sauce.checkout_page import CheckoutPage
from pages.sauce.inventory_page import InventoryPage
from pages.sauce.item_page import ItemPage
from pages.sauce.login_page import LoginPage
from test_data.user_informations import STANDARD_USER, STANDARD_PASSWORD


@pytest.fixture
async def browser_page():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()
        yield page
        await browser.close()


async def get_first_page(browser_page):
    async for page in browser_page:
        return page


@pytest.fixture
async def log_as_standard_user(browser_page) -> None:
    page = await get_first_page(browser_page)
    login_page = LoginPage(page)
    await login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)
    yield page
