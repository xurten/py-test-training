from typing import Optional
from playwright.sync_api import Page
from library.helper import sum_list_of_strings
from pages.sauce.base_page import BasePage


class CardPage(BasePage):

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def menu_quantity(self) -> Optional[str]:
        return self.page.locator('//*[@id="shopping_cart_container"]/a/span').text_content()

    def card_quantity(self) -> str:
        quantities = self.page.query_selector_all('.cart_quantity')
        return sum_list_of_strings([q.text_content() for q in quantities])

    def verify_card_quantity(self, expected_card_quantity):
        card_menu_quantity = self.menu_quantity()
        card_quantity = self.card_quantity()
        assert card_menu_quantity == expected_card_quantity, f" Wrong menu card quantity : {card_menu_quantity} != {expected_card_quantity}"
        assert card_quantity == expected_card_quantity, f" Wrong card quantity : {card_quantity} != {expected_card_quantity}"
        return self

    def click_checkout(self) -> None:
        self.page.locator('.checkout_button').click()
        return self

    def click_continue_shopping(self) -> None:
        self.page.locator('#continue-shopping').click()
        return self
