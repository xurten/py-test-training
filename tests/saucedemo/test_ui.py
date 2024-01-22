from datetime import datetime

import pytest
from library.helper import download_picture_from_url, validate_picture, remove_file
from pages.sauce.base_page import Pages
from pages.sauce.checkout_page import CheckoutPage
from pages.sauce.inventory_page import InventoryPage
from pages.sauce.login_page import LoginPage
from tests.saucedemo.conftest import get_first_page

EXTERNAL_SERVICES = [
    ('Facebook', 'https://www.facebook.com/saucelabs'),
    ('LinkedIn', 'https://www.linkedin.com/'),
    ('Twitter', 'https://twitter.com/saucelabs')
]


@pytest.mark.asyncio
async def test_footer(log_as_standard_user) -> None:
    """
        # Scenario 1. Check footer
    """
    actual_year = datetime.now().year
    page = await get_first_page(log_as_standard_user)
    inventory_page = InventoryPage(page)
    actual_footer = await inventory_page.get_footer_text()
    assert actual_footer == f"© {actual_year} Sauce Labs. All Rights Reserved. Terms of Service | Privacy " \
                                               "Policy"


@pytest.mark.asyncio
@pytest.mark.parametrize('external_service', EXTERNAL_SERVICES)
async def test_redirection_media(log_as_standard_user, external_service: str) -> None:
    """
        # Scenario 2. Check redirection media
    """
    page = await get_first_page(log_as_standard_user)
    inventory_page = InventoryPage(page)
    await inventory_page.click_external_service(external_service[0])
    # timeout needed because of opening a new tab
    await inventory_page.page.wait_for_timeout(2000)
    assert external_service[1] in page.context.pages[1].url


@pytest.mark.asyncio
async def test_add_one_item(log_as_standard_user) -> None:
    """
        # Scenario 3. Check that adding one item is good
    """
    page = await get_first_page(log_as_standard_user)
    inventory_page = InventoryPage(page)
    await inventory_page.click_generic_item(0)
    await inventory_page.click_card()
    card_page = inventory_page.navigate_to(Pages.CardPage)
    await card_page.verify_card_quantity('1')


@pytest.mark.asyncio
async def test_add_three_items_and_remove_first_one(log_as_standard_user) -> None:
    """
        # Scenario 4. Add 3 items and remove one item
    """
    page = await get_first_page(log_as_standard_user)
    inventory_page = InventoryPage(page)
    for index in range(3):
        await inventory_page.click_generic_item(index)
    await inventory_page.click_generic_remove_item(0)
    await inventory_page.click_card()
    card_pages = inventory_page.navigate_to(Pages.CardPage)
    await card_pages.verify_card_quantity('2')


@pytest.mark.asyncio
async def test_add_one_item_and_checkout(log_as_standard_user) -> None:
    """
        # Scenario 5. Add one item and check out
    """
    page = await get_first_page(log_as_standard_user)
    inventory_page = InventoryPage(page)
    await inventory_page.click_generic_item(0)
    await inventory_page.click_card()
    card_page = inventory_page.navigate_to(Pages.CardPage)
    await card_page.click_checkout()
    checkout_page = card_page.navigate_to(Pages.CheckoutPage)
    await checkout_page.fill_checkout_information('Andrzej', 'Zaaaaa', '87-100')
    await checkout_page.click_continue()
    await checkout_page.click_finish_button()
    await checkout_page.verify_complete_status(CheckoutPage.COMPLETE_STATUS)
    await checkout_page.verify_complete_status_header(CheckoutPage.COMPLETE_STATUS_HEADER)


@pytest.mark.asyncio
async def test_add_four_items_and_checkout(log_as_standard_user) -> None:
    """
        # Scenario 6. Add four items and check out
    """
    page = await get_first_page(log_as_standard_user)
    inventory_page = InventoryPage(page)
    for index in range(4):
        await inventory_page.click_generic_item(index)
    await inventory_page.click_card()
    card_pages = inventory_page.navigate_to(Pages.CardPage)
    await card_pages.verify_card_quantity('4')
    await card_pages.click_checkout()
    checkout_page = card_pages.navigate_to(Pages.CheckoutPage)
    await checkout_page.fill_checkout_information('Andrzej', 'Zaaaaa', '87-100')
    await checkout_page.click_continue()
    await checkout_page.click_finish_button()
    await checkout_page.verify_complete_status(CheckoutPage.COMPLETE_STATUS)
    await checkout_page.verify_complete_status_header(CheckoutPage.COMPLETE_STATUS_HEADER)


@pytest.mark.asyncio
async def test_one_item_display(log_as_standard_user) -> None:
    """
        # Scenario 7. Check one item display
    """
    download_picture_name = 'download_picture.jpg'
    expected_price = '$29.99'
    expected_header = 'Sauce Labs Backpack'
    expected_description = 'carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection.'
    page = await get_first_page(log_as_standard_user)
    inventory_page = InventoryPage(page)

    await inventory_page.click_generic_item_name(0)
    item_page = inventory_page.navigate_to(Pages.ItemPage)
    image_path = await item_page.get_image_src()
    full_image_path = f"{LoginPage.URL}{image_path}"
    download_picture_from_url(full_image_path, download_picture_name)
    validate_picture(download_picture_name)
    item_page.verify_item_fields(expected_price, expected_header, expected_description)
    await item_page.click_add_item()
    inventory_page = item_page.navigate_to(Pages.InventoryPage)
    await inventory_page.click_card()
    card_page = inventory_page.navigate_to(Pages.CardPage)
    await card_page.verify_card_quantity('1')
    remove_file(download_picture_name)


@pytest.mark.asyncio
async def test_deletion_of_multiply_items(log_as_standard_user) -> None:
    """
        # Scenario 8. Check deletion of multiply items
    """
    page = await get_first_page(log_as_standard_user)
    inventory_page = InventoryPage(page)

    for index in range(6):
        await inventory_page.click_generic_item(index)
    for remove_index in range(5):
        await inventory_page.click_generic_remove_item(remove_index)
    await inventory_page.click_card()
    card_page = inventory_page.navigate_to(Pages.CardPage)
    await card_page.verify_card_quantity('1')
