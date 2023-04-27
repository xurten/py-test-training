from typing import Optional, Coroutine, Any
from playwright.async_api import Page

from pages.sauce.base_page import BasePage


class ItemPage(BasePage):

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def _get_text_content(self, selector: str) -> Optional[str]:
        element = self.page.locator(selector).first
        if element:
            return element.text_content()
        return None

    def _get_price(self) -> Coroutine[Any, Any, Optional[str]]:
        return self._get_text_content('.inventory_details_price')

    def _get_item_title(self) -> Coroutine[Any, Any, Optional[str]]:
        return self._get_text_content('.inventory_details_name')

    def _get_item_description(self) -> Coroutine[Any, Any, Optional[str]]:
        return self._get_text_content('.inventory_details_desc')

    def verify_item_fields(self, expected_price: str, expected_header: str,
                           expected_description: str):
        assert self._get_price() == expected_price
        assert self._get_item_title() == expected_header
        assert self._get_item_description() == expected_description
        return self

    def get_image_src(self) -> Coroutine[Any, Any, Optional[str]]:
        return self.page.locator('.inventory_details_img').get_attribute('src')

    def click_add_item(self) -> None:
        self.page.locator('.btn_inventory').click()
        return self
