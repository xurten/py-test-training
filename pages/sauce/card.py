from typing import Optional, List
from playwright.sync_api import Page
from library.helper import sum_list_of_strings


class SauceCard:
    URL = 'https://saucedemo.com'

    def __init__(self, page: Page) -> None:
        self.page = page

    def get_card_quantity_in_menu(self) -> Optional[str]:
        return self.page \
            .locator('//*[@id="shopping_cart_container"]/a/span') \
            .text_content()

    def get_card_quantity(self) -> str:
        card_quantity = self.page \
            .locator('.cart_quantity') \
            .all_text_contents()
        return sum_list_of_strings(card_quantity)

    def click_checkout(self) -> None:
        self.page \
            .locator('.checkout_button') \
            .click()

    def click_continue_shopping(self) -> None:
        self.page \
            .locator('#continue-shopping') \
            .click()
