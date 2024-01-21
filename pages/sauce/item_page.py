from typing import Optional, Coroutine, Any
from playwright.async_api import Page
from pages.sauce.base_page import BasePage


class ItemPage(BasePage):
    PRICE_SELECTOR = '.inventory_details_price'
    ITEM_TITLE_SELECTOR = '.inventory_details_name'
    ITEM_DESCRIPTION_SELECTOR = '.inventory_details_desc'

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def _get_text_content(self, selector: str) -> Optional[str]:
        element = await self.page.locator(selector).first
        if element:
            return await element.text_content()
        return None

    async def _get_price(self) -> Coroutine[Any, Any, Optional[str]]:
        return await self._get_text_content(self.PRICE_SELECTOR)

    async def _get_item_title(self) -> Coroutine[Any, Any, Optional[str]]:
        return await self._get_text_content(self.ITEM_TITLE_SELECTOR)

    def _get_item_description(self) -> Coroutine[Any, Any, Optional[str]]:
        return self._get_text_content(self.ITEM_DESCRIPTION_SELECTOR)

    async def verify_item_fields(self, expected_price: str, expected_header: str,
                                 expected_description: str):
        actual_price = await self._get_price()
        actual_title = await self._get_item_title()
        actual_item_description = await self._get_item_description()
        assert actual_price == expected_price
        assert actual_title == expected_header
        assert actual_item_description == expected_description

    async def get_image_src(self) -> Coroutine[Any, Any, Optional[str]]:
        return await self.page.locator('.inventory_details_img').get_attribute('src')

    async def click_add_item(self) -> None:
        await self.page.locator('.btn_inventory').click()
        return self
