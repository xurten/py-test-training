import pytest

from pages.sauce.inventory_page import SortAction, InventoryPage
from library.helper import is_list_low_to_high, is_list_in_a_to_z_order, is_list_in_z_to_a_order
from tests.saucedemo.conftest import get_first_page


@pytest.mark.asyncio
async def test_item_name_in_asc_order(log_as_standard_user) -> None:
    """
        # Scenario 1. Check item names from A to Z
    """
    page = await get_first_page(log_as_standard_user)
    inventory_page = InventoryPage(page)
    await inventory_page.click_sort_items(SortAction.NAME_ASC.value)
    assert is_list_in_a_to_z_order(await inventory_page._get_list_of_item_names())


@pytest.mark.asyncio
async def test_item_name_in_desc_order(log_as_standard_user) -> None:
    """
        # Scenario 2. Check item names from Z to A
    """
    page = await get_first_page(log_as_standard_user)
    inventory_page = InventoryPage(page)
    await inventory_page.click_sort_items(SortAction.NAME_DESC.value)
    assert is_list_in_z_to_a_order(await inventory_page._get_list_of_item_names())


@pytest.mark.asyncio
async def test_price_from_low_to_high_order(log_as_standard_user) -> None:
    """
        # Scenario 3. Price Low to High
    """
    page = await get_first_page(log_as_standard_user)
    inventory_page = InventoryPage(page)
    await inventory_page.click_sort_items(SortAction.PRICE_ASC.value)
    assert is_list_low_to_high(await inventory_page.get_list_of_item_prices())


@pytest.mark.asyncio
async def test_price_from_high_to_low_order(log_as_standard_user) -> None:
    """
        # Scenario 4. Price High to Low
    """
    page = await get_first_page(log_as_standard_user)
    inventory_page = InventoryPage(page)
    await inventory_page.click_sort_items(SortAction.PRICE_DESC.value)
    assert not is_list_low_to_high(await inventory_page.get_list_of_item_prices())
