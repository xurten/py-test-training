import pytest

from pages.sauce.base_page import Pages
from test_data.user_informations import STANDARD_PASSWORD, STANDARD_USER, LOCKED_USER


# Scenario 1. Check login flow for standard user
def test_login_flow_with_standard_user(login_page) -> None:
    login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD) \
       .verify_url('https://www.saucedemo.com/inventory.html') \
       .navigate_to(Pages.INVENTORY_PAGE) \
       .logout_user() \
       .verify_url('https://www.saucedemo.com/')


# Scenario 2. Check wrong login
def test_wrong_login(login_page) -> None:
    login_page.login_as_user('aaaa', 'bbb') \
        .verify_error_message('Epic sadface: Username and password do not match any user in this service')


# Scenario 3. Check locked user
def test_locked_login(login_page) -> None:
    login_page.login_as_user(LOCKED_USER, STANDARD_PASSWORD) \
        .verify_error_message('Epic sadface: Sorry, this user has been locked out.')
