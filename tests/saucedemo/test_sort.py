import pytest

from pages.sauce.base_page import Pages
from pages.sauce.inventory_page import SortAction
from library.helper import is_list_low_to_high, is_list_in_a_to_z_order, is_list_in_z_to_a_order
from test_data.user_informations import STANDARD_USER, STANDARD_PASSWORD


@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(login_page) -> None:
    login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)
    yield
    inventory_page = login_page.navigate_to(Pages.INVENTORY_PAGE)
    inventory_page.logout_user()

# Scenario 1. Check item names from A to Z
def test_item_name_in_asc_order(inventory_page) -> None:
    inventory_page.click_sort_items(SortAction.NAME_ASC.value)
    assert is_list_in_a_to_z_order(inventory_page._get_list_of_item_names())


# Scenario 2. Check item names from Z to A
def test_item_name_in_desc_order(inventory_page) -> None:
    inventory_page.click_sort_items(SortAction.NAME_DESC.value)
    assert is_list_in_z_to_a_order(inventory_page._get_list_of_item_names())


# Scenario 3. Price Low to High
def test_price_from_low_to_high_order(inventory_page) -> None:
    inventory_page.click_sort_items(SortAction.PRICE_ASC.value)
    assert is_list_low_to_high(inventory_page.get_list_of_item_prices())


# Scenario 4. Price High to Low
def test_price_from_high_to_low_order(inventory_page) -> None:
    inventory_page.click_sort_items(SortAction.PRICE_DESC.value)
    assert not is_list_low_to_high(inventory_page.get_list_of_item_prices())