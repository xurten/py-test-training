from enum import Enum

from playwright.sync_api import Page


class Pages(Enum):
    CARD_PAGE = 1
    CHECKOUT_PAGE = 2
    INVENTORY_PAGE = 3
    ITEM_PAGE = 4
    LOGIN_PAGE = 5


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate_to(self, my_page: Pages):
        if my_page.value == Pages.CARD_PAGE.value:
            from pages.sauce.card_page import CardPage
            return CardPage(self.page)
        elif my_page.value == Pages.CHECKOUT_PAGE.value:
            from pages.sauce.checkout_page import CheckoutPage
            return CheckoutPage(self.page)
        elif my_page.value == Pages.INVENTORY_PAGE.value:
            from pages.sauce.inventory_page import InventoryPage
            return InventoryPage(self.page)
        elif my_page.value == Pages.ITEM_PAGE.value:
            from pages.sauce.item_page import ItemPage
            return ItemPage(self.page)
        elif my_page.value == Pages.LOGIN_PAGE.value:
            from pages.sauce.login_page import LoginPage
            return LoginPage(self.page)
