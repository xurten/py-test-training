from typing import Optional

from playwright.sync_api import Page


class SauceCheckout:

    def __init__(self, page: Page) -> None:
        self.page = page
        self.firstname = page.locator("[data-test=\"firstName\"]")
        self.lastname = page.locator("[data-test=\"lastName\"]")
        self.postal_code = page.locator("[data-test=\"postalCode\"]")
        self.continue_button = page.locator("[data-test=\"continue\"]")
        self.finish_button = page.locator("[data-test=\"finish\"]")

    def fill_checkout_information(self, firstname: str, lastname: str, postal_code: str) -> None:
        self.firstname.fill(firstname)
        self.lastname.fill(lastname)
        self.postal_code.fill(postal_code)

    def click_continue(self) -> None:
        self.continue_button\
            .click()

    def click_finish_button(self) -> None:
        self.finish_button\
            .click()

    def get_complete_status(self) -> Optional[str]:
        return self.page \
            .locator('.complete-text') \
            .text_content()

    def get_complete_header_status(self) -> Optional[str]:
        return self.page \
            .locator('.complete-header') \
            .text_content()
