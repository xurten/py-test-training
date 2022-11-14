# Scenario 1 Check A to Z
import pytest
from playwright.async_api import Page

from pages.sauce.inventory import SauceInventoryPage, SortAction
from pages.sauce.login import SauceLoginPage
from tests.saucedemo.helper import is_list_low_to_high
from tests.saucedemo.user_informations import STANDARD_USER, STANDARD_PASSWORD


@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    page.context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield
    page.context.tracing.stop(path="trace.zip")
    page.close()


# Scenario 1 Check A to Z
@pytest.mark.skip("Not yet implemented")
def test_item_name_in_asc_order(page: Page, login_page: SauceLoginPage,
                                       inventory_page: SauceInventoryPage) -> None:
    login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)
    inventory_page.click_sort_items(SortAction.NAME_ASC.value)
    list_of_item_names = inventory_page.page.locator('.inventory_item_name').all_text_contents()
    print(list_of_item_names)
    # assert is_list_low_to_high(list_of_item_names)
    inventory_page.logout_user()

# Scenario 2 Check Z to A
@pytest.mark.skip("Not yet implemented")
def test_item_name_in_desc_order(page: Page, login_page: SauceLoginPage,
                         inventory_page: SauceInventoryPage) -> None:
    login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)
    inventory_page.click_sort_items(SortAction.NAME_DESC.value)
    list_of_item_names = inventory_page.page.locator('.inventory_item_name').all_text_contents()
    print(list_of_item_names)
    # assert not is_list_low_to_high(list_of_item_names)
    inventory_page.logout_user()

# Scenario 3 Price Low to High
def test_price_from_low_to_high_order(page: Page, login_page: SauceLoginPage,
                         inventory_page: SauceInventoryPage) -> None:
    login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)
    inventory_page.click_sort_items(SortAction.PRICE_ASC.value)
    list_of_item_prices = inventory_page.page.locator('.inventory_item_price').all_text_contents()
    print(list_of_item_prices)
    assert is_list_low_to_high(list_of_item_prices)
    inventory_page.logout_user()

# Scenario 4 Price High to Low
def test_price_from_high_to_low_order(page: Page, login_page: SauceLoginPage,
                         inventory_page: SauceInventoryPage) -> None:
    login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)
    inventory_page.click_sort_items(SortAction.PRICE_DESC.value)
    list_of_item_prices = inventory_page.page.locator('.inventory_item_price').all_text_contents()
    print(list_of_item_prices)
    assert not is_list_low_to_high(list_of_item_prices)
    inventory_page.logout_user()