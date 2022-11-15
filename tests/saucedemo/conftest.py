import pytest
from playwright.async_api import Page

from pages.sauce.card import SauceCard
from pages.sauce.checkout import SauceCheckout
from pages.sauce.inventory import SauceInventoryPage
from pages.sauce.item import ItemPage
from pages.sauce.login import SauceLoginPage


@pytest.fixture
def login_page(page) -> SauceLoginPage:
    return SauceLoginPage(page)


@pytest.fixture
def inventory_page(page) -> SauceInventoryPage:
    return SauceInventoryPage(page)


@pytest.fixture
def card_page(page) -> SauceCard:
    return SauceCard(page)


@pytest.fixture
def checkout_page(page) -> SauceCheckout:
    return SauceCheckout(page)


@pytest.fixture
def item_page(page) -> ItemPage:
    return ItemPage(page)