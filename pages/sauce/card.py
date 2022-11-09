
from playwright.sync_api import Page


class SauceCard:
    URL = 'https://saucedemo.com'

    def __init__(self, page: Page) -> None:
        self.page = page
        self.continue_shopping = page.locator("[data-test=\"continue-shopping\"]")

    def click_continue_shopping(self):
        self.continue_shopping.click()

    def get_card_quantity_in_menu(self):
        return self.page.locator('//*[@id="shopping_cart_container"]/a/span').text_content()

    def get_card_quantity(self):
        return self.page.locator('//*[@id="cart_contents_container"]/div/div[1]/div[3]/div[1]').text_content()
