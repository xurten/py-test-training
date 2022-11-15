# Scenario 1 Check A to Z
import pytest
from playwright.async_api import Page

from pages.sauce.inventory import SauceInventoryPage, SortAction
from tests.saucedemo.helper import is_list_low_to_high, is_list_in_a_to_z_order, is_list_in_z_to_a_order
from tests.saucedemo.user_informations import STANDARD_USER, STANDARD_PASSWORD


@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page, inventory_page: SauceInventoryPage) -> None:
    page.context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield
    inventory_page.logout_user()
    page.context.tracing.stop(path="trace.zip")
    page.close()


# Scenario 1 Check item names from A to Z
@pytest.mark.regression
def test_item_name_in_asc_order(login_page, inventory_page) -> None:
    login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)
    inventory_page.click_sort_items(SortAction.NAME_ASC.value)
    assert is_list_in_a_to_z_order(inventory_page.get_list_of_item_names())


# Scenario 2 Check item names from Z to A
@pytest.mark.regression
def test_item_name_in_desc_order(login_page, inventory_page) -> None:
    login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)
    inventory_page.click_sort_items(SortAction.NAME_DESC.value)
    assert is_list_in_z_to_a_order(inventory_page.get_list_of_item_names())


# Scenario 3 Price Low to High
@pytest.mark.regression
def test_price_from_low_to_high_order(login_page, inventory_page) -> None:
    login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)
    inventory_page.click_sort_items(SortAction.PRICE_ASC.value)
    assert is_list_low_to_high(inventory_page.get_list_of_item_prices())


# Scenario 4 Price High to Low
@pytest.mark.regression
def test_price_from_high_to_low_order(login_page, inventory_page) -> None:
    login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)
    inventory_page.click_sort_items(SortAction.PRICE_DESC.value)
    assert not is_list_low_to_high(inventory_page.get_list_of_item_prices())
