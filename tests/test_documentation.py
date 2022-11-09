import re

import pytest
from playwright.sync_api import Page, expect
from pages.result import DuckDuckGoResultPage
from pages.search import DuckDuckGoSearchPage

ANIMALS = [
    'panda',
    'python'
]
# ANIMALS = [
#     'panda',
#     'python',
#     'polarbear',
#     'parrot',
#     'porcupine',
#     'parakeet',
#     'pangolin',
#     'panther',
#     'platypus',
#     'peacock'
# ]

@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    page.context.tracing.start(screenshots=True, snapshots=True, sources=True)
    print("beforeEach")

    yield
    print("afterEach")
    page.context.tracing.stop(path="trace.zip")
    page.close()


def test_homepage_has_playwright(page: Page):
    page.goto("https://playwright.dev/")
    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Playwright"))
    # create a locator
    get_started = page.get_by_role("link", name="Get started");
    # Expect an attribute "to be strictly equal" to the value.
    expect(get_started).to_have_attribute("href", "/docs/intro")
    # Click the get started link.
    get_started.click()
    # Expects the URL to contain intro.
    expect(page).to_have_url(re.compile(".*intro"))
    footer = page.locator(".footer__copyright")
    text = footer.all_inner_texts()
    assert text[0] == "Copyright © 2022 Microsoft"


@pytest.mark.parametrize('phrase', ANIMALS)
def test_homepage(phrase: str, page: Page, search_page: DuckDuckGoSearchPage,
                  result_page: DuckDuckGoResultPage) -> None:
    search_page = DuckDuckGoSearchPage(page)
    result_page = DuckDuckGoResultPage(page)
    # Given the DuckDuckGo home page is displayed
    search_page.load()
    # When the user searches for a phrase
    search_page.search(phrase)
    # Then the search result query is the phrase
    expect(result_page.search_input).to_have_value(phrase)
    # # And the search result links pertain to the phrase
    assert result_page.result_link_titles_contain_phrase(phrase)
    # # And the search result title contains the phrase
    expect(page).to_have_title(f'{phrase} at DuckDuckGo')
