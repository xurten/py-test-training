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

    def fill_checkout_information(self, firstname: str, lastname: str,
                                  postal_code: str) -> None:
        if not firstname or not lastname or not postal_code:
            raise ValueError("All checkout information fields must be provided.")
        self.firstname.fill(firstname)
        self.lastname.fill(lastname)
        self.postal_code.fill(postal_code)
        return self

    def click_continue(self) -> None:
        try:
            self.continue_button.click()
        except Exception as e:
            raise Exception(f"Error occurred while clicking continue button: {e}")
        return self

    def click_finish_button(self) -> None:
        try:
            self.finish_button.click()
        except Exception as e:
            raise Exception(f"Error occurred while clicking finish button: {e}")
        return self

    def _get_complete_status(self) -> Optional[str]:
        return self.page \
            .locator('.complete-text') \
            .text_content()

    def _get_complete_header_status(self) -> Optional[str]:
        return self.page \
            .locator('.complete-header') \
            .text_content()

    def verify_complete_status(self, expect_complete_status):
        actual_status = self._get_complete_status()
        assert actual_status == expect_complete_status, f"Expected complete status: {expect_complete_status}, but got: {actual_status}"
        return self

    def verify_complete_status_header(self, expect_complete_status_header):
        actual_header = self._get_complete_header_status()
        assert actual_header == expect_complete_status_header, f"Expected complete status header: {expect_complete_status_header}, but got: {actual_header}"
        return self
