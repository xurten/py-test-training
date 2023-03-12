import pytest

from pages.sauce.base_page import Pages
from pages.sauce.login_page import LoginPage
from test_data.user_informations import STANDARD_USER, STANDARD_PASSWORD


@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page) -> None:
    LoginPage(page).login_as_user(STANDARD_USER, STANDARD_PASSWORD)
    yield


# Scenario 1. Navigation reset app state
def test_reset_app_state(inventory_page):
    for index in range(3):
        inventory_page.click_generic_item(index)
    inventory_page.verify_badge_count('3') \
        .click_menu() \
        .click_reset_app_state() \
        .verify_badge_count('0')


# Scenario 2. Navigation check about
def test_navigation_to_about_page(inventory_page):
    inventory_page.click_menu() \
        .click_about() \
        .verify_url('https://saucelabs.com/')


# Scenario 3. Navigation check all items
def test_navigation_to_all_items_page(inventory_page):
    inventory_page.click_menu() \
        .click_all_items() \
        .verify_items_names()


# Scenario 4. Check continue shopping
def test_continue_shopping(inventory_page):
    inventory_page.click_generic_item(0) \
        .click_card() \
        .navigate_to(Pages.CardPage) \
        .verify_card_quantity('1') \
        .click_continue_shopping() \
        .navigate_to(Pages.InventoryPage) \
        .verify_badge_count('1')