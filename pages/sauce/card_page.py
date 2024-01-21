from typing import Optional
from playwright.async_api import Page
from library.helper import sum_list_of_strings
from pages.sauce.base_page import BasePage


class CardPage(BasePage):

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def menu_quantity(self) -> Optional[str]:
        return await self.page.locator('#shopping_cart_container > a > span')\
            .text_content()

    async def card_quantity(self) -> str:
        quantities = await self.page.query_selector_all('.cart_quantity')
        return sum_list_of_strings([q.text_content() for q in quantities])

    async def verify_card_quantity(self, expected_card_quantity):
        card_menu_quantity = await self.menu_quantity()
        card_quantity = await self.card_quantity()
        assert card_menu_quantity == expected_card_quantity,\
            f" Wrong menu card quantity : {card_menu_quantity} != {expected_card_quantity}"
        assert card_quantity == expected_card_quantity,\
            f" Wrong card quantity : {card_quantity} != {expected_card_quantity}"
        return self

    async def click_checkout(self) -> None:
        await self.page.locator('.checkout_button').click()
        return self

    async def click_continue_shopping(self) -> None:
        await self.page.locator('#continue-shopping').click()
        return self
