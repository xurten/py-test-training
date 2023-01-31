import pytest
from test_data.user_informations import STANDARD_USER, STANDARD_PASSWORD


@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(login_page, inventory_page) -> None:
    login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)
    yield


# Scenario 1 Navigation reset app state
@pytest.mark.regression
def test_navigation_reset_app_state(login_page, inventory_page) -> None:
    for index in range(3):
        inventory_page.click_generic_item(index)
    assert inventory_page.get_badge_value() == '3'
    inventory_page.click_menu()
    inventory_page.click_reset_app_state()
    assert inventory_page.get_badge_value() == '0'


# Scenario 2 Navigation check about
@pytest.mark.regression
def test_navigation_check_about(login_page, inventory_page) -> None:
    inventory_page.click_menu()
    inventory_page.click_about()
    assert inventory_page.page.url == 'https://saucelabs.com/'


# Scenario 3 Navigation check all items
@pytest.mark.regression
def test_navigation_check_all_items(login_page, inventory_page) -> None:
    inventory_page.click_menu()
    inventory_page.click_all_items()
    assert len(inventory_page.get_list_of_item_names()) > 0


# Scenario 4 Check continue shopping
@pytest.mark.regression
def test_navigation_check_all_items(login_page, inventory_page, card_page) -> None:
    inventory_page.click_generic_item(0)
    inventory_page.click_card()
    assert card_page.get_card_quantity_in_menu() == '1'
    assert card_page.get_card_quantity() == '1'
    card_page.click_continue_shopping()
    assert inventory_page.get_badge_value() == '1'