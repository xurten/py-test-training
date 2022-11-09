from concurrent.futures._base import LOGGER

from playwright.sync_api import Page


class DuckDuckGoSearchPage:
    URL = 'https://www.duckduckgo.com'

    def __init__(self, page: Page) -> None:
        self.page = page
        self.search_button = page.get_by_role("button", name="Search")
        self.search_input = page.locator('//*[@id="searchbox_input"]')
        print("Init")

    def load(self) -> None:
        self.page.goto(self.URL)
        print("Load")


    def search(self, phrase: str) -> None:
        self.search_input.fill(phrase)
        self.search_button.click()
        print("Search")