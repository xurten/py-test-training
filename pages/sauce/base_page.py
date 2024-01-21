from importlib import import_module
from playwright.async_api import Page
from pages.sauce.pages import Pages


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate_to(self, my_page: Pages):
        module = import_module(f"pages.sauce.{my_page.value.lower()}")
        page_class = getattr(module, my_page.name)
        return page_class(self.page)
