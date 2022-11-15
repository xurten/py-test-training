import pytest

from tests.saucedemo.user_informations import STANDARD_USER, STANDARD_PASSWORD


# Scenario 1 Navigation reset app state
@pytest.mark.regression
def test_navigation_reset_app_state(login_page, inventory_page) -> None:
    login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)


# Scenario 2 Navigation check about
@pytest.mark.regression
def test_navigation_check_about(login_page, inventory_page) -> None:
    login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)


# Scenario 3 Navigation check all items
@pytest.mark.regression
def test_navigation_check_all_items(login_page, inventory_page) -> None:
    login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)
