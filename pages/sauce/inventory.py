from playwright.sync_api import Page


class SauceInventoryPage:

    def __init__(self, page: Page) -> None:
        self.page = page
        self.navigation_menu = page.get_by_role("button", name="Open Menu")
        self.logout_option = page.get_by_role("link", name="Logout")
        self.inventory_list = page.locator(".inventory_list")
        self.footer = page.locator('//*[@id="page_wrapper"]/footer/div')

    def open_navigation_menu(self):
        self.navigation_menu.click()

    def click_logout(self) -> None:
        self.logout_option.click()

    def get_footer_text(self):
        return self.footer.text_content()

    def click_external_service(self, service_name):
        self.page.get_by_role("link", name=f"{service_name}").click()
