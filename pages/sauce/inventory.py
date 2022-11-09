from playwright.sync_api import Page


class SauceInventoryPage:

    def __init__(self, page: Page) -> None:
        self.page = page
        self.navigation_menu = page.get_by_role("button", name="Open Menu")
        self.logout_option = page.get_by_role("link", name="Logout")
        self.inventory_list = page.locator(".inventory_list")
        self.footer = page.locator('//*[@id="page_wrapper"]/footer/div')

    def logout_user(self):
        self.open_navigation_menu()
        self.click_logout()

    def open_navigation_menu(self):
        self.navigation_menu.click()

    def click_logout(self) -> None:
        self.logout_option.click()

    def get_footer_text(self):
        return self.footer.text_content()

    def click_external_service(self, service_name):
        self.page.get_by_role("link", name=f"{service_name}").click()

    def get_inventory_list(self):
        return self.page.locator(".inventory_list")

    def click_generic_item(self, index):
        if index < 0 or index > 5:
            raise Exception("Not valid index")
        self.get_inventory_list().locator('.btn_inventory').nth(index).click()

    def click_generic_remove_item(self, index):
        self.get_inventory_list().locator('.btn_inventory').nth(index).click()

    def click_card(self):
        self.page.locator("#shopping_cart_container a").click()