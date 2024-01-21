from enum import Enum, unique
from typing import Optional

import playwright as playwright
from playwright.async_api import Page

from pages.sauce.base_page import BasePage
from pages.sauce.login_page import LoginPage


@unique
class SortAction(Enum):
    """
    Enum representing different sorting actions.
    """
    NAME_ASC = "az"
    """
    Sort items by name in ascending order.
    """
    NAME_DESC = "za"
    """
    Sort items by name in descending order.
    """
    PRICE_ASC = "lohi"
    """
    Sort items by price in ascending order.
    """
    PRICE_DESC = "hilo"
    """
    Sort items by price in descending order.
    """


class InventoryPage(BasePage):
    ITEM_COUNT = 6

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.navigation_menu = page.get_by_role("button", name="Open Menu")
        self.logout_option = page.get_by_role("link", name="Logout")
        self.inventory_list = page.locator(".inventory_list")
        self.footer = page.locator('//*[@id="page_wrapper"]/footer/div')

    async def logout_user(self) -> None:
        await self.open_navigation_menu()
        await self.click_logout()
        return LoginPage(self.page)

    async def open_navigation_menu(self) -> None:
        await self.navigation_menu.click()
        return self

    async def click_logout(self) -> None:
        await self.logout_option.click()

    async def get_footer_text(self) -> Optional[str]:
        return await self.footer.text_content()

    async def click_external_service(self, service_name: str) -> None:
        await self.page \
            .get_by_role("link", name=f"{service_name}") \
            .click()

    def get_inventory_list(self) -> playwright.sync_api._generated.Locator:
        return self.page\
            .locator(".inventory_list")

    async def click_generic_item(self, index: int) -> None:
        if not 0 <= index < self.ITEM_COUNT:
            raise Exception("Not valid index")
        await self.get_inventory_list() \
            .locator('.btn_inventory') \
            .nth(index) \
            .click()

    async def click_generic_item_name(self, index: int) -> None:
        if not 0 <= index < self.ITEM_COUNT:
            raise Exception("Not valid index")
        await self.get_inventory_list() \
            .locator('.inventory_item_name') \
            .nth(index) \
            .click()

    async def click_generic_remove_item(self, index: int) -> None:
        await self.get_inventory_list() \
            .locator('.btn_inventory') \
            .nth(index) \
            .click()

    async def click_card(self) -> None:
        await self.page.locator("#shopping_cart_container a").click()

    async def click_sort_items(self, sort_actions: str) -> None:
        await self.page \
            .locator("[data-test=\"product_sort_container\"]") \
            .select_option(sort_actions)
        return self

    async def _get_list_of_item_names(self) -> list[str]:
        item_names = await self.page \
            .locator('.inventory_item_name') \
            .all_text_contents()
        return item_names

    async def verify_items_names(self):
        item_names = await self._get_list_of_item_names()
        assert len(item_names) > 0
        return self

    async def get_list_of_item_prices(self) -> list[str]:
        return await self.page \
            .locator('.inventory_item_price') \
            .all_text_contents()

    async def click_about(self) -> 'LoginPage':
        await self.page \
            .locator('#about_sidebar_link') \
            .click()
        return LoginPage(self.page)

    async def click_all_items(self) -> None:
        await self.page \
            .locator('#inventory_sidebar_link') \
            .click()
        return InventoryPage(self.page)

    async def click_reset_app_state(self) -> None:
        await self.page \
            .locator('#reset_sidebar_link') \
            .click()
        return self

    async def is_shopping_cart_empty(self) -> bool:
        shopping_card = await self.page \
            .locator('.shopping_cart_link') \
            .inner_html()
        return shopping_card == ''

    async def get_shopping_cart_badge_value(self) -> str:
        card_value = await self.page \
            .locator('.shopping_cart_badge') \
            .inner_html()
        return card_value

    async def verify_badge_count(self, expected_count):
        actual_badge_count = await self._get_badge_value()
        assert actual_badge_count == expected_count
        return self

    async def _get_badge_value(self) -> str:
        is_card_empty = await self.is_shopping_cart_empty()
        if is_card_empty:
            shopping_card_value = '0'
        else:
            shopping_card_value = await self.get_shopping_cart_badge_value()
        return shopping_card_value

    async def click_menu(self) -> None:
        await self.page \
            .locator('#react-burger-menu-btn') \
            .click()
        return self
