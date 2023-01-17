import pytest

from pages.sauce.login import SauceLoginPage
from library.helper import download_picture_from_url, validate_picture, remove_file
from tests.saucedemo.user_informations import STANDARD_USER, STANDARD_PASSWORD

EXTERNAL_SERVICES = [
    ('Facebook', 'https://www.facebook.com/saucelabs'),
    ('LinkedIn', 'https://www.linkedin.com/'),
    ('Twitter', 'https://twitter.com/saucelabs')
]


@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(login_page, inventory_page) -> None:
    login_page.login_as_user(STANDARD_USER, STANDARD_PASSWORD)
    yield
    inventory_page.logout_user()


# Scenario 1 Check footer
@pytest.mark.regression
def test_footer(login_page, inventory_page) -> None:
    assert inventory_page.get_footer_text() == "© 2022 Sauce Labs. All Rights Reserved. Terms of Service | Privacy " \
                                               "Policy "


# Scenario 2 Check redirection media
@pytest.mark.parametrize('external_service', EXTERNAL_SERVICES)
@pytest.mark.regression
def test_redirection_media(page, external_service: str, inventory_page) -> None:
    inventory_page.click_external_service(external_service[0])
    # timeout needed because of opening a new tab
    page.wait_for_timeout(1000)
    assert external_service[1] in page.context.pages[1].url


# Scenario 3 Check that adding one item is good
@pytest.mark.regression
def test_add_one_item(inventory_page, card_page) -> None:
    inventory_page.click_generic_item(0)
    inventory_page.click_card()
    assert card_page.get_card_quantity_in_menu() == '1'
    assert card_page.get_card_quantity() == '1'


# Scenario 4 Add 3 items and remove one item
@pytest.mark.regression
def test_add_three_items_and_remove_first_one(inventory_page, card_page) -> None:
    for index in range(3):
        inventory_page.click_generic_item(index)
    inventory_page.click_generic_remove_item(0)
    inventory_page.click_card()
    assert card_page.get_card_quantity_in_menu() == '2'
    assert card_page.get_card_quantity() == '2'


# Scenario 5 Add one item and check out
def test_add_one_item_and_checkout(inventory_page, card_page, checkout_page) -> None:
    inventory_page.click_generic_item(0)
    inventory_page.click_card()
    card_page.click_checkout()
    checkout_page.fill_checkout_information('Andrzej', 'Zaaaaa', '87-100')
    checkout_page.click_continue()
    checkout_page.click_finish_button()
    assert checkout_page.get_complete_status() == 'Your order has been dispatched, and will arrive just as fast as the pony can get there!'
    assert checkout_page.get_complete_header_status() == "THANK YOU FOR YOUR ORDER"


# Scenario 6 Add four items and check out
@pytest.mark.regression
def test_add_four_items_and_checkout(inventory_page, card_page, checkout_page) -> None:
    for index in range(4):
        inventory_page.click_generic_item(index)
    inventory_page.click_card()
    assert card_page.get_card_quantity_in_menu() == '4'
    assert card_page.get_card_quantity() == '4'
    card_page.click_checkout()
    checkout_page.fill_checkout_information('Andrzej', 'Zaaaaa', '87-100')
    checkout_page.click_continue()
    checkout_page.click_finish_button()
    assert checkout_page.get_complete_status() == 'Your order has been dispatched, and will arrive just as fast as the pony can get there!'
    assert checkout_page.get_complete_header_status() == "THANK YOU FOR YOUR ORDER"


# Scenario 7 Check one item display
@pytest.mark.regression
def test_one_item_display(inventory_page, card_page, item_page) -> None:
    local_picture_path = 'download_picture.jpg'
    expected_price = '$29.99'
    expected_header = 'Sauce Labs Backpack'
    expected_description = 'carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection.'
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


# Scenario 8 Check deletion of multiply items
@pytest.mark.regression
def test_deletion_of_multiply_items(inventory_page, card_page) -> None:
    for index in range(6):
        inventory_page.click_generic_item(index)
    for remove_index in range(5):
        inventory_page.click_generic_remove_item(remove_index)
    inventory_page.click_card()
    assert card_page.get_card_quantity_in_menu() == '1'
    assert card_page.get_card_quantity() == '1'