import re
from playwright.sync_api import Page, expect, sync_playwright
import pytest
from pages.result import DuckDuckGoResultPage
from pages.search import DuckDuckGoSearchPage

ANIMALS = [
    'panda',
    'python',
    'polar bear',
    'parrot',
    'porcupine',
    'parakeet',
    'pangolin',
    'panther',
    'platypus',
    'peacock'
]

@pytest.mark.parametrize('phrase', ANIMALS)
def test_homepage(phrase: str, page: Page, search_page: DuckDuckGoSearchPage, result_page: DuckDuckGoResultPage) -> None:
    search_page = DuckDuckGoSearchPage(page)
    result_page = DuckDuckGoResultPage(page)
    # Given the DuckDuckGo home page is displayed
    search_page.load()
    # When the user searches for a phrase
    search_page.search(phrase)
    # Then the search result query is the phrase
    expect(result_page.search_input).to_have_value(phrase)
    # And the search result links pertain to the phrase
    assert result_page.result_link_titles_contain_phrase(phrase)
    # And the search result title contains the phrase
    expect(page).to_have_title(f'{phrase} at DuckDuckGo')
