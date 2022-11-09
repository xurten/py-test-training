import shutil
import os
import sys
import warnings
from typing import Any, Callable, Dict, Generator, List, Optional

import pytest
from playwright.sync_api import (
    Browser,
    BrowserContext,
    BrowserType,
    Error,
    Page,
    Playwright,
    sync_playwright,
)
from slugify import slugify
import tempfile

from pages.result import DuckDuckGoResultPage
from pages.search import DuckDuckGoSearchPage


@pytest.fixture(scope='session')
def browser_context_args(browser_context_args, video_path):
    return {
        **browser_context_args,
        "record_video_dir": video_path,
        "viewport":
            {
                "width": 1920,
                "height": 1080
            }
    }


@pytest.fixture(scope='session')
def video_path():
    return "./videos"


def pytest_sessionstart(session):
    """
    Called before test run starts
    """
    print("pytest_sessionstart")
    if os.path.exists("./videos"):
        for filename in os.listdir("./videos"):
            filepath = os.path.join("./videos", filename)
            try:
                shutil.rmtree(filepath)
            except OSError:
                os.remove(filepath)


@pytest.fixture
def context(
        browser: Browser, browser_context_args: Dict, browser_name, video_path, request
) -> Generator[BrowserContext, None, None]:
    context = browser.new_context(**browser_context_args)
    current_failed_tests = request.session.testsfailed
    yield context
    current_video_name = context.current_video_name
    current_video_path = os.path.join(video_path, current_video_name)
    updated_video_path = os.path.join(video_path, f'{request.node.originalname}_{browser_name}.webm')
    context.close()
    os.rename(current_video_path, updated_video_path)
    if request.session.testsfailed == current_failed_tests:
        os.remove(updated_video_path)


@pytest.fixture
def result_page(page: Page) -> DuckDuckGoResultPage:
    return DuckDuckGoResultPage(page)


@pytest.fixture
def search_page(page: Page) -> DuckDuckGoSearchPage:
    return DuckDuckGoSearchPage(page)
