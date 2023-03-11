import pytest

from pages.sauce.card_page import CardPage
from pages.sauce.checkout_page import CheckoutPage
from pages.sauce.inventory_page import InventoryPage
from pages.sauce.item_page import ItemPage
from pages.sauce.login_page import LoginPage


@pytest.fixture
def login_page(page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def inventory_page(page) -> InventoryPage:
    return InventoryPage(page)


@pytest.fixture
def card_page(page) -> CardPage:
    return CardPage(page)


@pytest.fixture
def checkout_page(page) -> CheckoutPage:
    return CheckoutPage(page)


@pytest.fixture
def item_page(page) -> ItemPage:
    return ItemPage(page)
