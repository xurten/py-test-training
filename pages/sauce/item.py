from typing import Optional, Coroutine, Any
from playwright.async_api import Page


class ItemPage:

    def __init__(self, page: Page) -> None:
        self.page = page

    def get_price(self) -> Coroutine[Any, Any, Optional[str]]:
        return self.page \
            .locator('.inventory_details_price') \
            .first \
            .text_content()

    def get_item_title(self) -> Coroutine[Any, Any, Optional[str]]:
        return self.page \
            .locator('.inventory_details_name') \
            .first \
            .text_content()

    def get_item_description(self) -> Coroutine[Any, Any, Optional[str]]:
        return self.page \
            .locator('.inventory_details_desc') \
            .first \
            .text_content()

    def get_image_src(self) -> Coroutine[Any, Any, Optional[str]]:
        return self.page \
            .locator('.inventory_details_img') \
            .get_attribute('src')

    def click_add_item(self) -> None:
        self.page \
            .locator('.btn_inventory') \
            .click()
