from datetime import datetime

import pytest
from library.helper import download_picture_from_url, validate_picture, remove_file
from pages.sauce.base_page import Pages
from pages.sauce.checkout_page import CheckoutPage
from pages.sauce.login_page import LoginPage
from test_data.user_informations import STANDARD_USER, STANDARD_PASSWORD

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


# Scenario 1. Check footer
@pytest.mark.regression
def test_footer(inventory_page) -> None:
    actual_year = datetime.now().year
    assert inventory_page.get_footer_text() == f"© {actual_year} Sauce Labs. All Rights Reserved. Terms of Service | Privacy " \
                                               "Policy"


# Scenario 2. Check redirection media
@pytest.mark.parametrize('external_service', EXTERNAL_SERVICES)
@pytest.mark.regression
def test_redirection_media(inventory_page, external_service: str) -> None:
    inventory_page.click_external_service(external_service[0])
    # timeout needed because of opening a new tab
    inventory_page.page.wait_for_timeout(1000)
    assert external_service[1] in inventory_page.page.context.pages[1].url


# Scenario 3. Check that adding one item is good
@pytest.mark.regression
def test_add_one_item(inventory_page) -> None:
    inventory_page.click_generic_item(0) \
        .click_card() \
        .navigate_to(Pages.CARD_PAGE) \
        .verify_card_quantity('1')


# Scenario 4. Add 3 items and remove one item
@pytest.mark.regression
def test_add_three_items_and_remove_first_one(inventory_page) -> None:
    for index in range(3):
        inventory_page.click_generic_item(index)
    inventory_page.click_generic_remove_item(0) \
        .click_card() \
        .navigate_to(Pages.CARD_PAGE) \
        .verify_card_quantity('2')


# Scenario 5. Add one item and check out
def test_add_one_item_and_checkout(inventory_page) -> None:
    inventory_page.click_generic_item(0) \
        .click_card() \
        .navigate_to(Pages.CARD_PAGE) \
        .click_checkout() \
        .navigate_to(Pages.CHECKOUT_PAGE) \
        .fill_checkout_information('Andrzej', 'Zaaaaa', '87-100') \
        .click_continue() \
        .click_finish_button() \
        .verify_complete_status(CheckoutPage.COMPLETE_STATUS) \
        .verify_complete_status_header(CheckoutPage.COMPLETE_STATUS_HEADER)


# Scenario 6. Add four items and check out
@pytest.mark.regression
def test_add_four_items_and_checkout(inventory_page) -> None:
    for index in range(4):
        inventory_page.click_generic_item(index)
    inventory_page.click_card() \
        .navigate_to(Pages.CARD_PAGE) \
        .verify_card_quantity('4') \
        .click_checkout() \
        .navigate_to(Pages.CHECKOUT_PAGE) \
        .fill_checkout_information('Andrzej', 'Zaaaaa', '87-100') \
        .click_continue() \
        .click_finish_button() \
        .verify_complete_status(CheckoutPage.COMPLETE_STATUS) \
        .verify_complete_status_header(CheckoutPage.COMPLETE_STATUS_HEADER)


# Scenario 7. Check one item display
@pytest.mark.regression
def test_one_item_display(inventory_page) -> None:
    download_picture_name = 'download_picture.jpg'
    expected_price = '$29.99'
    expected_header = 'Sauce Labs Backpack'
    expected_description = 'carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection.'
    image_path = inventory_page.click_generic_item_name(0) \
        .navigate_to(Pages.ITEM_PAGE) \
        .get_image_src()
    full_image_path = f"{LoginPage.URL}{image_path}"
    download_picture_from_url(full_image_path, download_picture_name)
    validate_picture(download_picture_name)
    inventory_page.navigate_to(Pages.ITEM_PAGE) \
        .verify_item_fields(expected_price, expected_header, expected_description) \
        .click_add_item() \
        .navigate_to(Pages.INVENTORY_PAGE) \
        .click_card() \
        .navigate_to(Pages.CARD_PAGE) \
        .verify_card_quantity('1')
    remove_file(download_picture_name)


# Scenario 8. Check deletion of multiply items
@pytest.mark.regression
def test_deletion_of_multiply_items(inventory_page) -> None:
    for index in range(6):
        inventory_page.click_generic_item(index)
    for remove_index in range(5):
        inventory_page.click_generic_remove_item(remove_index)
    inventory_page.click_card() \
        .navigate_to(Pages.CARD_PAGE) \
        .verify_card_quantity('1')