from enum import Enum

from playwright.sync_api import Page


class SortAction(Enum):
    NAME_ASC = "az"
    NAME_DESC = "za"
    PRICE_ASC = "lohi"
    PRICE_DESC = "hilo"


class SauceInventoryPage:

    def __init__(self, page: Page) -> None:
        self.page = page
        self.navigation_menu = page.get_by_role("button", name="Open Menu")
        self.logout_option = page.get_by_role("link", name="Logout")
        self.inventory_list = page.locator(".inventory_list")
        self.footer = page.locator('//*[@id="page_wrapper"]/footer/div')

    def logout_user(self) -> None:
        self.open_navigation_menu()
        self.click_logout()

    def open_navigation_menu(self) -> None:
        self.navigation_menu.click()

    def click_logout(self) -> None:
        self.logout_option.click()

    def get_footer_text(self) -> str:
        return self.footer.text_content()

    def click_external_service(self, service_name) -> None:
        self.page.get_by_role("link", name=f"{service_name}").click()

    def get_inventory_list(self) -> list:
        return self.page\
            .locator(".inventory_list")

    def click_generic_item(self, index) -> None:
        if index < 0 or index > 5:
            raise Exception("Not valid index")
        self.get_inventory_list()\
            .locator('.btn_inventory')\
            .nth(index)\
            .click()

    def click_generic_item_name(self, index) -> None:
        if index < 0 or index > 5:
            raise Exception("Not valid index")
        self.get_inventory_list()\
            .locator('.inventory_item_name')\
            .nth(index)\
            .click()

    def click_generic_remove_item(self, index) -> None:
        self.get_inventory_list()\
            .locator('.btn_inventory')\
            .nth(index)\
            .click()

    def click_card(self) -> None:
        self.page\
            .locator("#shopping_cart_container a")\
            .click()

    def click_sort_items(self, sort_actions) -> None:
        self.page\
            .locator("[data-test=\"product_sort_container\"]")\
            .select_option(sort_actions)

    def get_list_of_item_names(self) -> list:
        return self.page\
            .locator('.inventory_item_name')\
            .all_text_contents()

    def get_list_of_item_prices(self) -> list:
        return self.page\
            .locator('.inventory_item_price')\
            .all_text_contents()