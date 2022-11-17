from playwright.sync_api import Page

from tests.saucedemo.helper import sum_list_of_strings


class SauceCard:
    URL = 'https://saucedemo.com'

    def __init__(self, page: Page) -> None:
        self.page = page
        self.continue_shopping = page.locator("[data-test=\"continue-shopping\"]")

    def click_continue_shopping(self):
        self.continue_shopping.click()

    def get_card_quantity_in_menu(self):
        return self.page \
            .locator('//*[@id="shopping_cart_container"]/a/span') \
            .text_content()

    def get_card_quantity(self):
        card_quantity = self.page \
            .locator('.cart_quantity') \
            .all_text_contents()
        return sum_list_of_strings(card_quantity)

    def click_checkout(self):
        self.page \
            .locator('.checkout_button') \
            .click()

    def click_continue_shopping(self):
        self.page\
            .locator('#continue-shopping')\
            .click()