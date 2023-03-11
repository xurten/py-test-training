from typing import Optional

from playwright.sync_api import Page

from pages.sauce.base_page import BasePage


class CheckoutPage(BasePage):
    COMPLETE_STATUS = 'Your order has been dispatched, and will arrive just as fast as the pony can get there!'
    COMPLETE_STATUS_HEADER = 'Thank you for your order!'

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.firstname = page.locator("[data-test=\"firstName\"]")
        self.lastname = page.locator("[data-test=\"lastName\"]")
        self.postal_code = page.locator("[data-test=\"postalCode\"]")
        self.continue_button = page.locator("[data-test=\"continue\"]")
        self.finish_button = page.locator("[data-test=\"finish\"]")

    def fill_checkout_information(self, firstname: str, lastname: str, postal_code: str) -> None:
        self.firstname.fill(firstname)
        self.lastname.fill(lastname)
        self.postal_code.fill(postal_code)
        return CheckoutPage(self.page)

    def click_continue(self) -> None:
        self.continue_button\
            .click()
        return CheckoutPage(self.page)

    def click_finish_button(self) -> None:
        self.finish_button\
            .click()
        return CheckoutPage(self.page)

    def _get_complete_status(self) -> Optional[str]:
        return self.page \
            .locator('.complete-text') \
            .text_content()

    def _get_complete_header_status(self) -> Optional[str]:
        return self.page \
            .locator('.complete-header') \
            .text_content()

    def verify_complete_status(self, expect_complete_status):
        assert self._get_complete_status() == expect_complete_status
        return CheckoutPage(self.page)

    def verify_complete_status_header(self, expect_complete_status_header):
        assert self._get_complete_header_status() == expect_complete_status_header
        return CheckoutPage(self.page)
