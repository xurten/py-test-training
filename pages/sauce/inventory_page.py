import xml
from enum import Enum
from typing import Optional

import playwright as playwright
from playwright.sync_api import Page

from pages.sauce.base_page import BasePage
from pages.sauce.login_page import LoginPage


class SortAction(Enum):
    NAME_ASC = "az"
    NAME_DESC = "za"
    PRICE_ASC = "lohi"
    PRICE_DESC = "hilo"


class InventoryPage(BasePage):

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.navigation_menu = page.get_by_role("button", name="Open Menu")
        self.logout_option = page.get_by_role("link", name="Logout")
        self.inventory_list = page.locator(".inventory_list")
        self.footer = page.locator('//*[@id="page_wrapper"]/footer/div')

    def logout_user(self) -> None:
        self.open_navigation_menu()
        self.click_logout()
        return LoginPage(self.page)

    def open_navigation_menu(self) -> None:
        self.navigation_menu.click()
        return InventoryPage(self.page)

    def click_logout(self) -> None:
        self.logout_option.click()

    def get_footer_text(self) -> Optional[str]:
        return self.footer\
            .text_content()

    def click_external_service(self, service_name: str) -> None:
        self.page \
            .get_by_role("link", name=f"{service_name}") \
            .click()

    def get_inventory_list(self) -> playwright.sync_api._generated.Locator:
        return self.page\
            .locator(".inventory_list")

    def click_generic_item(self, index: int) -> None:
        if index < 0 or index > 5:
            raise Exception("Not valid index")
        self.get_inventory_list() \
            .locator('.btn_inventory') \
            .nth(index) \
            .click()
        return InventoryPage(self.page)

    def click_generic_item_name(self, index: int) -> None:
        if index < 0 or index > 5:
            raise Exception("Not valid index")
        self.get_inventory_list() \
            .locator('.inventory_item_name') \
            .nth(index) \
            .click()
        return InventoryPage(self.page)

    def click_generic_remove_item(self, index: int) -> None:
        self.get_inventory_list() \
            .locator('.btn_inventory') \
            .nth(index) \
            .click()
        return InventoryPage(self.page)

    def click_card(self) -> None:
        self.page \
            .locator("#shopping_cart_container a") \
            .click()
        return InventoryPage(self.page)

    def click_sort_items(self, sort_actions: str) -> None:
        self.page \
            .locator("[data-test=\"product_sort_container\"]") \
            .select_option(sort_actions)

    def verify_items_names(self):
        assert len(self._get_list_of_item_names()) > 0

    def _get_list_of_item_names(self) -> list[str]:
        return self.page \
            .locator('.inventory_item_name') \
            .all_text_contents()

    def get_list_of_item_prices(self) -> list[str]:
        return self.page \
            .locator('.inventory_item_price') \
            .all_text_contents()

    def click_about(self) -> None:
        self.page \
            .locator('#about_sidebar_link') \
            .click()
        return LoginPage(self.page)

    def click_all_items(self) -> None:
        self.page \
            .locator('#inventory_sidebar_link') \
            .click()

    def click_reset_app_state(self) -> None:
        self.page \
            .locator('#reset_sidebar_link') \
            .click()
        return InventoryPage(self.page)

    def is_shopping_cart_empty(self) -> bool:
        return self.page \
            .locator('.shopping_cart_link') \
            .inner_html()  == ''

    def get_shopping_cart_badge_value(self) -> str:
        return self.page \
            .locator('.shopping_cart_badge') \
            .inner_html()

    def verify_badge_count(self, expected_count):
        assert self._get_badge_value() == expected_count
        return InventoryPage(self.page)

    def _get_badge_value(self) -> str:
        if self.is_shopping_cart_empty():
            shopping_card_value = '0'
        else:
            shopping_card_value = self.get_shopping_cart_badge_value()
        return shopping_card_value

    def click_menu(self) -> None:
        self.page \
            .locator('#react-burger-menu-btn') \
            .click()
        return InventoryPage(self.page)
