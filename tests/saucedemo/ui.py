import pytest
from playwright.async_api import Page

from pages.sauce.card import SauceCard
from pages.sauce.checkout import SauceCheckout
from pages.sauce.inventory import SauceInventoryPage
from pages.sauce.item import ItemPage
from pages.sauce.login import SauceLoginPage
from tests.saucedemo.helper import download_picture_from_url, validate_picture, remove_file
from tests.saucedemo.user_informations import STANDARD_USER, STANDARD_PASSWORD

EXTERNAL_SERVICES = [
    ('Facebook', 'https://www.facebook.com/saucelabs'),
    ('LinkedIn', 'https://www.linkedin.com/company/sauce-labs/'),
    ('Twitter', 'https://twitter.com/saucelabs')
]


@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    page.context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield
    page.context.tracing.stop(path="trace.zip")
    page.close()


# Scenario 1 Check login flow for standard user
def test_login_flow_with_standard_user(page: Page, login_page: SauceLoginPage,
                                       inventory_page: SauceInventoryPage) -> None:
    login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)
    assert page.url == 'https://www.saucedemo.com/inventory.html'
    inventory_page.logout_user()
    assert page.url == 'https://www.saucedemo.com/'


# Scenario 2 Check footer
def test_footer_check(page: Page, login_page: SauceLoginPage, inventory_page: SauceInventoryPage) -> None:
    login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)
    assert inventory_page.get_footer_text() == "© 2022 Sauce Labs. All Rights Reserved. Terms of Service | Privacy Policy"
    inventory_page.logout_user()


# Scenario 3 Check redirection media
@pytest.mark.parametrize('external_service', EXTERNAL_SERVICES)
def test_redirection_media(external_service: str, page: Page, login_page: SauceLoginPage,
                           inventory_page: SauceInventoryPage) -> None:
    login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)
    inventory_page.click_external_service(external_service[0])
    assert page.context.pages[1].url == external_service[1]
    inventory_page.logout_user()


# Scenario 4 Check that adding one item is good
def test_adding_of_one_item(page: Page, login_page: SauceLoginPage, inventory_page: SauceInventoryPage,
                            card_page: SauceCard) -> None:
    login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)
    inventory_page.click_generic_item(0)
    inventory_page.click_card()
    assert card_page.get_card_quantity_in_menu() == '1'
    assert card_page.get_card_quantity() == '1'
    inventory_page.logout_user()


# Scenario 5 Add 3 items and remove one item
def test_three_items_and_remove_first_one(page: Page, login_page: SauceLoginPage, inventory_page: SauceInventoryPage,
                                          card_page: SauceCard) -> None:
    login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)
    inventory_page.click_generic_item(0)
    inventory_page.click_generic_item(1)
    inventory_page.click_generic_item(2)
    inventory_page.click_generic_remove_item(0)
    inventory_page.click_card()
    assert card_page.get_card_quantity_in_menu() == '2'
    assert card_page.get_card_quantity() == '2'
    inventory_page.logout_user()


# Scenario 6 Add one item and check out
def test_add_one_item_and_checkout(page: Page, login_page: SauceLoginPage, inventory_page: SauceInventoryPage,
                                   card_page: SauceCard, checkout_page: SauceCheckout) -> None:
    login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)
    inventory_page.click_generic_item(0)
    inventory_page.click_card()
    card_page.click_checkout()
    checkout_page.fill_checkout_information('Andrzej', 'Zaaaaa', '87-100')
    checkout_page.click_continue()
    checkout_page.click_finish_button()
    assert checkout_page.get_complete_status() == 'Your order has been dispatched, and will arrive just as fast as the pony can get there!'
    assert checkout_page.get_complete_header_status() == "THANK YOU FOR YOUR ORDER"
    inventory_page.logout_user()


# Scenario 7 Add four items and check out
def test_four_items_and_checkout(page: Page, login_page: SauceLoginPage, inventory_page: SauceInventoryPage,
                                 card_page: SauceCard, checkout_page: SauceCheckout) -> None:
    login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)
    inventory_page.click_generic_item(0)
    inventory_page.click_generic_item(1)
    inventory_page.click_generic_item(2)
    inventory_page.click_generic_item(3)
    inventory_page.click_card()
    assert card_page.get_card_quantity_in_menu() == '4'
    assert card_page.get_card_quantity() == '4'
    card_page.click_checkout()
    checkout_page.fill_checkout_information('Andrzej', 'Zaaaaa', '87-100')
    checkout_page.click_continue()
    checkout_page.click_finish_button()
    assert checkout_page.get_complete_status() == 'Your order has been dispatched, and will arrive just as fast as the pony can get there!'
    assert checkout_page.get_complete_header_status() == "THANK YOU FOR YOUR ORDER"
    inventory_page.logout_user()


# Scenario 8 Check one item display
def test_one_item_display(page: Page, login_page: SauceLoginPage, inventory_page: SauceInventoryPage, card_page: SauceCard, item_page: ItemPage):
    local_picture_path = 'download_picture.jpg'
    expected_price = '$29.99'
    expected_header = 'Sauce Labs Backpack'
    expected_description = 'carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection.'
    login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)
    inventory_page.click_generic_item_name(0)
    image_path = item_page.get_image_src()
    full_image_path = f"{SauceLoginPage.URL}{image_path}"
    download_picture_from_url(full_image_path, local_picture_path)
    validate_picture(local_picture_path)
    assert item_page.get_price() == expected_price
    assert item_page.get_item_title() == expected_header
    assert item_page.get_item_description() == expected_description
    item_page.click_add_item()
    inventory_page.click_card()
    assert card_page.get_card_quantity_in_menu() == '1'
    assert card_page.get_card_quantity() == '1'
    remove_file(local_picture_path)
    inventory_page.logout_user()


# Scenario 9 Check wrong login
def test_wrong_login(page: Page, login_page: SauceLoginPage):
    login_page.login_as_user('aaaa', 'bbb')
    assert login_page.get_error_message() == 'Epic sadface: Username and password do not match any user in this service'


# Scenario 10 Check deletion of multiply items
def test_deletion_of_multiply_items(page: Page, login_page: SauceLoginPage, inventory_page: SauceInventoryPage,
                                     card_page: SauceCard):
    login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)
    inventory_page.click_generic_item(0)
    inventory_page.click_generic_item(1)
    inventory_page.click_generic_item(2)
    inventory_page.click_generic_item(3)
    inventory_page.click_generic_item(4)
    inventory_page.click_generic_item(5)
    inventory_page.click_generic_remove_item(0)
    inventory_page.click_generic_remove_item(1)
    inventory_page.click_generic_remove_item(2)
    inventory_page.click_generic_remove_item(3)
    inventory_page.click_generic_remove_item(4)
    inventory_page.click_card()
    assert card_page.get_card_quantity_in_menu() == '1'
    assert card_page.get_card_quantity() == '1'
    inventory_page.logout_user()
