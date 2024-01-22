import pytest
from pages.sauce.base_page import Pages
from pages.sauce.inventory_page import InventoryPage
from tests.saucedemo.conftest import get_first_page


@pytest.mark.asyncio
async def test_reset_app_state(log_as_standard_user):
    """
        # Scenario 1. Navigation reset app state
    """
    page = await get_first_page(log_as_standard_user)
    inventory_page = InventoryPage(page)
    for index in range(3):
        await inventory_page.click_generic_item(index)
    inventory_page = await inventory_page.verify_badge_count('3')
    inventory_page = await inventory_page.click_menu()
    inventory_page = await inventory_page.click_reset_app_state()
    await inventory_page.verify_badge_count('0')


@pytest.mark.asyncio
async def test_navigation_to_about_page(log_as_standard_user):
    """
        # Scenario 2. Navigation check about
    """
    page = await get_first_page(log_as_standard_user)
    inventory_page = InventoryPage(page)
    inventory_page = await inventory_page.click_menu()
    login_page = await inventory_page.click_about()
    await login_page.verify_url('https://saucelabs.com/')


@pytest.mark.asyncio
async def test_navigation_to_all_items_page(log_as_standard_user):
    """
        # Scenario 3. Navigation check all items
    """
    page = await get_first_page(log_as_standard_user)
    inventory_page = InventoryPage(page)
    inventory_page = await inventory_page.click_menu()
    inventory_page = await inventory_page.click_all_items()
    inventory_page.verify_items_names()


@pytest.mark.asyncio
async def test_continue_shopping(log_as_standard_user):
    """
        # Scenario 4. Check continue shopping
    """
    page = await get_first_page(log_as_standard_user)
    inventory_page = InventoryPage(page)
    await inventory_page.click_generic_item(0)
    await inventory_page.click_card()
    inventory_page = inventory_page.navigate_to(Pages.CardPage)
    await inventory_page.verify_card_quantity('1')
    await inventory_page.click_continue_shopping()
    inventory_page = inventory_page.navigate_to(Pages.InventoryPage)
    await inventory_page.verify_badge_count('1')