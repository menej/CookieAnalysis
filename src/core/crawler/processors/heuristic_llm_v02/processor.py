import json
import logging
import os
import re
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Any
from urllib.parse import urljoin, urlparse

from openai import OpenAI
from playwright.sync_api import sync_playwright, Playwright, Browser, BrowserContext, Page, Frame
from playwright.sync_api import TimeoutError

from src.core.common import loader
from src.core.crawler.processors.heuristic_llm_v02.business import processor_helper
from src.core.crawler.processors.heuristic_llm_v02.entities.enums.BannerInteraction import BannerInteraction
from src.core.crawler.processors.heuristic_llm_v02.entities.enums.InteractionStatus import InteractionStatus
from src.core.crawler.processors.heuristic_llm_v02.entities.enums.StageOutcome import StageOutcome
from src.core.crawler.processors.heuristic_llm_v02.entities.models.InteractionResult import InteractionResult
from src.core.crawler.processors.heuristic_llm_v02.entities.models.MissingLLMResponseKeyError import MissingLLMResponseKeyError
from src.core.crawler.processors.heuristic_llm_v02.entities.models.StageMetadata import initialize_metadata_accept_stage, initialize_metadata_decline_stage
from src.entities.enums.BrowserProvider import BrowserProvider
from src.entities.enums.VisitStage import VisitStage
from src.entities.models.Stage import Stage
from src.entities.models.WebsiteCrawl import WebsiteCrawl

"""
Global Configuration and Variables

This processor initializes essential global variables for the crawling process.

Configuration Variables:
    global_config (dict): Loaded global configuration settings from src.
    local_config (dict): Loaded processors local configuration from the processors directory (from config.json).

Cookie Lexicon:
    cookie_lexicon (dict): A predefined lexicon for identifying and categorizing cookies.

Crawling State Variables:
    root_web_page (str | None): The root URL of the website being crawled, initialized as None.
    root_output_path (Path | None): The output directory where crawl results are stored, initialized as None.
    website_crawl (WebsiteCrawl | None): Represents the current website crawl session.

Playwright Browser Instances:
    playwright (Playwright | None): The Playwright instance managing browser automation.
    browser (Browser | None): The active browser instance.
    context (BrowserContext | None): The browser context managing isolated sessions.
    page (Page | None): The active Playwright page used for crawling.

Notes:
    - `global_config` and `local_config` store different levels of configuration.
    - `cookie_lexicon` is used to classify cookies during analysis.
    - The Playwright variables (`playwright`, `browser`, `context`, `page`) are initialized as `None` 
      and are assigned during the crawling session. They are aftwerards set as 'None'.
"""

# Load logger
logger = logging.getLogger(__name__)

# Load global configurations
global_config = loader.load_config()

# Load local configuration from 'config.json'
with open(os.path.dirname(os.path.abspath(__file__)) + "/config.json", 'r', encoding='utf-8') as file:
    local_config = json.load(file)

# Load cookie lexicon for classification
cookie_lexicon = loader.load_cookie_lexicon()

# Initialize global state variables
root_web_page: str | None = None
root_output_path: Path | None = None
website_crawl: WebsiteCrawl | None

# Initialize Playwright browser instances
playwright: Playwright | None = None
browser: Browser | None = None
context: BrowserContext | None = None
page: Page | None = None


def crawl(web_page: str, output_path: Path) -> WebsiteCrawl:
    """
    Perform a full website crawl, processing different cookie consent stages.

    This function follows a structured workflow to:
    1. Initialize the crawl with `_init()`, setting up the Playwright driver and other resources.
    2. Process the "normal stage" (`_process_normal_stage()`), which collects cookies before any interactions.
    3. Restart the browser and process the "accept stage" (`_process_accept_stage()`), simulating a full cookie acceptance.
    4. Restart the browser again and process the "decline stage" (`_process_decline_stage()`), simulating cookie rejection.
    5. Handle any exceptions that may occur during execution.
    6. Ensure proper cleanup of resources with `_cleanup()`.

    Args:
        web_page (str): The URL of the website to crawl.
        output_path (Path): The path where the crawl results will be saved.

    Returns:
        WebsiteCrawl: An object containing the collected crawl data.

    Raises:
        Exception: If any stage of the crawl process encounters an error.

    Global Variables:
        website_crawl: Stores crawl results and metadata.

    Notes:
        - The `restart_driver()` function ensures a fresh session between consent stages.
        - The `finally` block ensures `_cleanup()` is called, even if an error occurs.
    """
    global website_crawl

    try:
        _init(web_page, output_path)
        _init_driver()

        _process_normal_stage()

        _stop_driver()
        _init_driver()

        _process_accept_stage()

        _stop_driver()
        _init_driver()

        _process_decline_stage()
    except Exception as e:
        raise e
    finally:
        _cleanup()

    return website_crawl


def _init(web_page: str, output_path: Path) -> WebsiteCrawl:
    """
    Initializes a website crawl by setting global variables, creating a `WebsiteCrawl` instance,
    and starting the crawling process.

    :param web_page: The URL of the website to crawl.
    :param output_path: The directory to store crawl-related output.
    :return: The initialized `WebsiteCrawl` instance.
    """
    global root_web_page, website_crawl, root_output_path

    root_web_page = web_page
    root_output_path = output_path

    website_crawl = WebsiteCrawl(
        web_page=root_web_page,
        name_of_analysis=global_config["cookie_crawler_configuration"]["name_of_analysis"],
        crawl_mode=global_config["cookie_crawler_configuration"]["crawl_mode"],
        browser_provider=global_config["cookie_crawler_configuration"]["browser_provider"],
        take_screenshots=global_config["cookie_crawler_configuration"]["take_screenshots"],
    )

    website_crawl.start()

    return website_crawl


def _init_driver():
    """
    Initialize the Playwright browser driver and set up the browsing context.

    This function performs the following tasks:
    1. Checks if the browser provider is supported (only Chrome is allowed).
    2. Starts Playwright and launches a Chromium browser instance using the Chrome channel.
    3. Configures the browser with specific arguments to:
       - Disable automation detection by websites.
       - Allow third-party cookies by disabling SameSite-by-default policies.
    4. Sets up a new browser context with:
       - A fixed viewport size of 1920x1080.
       - A predefined user agent string mimicking a Chrome browser on Windows.
    5. Creates a new page instance for interactions.

    Raises:
        Exception: If the `browser_provider` is not set to "CHROME".

    Global Variables:
        playwright: Playwright instance for browser automation.
        browser: Playwright browser instance.
        context: Playwright browser context for isolated sessions.
        page: Playwright page instance for browsing.
        website_crawl: Global configuration object containing the crawl settings.
    """
    global playwright, browser, context, page, website_crawl

    if website_crawl.browser_provider != BrowserProvider.CHROME.name:
        raise Exception("Browser provider not supported for this crawl.")

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(
        channel="chrome",
        headless=local_config["headless_mode"],
        args=[
            "--disable-blink-features=AutomationControlled",  # Hide "automation"
            "--disable-features=SameSiteByDefaultCookies"  # Allow 3rd party cookies
        ]
    )

    screen_width = 1920
    screen_height = 1080

    context = browser.new_context(
        viewport={"width": screen_width, "height": screen_height},
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/110.0.0.0 Safari/537.36"
        )
    )

    page = context.new_page()


def _stop_driver():
    """
    Stop Playwright and clean up browser resources.

    Closes the Playwright page, browser context, and browser instance if they exist.
    Ensures that all references are cleared after stopping Playwright.
    """
    global playwright, browser, context, page

    if page:
        page.close()
    if context:
        context.close()
    if browser:
        browser.close()
    if playwright:
        playwright.stop()

    playwright = None
    browser = None
    context = None
    page = None


def _cleanup():
    """
    Clean up global variables and stop the Playwright driver.

    This function resets key global variables to `None` and ensures the browser
    session is properly terminated by calling `_stop_driver()`. It also stops
    the `website_crawl` process to finalize the crawling session.
    """
    global root_web_page, website_crawl, root_output_path

    root_web_page = None
    root_output_path = None
    _stop_driver()
    website_crawl.stop()

def _process_normal_stage() -> Stage:
    """
    Process the normal stage of the website crawl.

    This function performs the initial cookie collection before any user interactions.
    It follows these steps:

    1. Initializes a new `Stage` object and assigns it to `website_crawl.normal_stage`.
    2. Starts the stage timer.
    3. Visits the root web page and collects cookies before any interactions.
    4. Crawls internal pages to gather additional cookies.
    5. Collects cookies again after traversing the internal pages.
    6. Stops the stage timer and returns the completed `Stage` object.

    Returns:
        Stage: The completed normal stage containing collected cookies.

    Notes:
        - `VisitStage.NORMAL_INITIAL_VISIT` represents cookies collected before navigation.
        - `VisitStage.NORMAL_AFTER_TRAVERSIAL` represents cookies collected after limited internal navigation.
        - The `max_pages` parameter is set to 1 to minimize crawling depth during this stage.
    """
    global page

    stage = Stage()
    website_crawl.normal_stage = stage

    stage.start()

    _visit_page(root_web_page, stage)
    _collect_cookies(stage, VisitStage.NORMAL_INITIAL_VISIT)
    _crawl_internal_pages(stage)
    _collect_cookies(stage, VisitStage.NORMAL_AFTER_TRAVERSIAL)

    stage.stop()

    return stage

def _process_accept_stage() -> Stage:
    """
    Process the "Accept All Cookies" stage of the website crawl.

    This function simulates a user accepting all cookies and collects cookie data
    before the interaction, after the interaction and after traversial.
    It follows these steps:

    1. Initializes a new `Stage` object and assigns it to `website_crawl.accept_stage`.
    2. Starts the stage timer.
    3. Visits the root web page and collects cookies before interaction.
    4. Interacts with the cookie banner to accept all cookies.
    5. Collects cookies again after acceptance.
    6. Crawls internal pages to gather additional cookies.
    7. Collects cookies once more after navigating internal pages.
    8. Stops the stage timer and returns the completed `Stage` object.

    Returns:
        Stage: The completed accept stage containing collected cookies.

    Notes:
        - `VisitStage.ACCEPT_INITIAL_VISIT` represents cookies collected before clicking "Accept".
        - `VisitStage.ACCEPT_AFTER_ACTION` represents cookies collected immediately after clicking "Accept".
        - `VisitStage.ACCEPT_AFTER_TRAVERSIAL` represents cookies collected after internal navigation.
        - The `_interact_with_accept()` function simulates the user accepting cookies.
    """
    global page

    stage = Stage()
    website_crawl.accept_stage = stage

    stage.start()

    _visit_page(root_web_page, stage)
    _collect_cookies(stage, VisitStage.ACCEPT_INITIAL_VISIT)
    execute_accept_initializer(stage)
    _collect_cookies(stage, VisitStage.ACCEPT_AFTER_ACTION)
    _crawl_internal_pages(stage)
    _collect_cookies(stage, VisitStage.ACCEPT_AFTER_TRAVERSIAL)

    stage.stop()

    return stage

def _process_decline_stage() -> Stage:
    global page

    stage = Stage()
    website_crawl.decline_stage = stage

    stage.start()

    _visit_page(root_web_page, stage)
    _collect_cookies(stage, VisitStage.DECLINE_INITIAL_VISIT)
    execute_decline_initializer(stage)
    _collect_cookies(stage, VisitStage.DECLINE_AFTER_ACTION)
    _crawl_internal_pages(stage)
    _collect_cookies(stage, VisitStage.DECLINE_AFTER_TRAVERSIAL)

    stage.stop()

    return stage


def _visit_page(web_page: str, stage: Stage, timeout=5000):
    """
    Visit the given webpage and add it to the list of visited pages.

    Args:
        web_page (str): The URL to visit.
        stage (Stage): The stage object tracking visited pages.
        timeout (int, optional): Timeout in milliseconds before proceeding. Defaults to 5000.

    Raises:
        Exception: Propagates any exception that occurs while visiting the page.
    """
    logger.info(f"Visiting: {web_page}")
    try:
        page.goto(web_page, wait_until="domcontentloaded")
        page.wait_for_timeout(timeout)
        stage.pages_visited.append(web_page)
    except Exception as e:
        error_msg = f"Failed to visit page '{web_page}': {str(e)}"
        stage.exceptions.append(error_msg)
        logger.exception(error_msg)
        raise


def _collect_cookies(stage, visit_stage):
    """
    Collect cookies from the current browser context and store them in the given stage.

    This function retrieves all cookies from the Playwright browser context and
    processes them into a structured dictionary format. Each cookie is stored
    under the corresponding `visit_stage.name` in the `stage.stage_cookies` dictionary.

    Args:
        stage (Stage): The stage object where collected cookies will be stored.
        visit_stage (VisitStage): Enum representing the current stage of the crawl.

    Notes:
        - Cookies are retrieved via `context.cookies()`.
        - The `expires` field is converted into a human-readable ISO format (`expires_date`).
        - Session cookies (`expires = -1` or `None`) are labeled as `"Session"`.
        - The function appends a record to `stage.interactions` to log the action.

    Example of Stored Cookie Data:
    {
        "name": "_ga",
        "value": "GA1.2.123456789.123456789",
        "domain": "example.com",
        "path": "/",
        "expires": 1700000000,
        "expires_date": "2023-11-30T12:34:56+00:00",
        "httpOnly": false,
        "secure": true,
        "sameSite": "Lax"
    }

    """
    cookies = context.cookies()

    stage.stage_cookies[visit_stage.name] = list()
    for cookie in cookies:
        expires = cookie.get('expires')

        if expires is None or expires == -1:
            expires_date = "Session"
            expires = -1
        else:
            expires_date = datetime.fromtimestamp(expires, tz=timezone.utc).isoformat()

        cookie_dict = {
            "name": cookie['name'],
            "value": cookie['value'],
            "domain": cookie['domain'],
            "path": cookie['path'],
            "expires": expires,  # Raw expires timestamp or -1
            "expires_date": expires_date,  # Human-readable or "Session"
            "httpOnly": cookie.get('httpOnly', False),
            "secure": cookie.get('secure', False),
            "sameSite": cookie.get('sameSite', None),
        }
        stage.stage_cookies[visit_stage.name].append(cookie_dict)

    stage.interactions.append(f"Collected cookies for {visit_stage.name}")


def _crawl_internal_pages(stage: Stage, max_pages: int = local_config['num_crawls']):
    """
    Crawl internal pages within the same domain, following discovered links.

    This function:
    - Collects same-domain links from the base URL.
    - Iteratively visits new links up to `max_pages`.
    - Handles navigation errors gracefully by logging and skipping failed pages.
    - Ensures the crawler does not follow redirects to different domains.
    - Simulates user scrolling interaction after visiting each page.

    Args:
        stage (Stage): The stage object tracking the crawl process.
        max_pages (int, optional): The maximum number of internal pages to crawl. Defaults to `local_config['num_crawls']`.

    Raises:
        Exception Handling: If page navigation fails, the error is logged, and the crawl continues.
        Exception: Propagates exception to `_visit_page` upon attempt of returning to root domain.

    Notes:
        - Uses `_retrieve_same_domain_urls()` to get discoverable links.
        - Calls `_visit_page()` to navigate each discovered link.
        - Prevents cross-domain navigation by checking and returning to the root domain if redirected.
        - Calls `_simulate_scroll_interaction()` after visiting a page to mimic human-like browsing.
    """
    same_domain_links = _retrieve_same_domain_urls(stage, root_web_page, stage.pages_visited)

    count = 0
    while same_domain_links and count < max_pages:
        link = same_domain_links.pop()
        count += 1

        try:
            _visit_page(link, stage)
        except Exception as e:
            error_msg = f"Exception occurred while visiting page {link}: {str(e)}"
            logger.error(error_msg)
            stage.exceptions.append(error_msg)
            continue

        # Check if the domain matches the root domain
        current_url = page.url  # Get the current URL after navigation
        current_domain = urlparse(current_url).netloc
        root_domain = urlparse(root_web_page).netloc

        if _canonical_domain(current_domain) != _canonical_domain(root_domain):
            logger.info(f"Redirected to a different domain: {current_domain}. Returning to root domain: {root_domain}.")
            _visit_page(root_web_page, stage)

        same_domain_links.update(_retrieve_same_domain_urls(stage, link, stage.pages_visited))

        _simulate_scroll_interaction(stage)

def _retrieve_same_domain_urls(stage: Stage, current_url: str, visited_urls: list[str]) -> set[str]:
    """
    Retrieve all unique, same-domain URLs from <a> elements on the current page.

    This function extracts all anchor (`<a>`) links from the current page and filters them
    to include only URLs that:
    - Belong to the same domain as `current_url`.
    - Have not been visited yet.
    - Are not the same as the `current_url`.

    Args:
        current_url (str): The URL of the currently visited page.
        visited_urls (list[str]): A list of URLs that have already been visited.

    Returns:
        set[str]: A set of unique same-domain URLs found on the page.

    Notes:
        - URLs are normalized using `_canonical_domain()` to ensure consistent comparison.
        - Relative URLs are converted to absolute using `urljoin()`.
        - Any errors retrieving anchor attributes are logged and skipped.
    """
    anchors = page.query_selector_all("a[href]")
    base_parsed = urlparse(current_url)
    base_domain = _canonical_domain(base_parsed.netloc)

    found_links = set()

    for a in anchors:
        try:
            href = a.get_attribute("href")
        except Exception as e:
            error_msg = f"Skipping anchor due to error: {str(e)}"
            logger.error(error_msg)
            stage.exceptions.append(error_msg)
            continue

        if not href:
            continue

        full_url = urljoin(current_url, href)
        parsed = urlparse(full_url)
        link_domain = _canonical_domain(parsed.netloc)

        if (link_domain == base_domain and
            full_url != current_url and
            full_url not in visited_urls):
            found_links.add(full_url)

    return found_links


def _canonical_domain(netloc: str) -> str:
    """
     Normalize a domain name to its canonical form.

     This function:
     - Converts the domain name to lowercase.
     - Removes the leading "www." prefix for consistency.

     Args:
         netloc (str): The network location (domain) extracted from a URL.

     Returns:
         str: The normalized domain name.

     The crawler is treating www.example.com and example.com as the same domain by removing the leading "www." so that links such as http://www.example.com/foo and http://example.com/foo are recognized as internal links on the same site. Without this normalization, the crawler might treat example.com and www.example.com as different domains, causing it to skip or mishandle links that only differ by the "www." prefix.
     """
    domain = netloc.lower()
    domain = re.sub(r'^www\.', '', domain)
    return domain


def execute_interaction(stage: Stage, cookie_banner_info: dict, llm_response: dict, attempt: int, interaction_type: BannerInteraction) -> InteractionResult:
    """
    Executes a cookie banner interaction based on the specified interaction type and LLM response.

    This function performs an interaction on a cookie banner by:
      - Extracting the expected target text from the llm_response using the provided interaction type.
      - Clicking the element that matches the target text for clickable elements in the cookie banner.
      - Taking screenshots before and after clicking.
      - Checking for unintended navigation (e.g., page redirection or opening of new tabs) and handling them.
      - Verifying if the cookie banner is dismissed after the click.

    The function returns an InteractionState that indicates:
      - Whether the interaction succeeded.
      - Whether any redirection occurred.
      - How many clicks were performed during the interaction.

    Parameters:
        stage (Stage): The current stage context used for screenshot capturing and logging.
        cookie_banner_info (dict): A dictionary containing details of the cookie banner, including its element.
        llm_response (dict): A dictionary containing LLM-generated responses. It must include keys corresponding to the
                             interaction types: "Accept", "Decline", "Settings", and "Save Settings".
        attempt (int): The current attempt number, used for naming screenshots.
        interaction_type (BannerInteraction): The type of interaction to execute. Must be one of the defined
                                                BannerInteraction enum values.

    Returns:
        InteractionResult: An object representing the result of the interaction, including:
            - result: InteractionResult.SUCCESS if the interaction succeeded, or InteractionResult.FAILED otherwise.
            - redirected: A boolean indicating whether the page was redirected or new tabs were opened.
            - num_clicks: The number of clicks performed during the interaction.

    Raises:
        ValueError: If the provided interaction_type is not recognized.
        MissingLLMResponseKeyError: If the expected key for the interaction_type is missing or empty in llm_response.
    """
    key_map = {
        BannerInteraction.ACCEPT: "Accept",
        BannerInteraction.DECLINE: "Decline",
        BannerInteraction.SETTINGS: "Settings",
        BannerInteraction.SAVE: "Save Settings",
    }

    key = key_map.get(interaction_type)
    if key is None:
        raise ValueError(f"Invalid interaction type: {interaction_type}")

    if key not in llm_response or not llm_response[key]:
        raise MissingLLMResponseKeyError(key)

    target_text = llm_response[key].strip().lower()

    interaction_result = False
    redirected = False
    any_force_clicks = False
    num_clicks = 0

    for ce in cookie_banner_info["clickable_elements"]:
        element_text = ce["text"].strip().lower()

        if target_text == element_text and element_text != "":
            num_clicks += 1

            logger.info(f"Clicking Target Button: {ce['text']!r}")

            filename = processor_helper.get_interaction_screenshot_filename(interaction_type, attempt, click_num=num_clicks)
            _take_screenshot(stage, filename, ce["element"])

            page_before = page.url
            existing_pages = context.pages  # Get the list of open tabs before clicking

            try:
                stage.interactions.append(f"Clicking an element of type ({ce['type']}), with text ({ce['text']})")
                ce["element"].click(timeout=3000)
            except TimeoutError:
                if ce["type"] not in ("div", "span"):
                    logger.warning("Normal click failed, attempting force click.")
                    any_force_clicks = True
                    try:
                        stage.interactions.append(f"Forcing a click on an element of type ({ce['type']}), with text ({ce['text']})")
                        ce["element"].evaluate("el => el.click()")
                    except Exception:
                        logger.error("Force click also failed. Click failed for interactive element.")
                else:
                    logger.error(f"Click failed for interactive element of type {ce['type']}.")
            except Exception as ex:
                error_msg = f"Exception occurred while executing interaction: {str(ex)}"
                logger.error(error_msg)
                stage.exceptions.append(error_msg)
                break

            if interaction_type == BannerInteraction.SETTINGS:
                page.wait_for_timeout(5000)
            else:
                page.wait_for_timeout(2500)

            page_after = page.url
            new_tabs = [p for p in context.pages if p not in existing_pages]
            logger.info(f"Before interaction: page=({page_before}), num_tabs=({len(existing_pages)}). "
                         f"Page after interaction: page=({page_after}), num_new_tabs=({len(new_tabs)}).")

            if page_before.rstrip("#") != page_after.rstrip("#"):
                logger.warning(
                    f"Redirected from ({page_before}) to ({page_after}) after interaction. Returning to root.")

                filename = processor_helper.get_interaction_screenshot_filename(
                    interaction_type,
                    attempt,
                    click_num=num_clicks,
                    suffix="FAIL_redirected"
                )
                _take_screenshot(stage, filename)

                # If this raises an exception, means that we could not return to the root page, which means that we are in
                # invalid state, so we allow for the exception to propagate
                _visit_page(root_web_page, stage)
                redirected = True
                break

            if new_tabs:
                logger.warning(f"Detected {len(new_tabs)} new tab(s). Closing them...")

                for i, new_page in enumerate(new_tabs):
                    filename = processor_helper.get_interaction_screenshot_filename(
                        interaction_type,
                        attempt,
                        click_num=num_clicks,
                        suffix=f"FAIL_new_tabs_{i}"
                    )
                    _take_screenshot(stage, filename, new_page)

                    logger.info(f"Closing tab: {new_page.url}")
                    new_page.close()
                logger.info("All new tabs closed.")
                redirected = True
                break

            # For SETTINGS or SAVE interactions, exit immediately.
            if interaction_type == BannerInteraction.SETTINGS:
                interaction_result = True
                break

            if not is_element_actually_visible(cookie_banner_info['element']):
                if not cookie_banner_info['is_visible']:
                    logger.warning("Interaction button may have been successful and the banner is gone, however previous state was also invisible")
                else:
                    logger.info("Interaction button clicked successfully, banner is gone.")

                interaction_result = True
                break

            logger.info("Banner is still visible after interaction.")

    status = "SUCCESS" if interaction_result else "FAIL"
    filename = processor_helper.get_interaction_screenshot_filename(interaction_type, attempt, suffix=status)
    _take_screenshot(stage, filename)

    return InteractionResult(
        result=InteractionStatus.SUCCESS if interaction_result else InteractionStatus.FAILED,
        redirected=redirected,
        num_clicks=num_clicks,
        any_force_clicks=any_force_clicks
    )


def execute_accept_operator(stage: Stage, attempt: int) -> InteractionStatus:
    """
    Attempts to find and interact with the accept button on a cookie banner.
    Returns the final interaction result indicating success or specific failure mode.
    """
    _take_screenshot(stage, f"accept_init_{attempt}.png")

    # Initialize metadata with default values
    stage_metadata = initialize_metadata_accept_stage(
        num_attempt=attempt,
        num_crawls=local_config['num_crawls'],
        allow_invisible=local_config['allow_invisible'],
        llm_model_used=local_config['model'],
        min_consensus=local_config['min_consensus'],
        num_llm_attempts=local_config['num_llm_attempts'],
        strict_consensus=local_config['strict_consensus']
    )

    stage_metadata.main_level.level_reached = True

    # Find initial banner
    candidate_result = find_best_candidate(stage, page.main_frame)
    candidate = candidate_result['candidate']
    raw_llm_response = candidate_result['raw_llm_response']
    parsed_llm_response = candidate_result['parsed_llm_response']
    consensus_ratio = candidate_result['consensus_ratio']
    consensus_reached = candidate_result['consensus_reached']

    if not candidate:
        stage_metadata.stage_outcome = StageOutcome.NO_BANNER.name
        stage.metadata = stage_metadata.model_dump()
        return InteractionStatus.NOT_FOUND

    if not raw_llm_response or not parsed_llm_response or not consensus_ratio:
        stage_metadata.stage_outcome = StageOutcome.UNSUCCESSFUL_INTERACTION.name
        stage.metadata = stage_metadata.model_dump()
        return InteractionStatus.FAILED

    _take_screenshot(stage, f"accept_best_candidate_{attempt}.png", candidate['element'])

    # Update metadata with banner information
    stage_metadata.main_level.found_best_candidate = True
    stage_metadata.main_level.is_visible = candidate["is_visible"]
    stage_metadata.main_level.banner_text = candidate["text"][:1000]
    stage_metadata.main_level.banner_z_index = candidate["z_index"]
    stage_metadata.main_level.banner_position = candidate["position"]
    stage_metadata.main_level.llm_response_raw = raw_llm_response
    stage_metadata.main_level.llm_response_parsed = parsed_llm_response
    stage_metadata.main_level.llm_consensus_value = consensus_ratio
    stage_metadata.main_level.llm_consensus_reached = consensus_reached

    # Check for accept button
    accept_text = parsed_llm_response.get("Accept")
    if not accept_text:
        _take_screenshot(stage, f"accept_best_candidate_NO_BUTTONS_{attempt}.png", candidate['element'])
        stage_metadata.stage_outcome = StageOutcome.UNSUCCESSFUL_INTERACTION.name
        stage.metadata = stage_metadata.model_dump()
        return InteractionStatus.FAILED

    stage_metadata.main_level.element_text = accept_text
    stage_metadata.main_level.element_ambiguous = parsed_llm_response.get("AcceptAmbiguous")
    stage_metadata.main_level.element_evidence = parsed_llm_response.get("AcceptEvidence")

    # Try to click accept button
    interaction_state = execute_interaction(
        stage,
        candidate,
        parsed_llm_response,
        attempt,
        BannerInteraction.ACCEPT
    )

    stage_metadata.main_level.banner_disappeared = interaction_state.result == InteractionStatus.SUCCESS
    stage_metadata.main_level.redirected = interaction_state.redirected
    stage_metadata.main_level.num_clicks = interaction_state.num_clicks
    stage_metadata.main_level.any_force_clicks = interaction_state.any_force_clicks

    if interaction_state.result == InteractionStatus.SUCCESS and not interaction_state.redirected and interaction_state.num_clicks > 0:
        stage_metadata.main_level.level_success = True
        stage_metadata.stage_outcome = StageOutcome.DIRECT_ACCEPT.name
    else:
        stage_metadata.stage_outcome = StageOutcome.UNSUCCESSFUL_INTERACTION.name

    stage.metadata = stage_metadata.model_dump()

    return interaction_state.result

def _take_screenshot(stage: Stage, screenshot_path: str, element=None):
    def count_screenshots(stage):
        return len(stage.screenshots) if stage and stage.screenshots else 0

    if not website_crawl.take_screenshots:
        return

    num_screenshots = count_screenshots(getattr(website_crawl, "accept_stage", None)) + \
                          count_screenshots(getattr(website_crawl, "decline_stage", None))

    screenshot_path = f"{num_screenshots:03}_" + screenshot_path

    try:
        screenshot_output_path = root_output_path / screenshot_path
        if not element:
            page.screenshot(path=screenshot_output_path, timeout=5000)
        else:
            element.screenshot(path=screenshot_output_path, timeout=5000)
        stage.screenshots.append(screenshot_output_path.name)
    except Exception as e:
        error_msg = f"Error taking screenshot of banner: {str(e)}"
        logger.error(error_msg)
        stage.exceptions.append(error_msg)


def execute_accept_initializer(stage: Stage) -> None:
    # First attempt
    logger.info("Initiating first accept interaction attempt")
    result = execute_accept_operator(stage, attempt=1)

    if result == InteractionStatus.SUCCESS:
        logger.info("Successfully completed accept interaction on first attempt.")
        return

    if result == InteractionStatus.FAILED:
        logger.warning("Accept interaction failed on first attempt - banner found but interaction failed.")
        return

    if result == InteractionStatus.NOT_FOUND:
        logger.info("Cookie banner not found on first attempt - Attempting to perform interaction.")

        # Reset and try alternative approaches
        stage.metadata = {}
        _simulate_scroll_interaction(stage)
        _crawl_internal_pages(stage, max_pages=2)

        # Second attempt
        logger.info("Initiating second accept interaction attempt")
        result = execute_accept_operator(stage, attempt=2)

        if result == InteractionStatus.SUCCESS:
            logger.info("Successfully completed accept interaction on second attempt")
        elif result == InteractionStatus.FAILED:
            logger.warning("Accept interaction failed on second attempt - banner found but interaction failed")
        else:
            logger.info("Cookie banner not found after all attempts")


def _parse_save_query_response(message: str) -> dict:
    """Parse save query response from LLM."""
    parsed = _parse_message(message, ["Save Settings", "Explanation"])
    return parsed

def _parse_message(message: str, required_fields: list[str]) -> dict[str, Optional[str]]:
    """Helper method to parse messages with a consistent format."""
    parsed_data = {field: None for field in required_fields}
    pattern = re.compile(f"^({'|'.join(required_fields)}):\\s*(.*)$")

    found_fields = set()
    for line in message.strip().splitlines():
        match = pattern.match(line.strip())
        if match:
            key, value = match.groups()
            found_fields.add(key)
            value = value.strip().replace('[', '').replace(']', '')
            parsed_data[key] = None if value.lower() == "none" else value.strip()

    missing_fields = set(required_fields) - found_fields
    if missing_fields:
        raise ValueError(f"Missing required fields: {missing_fields}")

    return parsed_data


def _parse_normal_query_response(message: str) -> dict:
    """Parse normal query response from LLM and include ambiguity flags and evidence of source fields."""
    parsed = _parse_message(
        message,
        [
            "GenericLabel1", "GenericLabel2",
            "AmbiguousLabel1", "AmbiguousLabel2",
            "GenericLabel3", "Explanation"
        ]
    )

    # Process Accept field:
    if parsed["GenericLabel1"]:
        accept_value = parsed["GenericLabel1"]
        accept_ambiguous = False
        accept_evidence = "GenericLabel1"
    elif parsed["AmbiguousLabel1"]:
        accept_value = parsed["AmbiguousLabel1"]
        accept_ambiguous = True
        accept_evidence = "AmbiguousLabel1"
    else:
        accept_value = None
        accept_ambiguous = False
        accept_evidence = None

    # Process Decline field:
    if parsed["GenericLabel2"]:
        decline_value = parsed["GenericLabel2"]
        decline_ambiguous = False
        decline_evidence = "GenericLabel2"
    elif parsed["AmbiguousLabel2"]:
        decline_value = parsed["AmbiguousLabel2"]
        decline_ambiguous = True
        decline_evidence = "AmbiguousLabel2"
    elif parsed["GenericLabel1"]:
        # Fallback: if there's a GenericLabel1 but no explicit generic decline,
        # use AmbiguousLabel1 (if available) as evidence.
        decline_value = parsed["AmbiguousLabel1"]
        decline_ambiguous = bool(parsed["AmbiguousLabel1"])
        decline_evidence = "AmbiguousLabel1" if parsed["AmbiguousLabel1"] else None
    else:
        decline_value = None
        decline_ambiguous = False
        decline_evidence = None

    return {
        "Accept": accept_value,
        "AcceptAmbiguous": accept_ambiguous,
        "AcceptEvidence": accept_evidence,
        "Decline": decline_value,
        "DeclineAmbiguous": decline_ambiguous,
        "DeclineEvidence": decline_evidence,
        "Settings": parsed["GenericLabel3"],
        "SettingsEvidence": "GenericLabel3" if bool(parsed["GenericLabel3"]) else None,
        "Explanation": parsed["Explanation"]
    }


def execute_decline_initializer(stage: Stage):
    logger.info("Initiating first decline interaction attempt")
    result = execute_decline_operator(stage, attempt=1)

    if result == InteractionStatus.SUCCESS:
        logger.info("Successfully completed decline interaction on first attempt")
        return

    if result == InteractionStatus.FAILED:
        logger.warning("Decline interaction failed on first attempt - banner found but interaction failed")
        return

    if result == InteractionStatus.NOT_FOUND:
        logger.info("Cookie banner not found on first attempt - Attempting to perform interaction.")

        # Reset and try alternative approaches
        stage.metadata = {}
        _simulate_scroll_interaction(stage)
        _crawl_internal_pages(stage, max_pages=2)

        # Second attempt
        logger.info("Initiating second decline interaction attempt")
        result = execute_decline_operator(stage, attempt=2)

        if result == InteractionStatus.SUCCESS:
            logger.info("Successfully completed decline interaction on second attempt")
        elif result == InteractionStatus.FAILED:
            logger.warning("Decline interaction failed on second attempt - banner found but interaction failed")
        else:
            logger.info("Cookie banner not found after all attempts")


def execute_decline_operator(stage: Stage, attempt: int) -> InteractionStatus:
    _take_screenshot(stage, f"decline_init_{attempt}.png")

    stage_metadata = initialize_metadata_decline_stage(
        num_attempt=attempt,
        num_crawls=local_config['num_crawls'],
        allow_invisible=local_config['allow_invisible'],
        llm_model_used=local_config['model'],
        min_consensus=local_config['min_consensus'],
        num_llm_attempts=local_config['num_llm_attempts'],
        strict_consensus=local_config['strict_consensus']
    )

    stage_metadata.main_level.level_reached = True

    candidate_result = find_best_candidate(stage, page.main_frame)
    candidate = candidate_result['candidate']
    raw_llm_response = candidate_result['raw_llm_response']
    parsed_llm_response = candidate_result['parsed_llm_response']
    consensus_ratio = candidate_result['consensus_ratio']
    consensus_reached = candidate_result['consensus_reached']

    if not candidate:
        stage_metadata.stage_outcome = StageOutcome.NO_BANNER.name
        stage.metadata = stage_metadata.model_dump()
        return InteractionStatus.NOT_FOUND

    if not raw_llm_response or not parsed_llm_response or not consensus_ratio:
        stage_metadata.stage_outcome = StageOutcome.UNSUCCESSFUL_INTERACTION.name
        stage.metadata = stage_metadata.model_dump()
        return InteractionStatus.FAILED

    _take_screenshot(stage, f"decline_best_candidate_{attempt}.png", candidate['element'])

    stage_metadata.main_level.found_best_candidate = True
    stage_metadata.main_level.is_visible = candidate["is_visible"]
    stage_metadata.main_level.banner_text = candidate["text"][:1000]
    stage_metadata.main_level.banner_z_index = candidate["z_index"]
    stage_metadata.main_level.banner_position = candidate["position"]
    stage_metadata.main_level.llm_response_raw = raw_llm_response
    stage_metadata.main_level.llm_response_parsed = parsed_llm_response
    stage_metadata.main_level.llm_consensus_value = consensus_ratio
    stage_metadata.main_level.llm_consensus_reached = consensus_reached

    decline_text = parsed_llm_response.get("Decline")
    settings_text = parsed_llm_response.get("Settings")

    if not (decline_text or settings_text):
        _take_screenshot(stage, f"decline_best_candidate_NO_BUTTONS_{attempt}.png")
        stage_metadata.stage_outcome = StageOutcome.UNSUCCESSFUL_INTERACTION.name
        stage.metadata = stage_metadata.model_dump()
        return InteractionStatus.FAILED

    stage_metadata.main_level.direct_decline_attempt = bool(decline_text)

    if decline_text:
        stage_metadata.main_level.element_text = decline_text
        stage_metadata.main_level.element_ambiguous = parsed_llm_response.get("DeclineAmbiguous")
        stage_metadata.main_level.element_evidence = parsed_llm_response.get("DeclineEvidence")
    else:
        stage_metadata.main_level.element_text = settings_text
        stage_metadata.main_level.element_ambiguous = None
        stage_metadata.main_level.element_evidence = parsed_llm_response.get("SettingsEvidence")

    # Attempt with either Decline and Settings
    interaction_state = execute_interaction(
        stage,
        candidate,
        parsed_llm_response,
        attempt,
        BannerInteraction.DECLINE if stage_metadata.main_level.direct_decline_attempt else BannerInteraction.SETTINGS
    )

    stage_metadata.main_level.banner_disappeared = interaction_state.result == InteractionStatus.SUCCESS
    stage_metadata.main_level.redirected = interaction_state.redirected
    stage_metadata.main_level.num_clicks = interaction_state.num_clicks
    stage_metadata.main_level.any_force_clicks = interaction_state.any_force_clicks

    # If the attempt was decline then we exit early
    if decline_text:
        if interaction_state.result == InteractionStatus.SUCCESS and not interaction_state.redirected and interaction_state.num_clicks > 0:
            stage_metadata.main_level.level_success = True
            stage_metadata.stage_outcome = StageOutcome.DIRECT_DECLINE.name
        else:
            stage_metadata.stage_outcome = StageOutcome.UNSUCCESSFUL_INTERACTION.name
        stage.metadata = stage_metadata.model_dump()
        return interaction_state.result

    # If the attempt was settings, but we got redirected or didn't click anything
    if interaction_state.result != InteractionStatus.SUCCESS or interaction_state.redirected or interaction_state.num_clicks == 0:
        stage_metadata.stage_outcome = StageOutcome.UNSUCCESSFUL_INTERACTION.name
        stage.metadata = stage_metadata.model_dump()
        return interaction_state.result

    stage_metadata.settings_level.level_reached = True

    candidate_result = find_best_candidate(stage, page.main_frame)
    candidate = candidate_result['candidate']
    raw_llm_response = candidate_result['raw_llm_response']
    parsed_llm_response = candidate_result['parsed_llm_response']
    consensus_ratio = candidate_result['consensus_ratio']
    consensus_reached = candidate_result['consensus_reached']

    if not candidate or not raw_llm_response or not parsed_llm_response or not consensus_ratio:
        stage_metadata.stage_outcome = StageOutcome.UNSUCCESSFUL_INTERACTION.name
        stage.metadata = stage_metadata.model_dump()
        return InteractionStatus.FAILED

    _take_screenshot(stage, f"decline_settings_best_candidate_{attempt}.png", candidate['element'])

    stage_metadata.settings_level.found_best_candidate = True
    stage_metadata.settings_level.is_visible = candidate["is_visible"]
    stage_metadata.settings_level.banner_text = candidate["text"][:1000]
    stage_metadata.settings_level.banner_z_index = candidate["z_index"]
    stage_metadata.settings_level.banner_position = candidate["position"]
    stage_metadata.settings_level.settings_decline_llm_response_raw = raw_llm_response
    stage_metadata.settings_level.settings_decline_llm_response_parsed = parsed_llm_response
    stage_metadata.settings_level.settings_decline_llm_consensus_value = consensus_ratio
    stage_metadata.settings_level.settings_decline_llm_consensus_reached = consensus_reached

    # Attempt with Decline of Settings if present
    decline_text = parsed_llm_response.get("Decline")
    if decline_text:
        stage_metadata.settings_level.settings_decline_attempt = True
        stage_metadata.settings_level.settings_decline_element_text = decline_text
        stage_metadata.settings_level.settings_decline_element_ambiguous = parsed_llm_response.get("DeclineAmbiguous")
        stage_metadata.settings_level.settings_decline_element_evidence = parsed_llm_response.get("DeclineEvidence")

        interaction_state = execute_interaction(
            stage,
            candidate,
            parsed_llm_response,
            attempt,
            BannerInteraction.DECLINE
        )

        stage_metadata.settings_level.banner_disappeared = interaction_state.result == InteractionStatus.SUCCESS
        stage_metadata.settings_level.redirected = interaction_state.redirected
        stage_metadata.settings_level.settings_decline_num_clicks = interaction_state.num_clicks
        stage_metadata.settings_level.settings_decline_any_force_clicks = interaction_state.any_force_clicks

        if interaction_state.result == InteractionStatus.SUCCESS and not interaction_state.redirected and interaction_state.num_clicks > 0:
            stage_metadata.settings_level.level_success = True
            stage_metadata.stage_outcome = StageOutcome.SETTINGS_DECLINE.name
            stage.metadata = stage_metadata.model_dump()
            return interaction_state.result
        elif interaction_state.redirected:
            stage_metadata.stage_outcome = StageOutcome.UNSUCCESSFUL_INTERACTION.name
            stage.metadata = stage_metadata.model_dump()
            return InteractionStatus.FAILED

        # Rerender clickable elements within the banner
        candidate["clickable_elements"] = find_clickable_elements_within_element(candidate["element"])


    # Decline button either not present in settings or the banner did not disappear after the interaction attempt
    clickable_texts = [
        ce['text'].strip()
        for ce in candidate["clickable_elements"]
        if '\n' not in ce['text'].strip()
    ]
    formatted_text = "\n".join(f"[{text}]" for text in set(clickable_texts))

    responses = _get_llm_responses(
        formatted_text=formatted_text,
        num_attempts=local_config["num_llm_attempts"],
        use_save_prompt=True
    )

    if not responses:
        stage_metadata.stage_outcome = StageOutcome.UNSUCCESSFUL_INTERACTION.name
        stage.metadata = stage_metadata.model_dump()
        return InteractionStatus.FAILED

    try:
        best_raw_response, best_parsed_response, consensus_ratio, consensus_reached = _get_llm_consensus(
            responses=responses,
            min_consensus=local_config["min_consensus"],
            strict_consensus=local_config["strict_consensus"],
            use_save_prompt=True
        )
    except Exception as ex:
        error_msg = f"Exception occurred while selecting best response: {str(ex)}"
        logger.error(error_msg)
        stage.exceptions.append(error_msg)
        stage_metadata.stage_outcome = StageOutcome.UNSUCCESSFUL_INTERACTION.name
        stage.metadata = stage_metadata.model_dump()
        return InteractionStatus.FAILED

    stage_metadata.settings_level.save_settings_llm_response_raw = best_raw_response
    stage_metadata.settings_level.save_settings_llm_response_parsed = best_parsed_response
    stage_metadata.settings_level.save_settings_llm_consensus_value = consensus_ratio
    stage_metadata.settings_level.save_settings_llm_consensus_reached = consensus_reached

    save_settings_text = best_parsed_response.get("Save Settings")
    if not save_settings_text:
        stage_metadata.stage_outcome = StageOutcome.UNSUCCESSFUL_INTERACTION.name
        stage.metadata = stage_metadata.model_dump()
        return InteractionStatus.FAILED

    stage_metadata.settings_level.save_settings_attempt = True
    stage_metadata.settings_level.settings_decline_element_text = save_settings_text

    interaction_state = execute_interaction(
        stage,
        candidate,
        best_parsed_response,
        attempt,
        BannerInteraction.SAVE
    )

    stage_metadata.settings_level.banner_disappeared = interaction_state.result == InteractionStatus.SUCCESS
    stage_metadata.settings_level.redirected = interaction_state.redirected
    stage_metadata.settings_level.save_settings_num_clicks = interaction_state.num_clicks
    stage_metadata.settings_level.save_settings_any_force_clicks = interaction_state.any_force_clicks

    if interaction_state.result == InteractionStatus.SUCCESS and not interaction_state.redirected and interaction_state.num_clicks > 0:
        stage_metadata.settings_level.level_success = True
        stage_metadata.stage_outcome = StageOutcome.SETTINGS_SAVE.name
    else:
        stage_metadata.stage_outcome = StageOutcome.UNSUCCESSFUL_INTERACTION.name

    stage.metadata = stage_metadata.model_dump()

    return interaction_state.result

def _query_normal_user_prompt(user_prompt: str) -> tuple[str | None, dict | None]:
    """Query LLM with normal prompt and parse response."""
    try:
        response = _query_llm_client(local_config["messages"]["normal_prompt"], user_prompt)
        if response:
            return response, _parse_normal_query_response(response)
        return None, None
    except Exception as e:
        logging.error(f"Normal prompt query failed: {str(e)}")
        return None, None

def _query_save_user_prompt(user_prompt: str) -> tuple[str | None, dict | None]:
    """Query LLM with save prompt and parse response."""
    try:
        response = _query_llm_client(local_config["messages"]["save_prompt"], user_prompt)
        if response:
            return response, _parse_save_query_response(response)
        return None, None
    except Exception as e:
        logging.error(f"Save prompt query failed: {str(e)}")
        return None, None

def _query_llm_client(system_prompt: str, user_prompt: str) -> Optional[str]:
    """Query OpenAI LLM with given prompts."""
    try:
        client = OpenAI(api_key=local_config["openai_token"])
        session_token = str(uuid.uuid4())[:8]
        modified_prompt = f"[Session: {session_token}] {user_prompt}"
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": modified_prompt}
        ]

        completion = client.chat.completions.create(
            model=local_config["model"],
            messages=messages,
            temperature=0.8
        )

        response = completion.choices[0].message.content
        logger.info(f"LLM response for session {session_token}:\n{response}")
        return response
    except Exception as e:
        logger.error(f"LLM query failed: {str(e)}")
        return None


def _simulate_scroll_interaction(stage: Stage):
    """
    Simulates scrolling interaction to mimic user behavior.
    """
    logger.debug("Simulating scroll interaction")
    for _ in range(3):
        page.mouse.wheel(delta_x=0, delta_y=500)  # Scroll down by 500 pixels
        page.wait_for_timeout(250)
    stage.interactions.append("Scrolled 3 times (500x each)")


def _gather_cookie_element_handles_in_frame(frame, cookie_words: list):
    """
    Gathers element handles in the frame that potentially represent cookie banners.

    This function:
      1) Executes a single JavaScript snippet that recursively traverses the entire DOM,
         including any open shadow roots. The snippet:
             - Checks each element’s text content for any occurrence of the cookie-related words.
             - Applies heuristics to determine "banner-likeness" based on computed styles,
               such as a z-index greater than 0 or a fixed/sticky position.
         The matching elements are collected in an array.
      2) Converts the resulting JavaScript array handle into a Python list of ElementHandle objects.

    Parameters:
        frame (Frame): The frame in which to search for cookie banner element handles.
        cookie_words (list): A list of cookie-related keywords to look for in element text.

    Returns:
        list: A list of ElementHandle objects corresponding to elements that are potential cookie banners.
    """

    js_code = """(words) => {
      const results = [];
      const visited = new Set();

      function walk(node) {
        // Stop if node is null or we've already visited it
        if (!node || visited.has(node)) return;
        visited.add(node);

        if (
          node.nodeType === Node.ELEMENT_NODE ||
          node.nodeType === Node.DOCUMENT_FRAGMENT_NODE
        ) {
          if (node.nodeType === Node.ELEMENT_NODE) {
            const el = node;
            const text = (el.textContent || "").toLowerCase();
            const hasCookieText = words.some((w) => text.includes(w));

            if (hasCookieText) {
              const style = window.getComputedStyle(el);
              const zIndexVal = parseInt(style.zIndex, 10);
              const positionVal = style.position; // "absolute", "fixed", "sticky", etc.

              // Heuristic for "banner-likeness":
              // 1) zIndex > 0, or
              // 2) position is fixed/sticky
              const isBannerLikely =
                (!Number.isNaN(zIndexVal) && zIndexVal > 0) ||
                positionVal === "fixed" ||
                positionVal === "sticky";

              if (isBannerLikely) {
                results.push(el);
              }
            }
          }

          // If there's an open shadow root, recurse into it
          if (node.shadowRoot) {
            walk(node.shadowRoot);
          }

          // Recurse child elements
          const children = node.children || [];
          for (let i = 0; i < children.length; i++) {
            walk(children[i]);
          }
        }
      }

      walk(document.documentElement);
      return results;
    }
    """

    try:
        handle_array = frame.evaluate_handle(js_code, cookie_words)
    except Exception as ex:
        logger.error(f"Failed at gathering cookie element. Returning an empty list. Reason: {ex}")
        return []

    # Convert the JavaScript array handle into a Python list of ElementHandles.
    element_handles = []
    properties = handle_array.get_properties()
    for _, js_handle in properties.items():
        el = js_handle.as_element()
        if el is not None:
            element_handles.append(el)

    # Dispose the array handle to avoid memory leaks.
    handle_array.dispose()

    return element_handles


def find_all_possible_cookie_banners(frame: Frame) -> list[dict]:
    """
    Recursively finds all possible cookie banner elements within the given frame and its child frames.

    The function works as follows:
      - It first checks if the provided frame is detached or has an invalid URL (e.g., empty or "about:blank").
      - It gathers potential cookie banner elements from the current frame by calling
        `find_cookie_banners_in_frame(frame, allow_invisible)`.
      - It then recursively processes each child frame (if not detached and has a valid URL)
        by calling itself.
      - All found banner dictionaries are combined and then sorted based on:
          1. Descending z-index (i.e., banners with higher z-index first),
          2. Top coordinate (y position), and
          3. Left coordinate (x position).

    Parameters:
        frame (Frame): The frame to search for cookie banners.

    Returns:
        list[dict]: A sorted list of dictionaries representing cookie banners.
                    Each dictionary contains keys such as "element", "clickable_elements",
                    "text", "z_index", "top", "left", and "is_visible".
    """
    if frame.is_detached() or not frame.url or frame.url.strip() == "" or frame.url == "about:blank":
        return []

    # Gather banners in this frame
    banners_here = find_cookie_banners_in_frame(frame)

    # Recur on child frames
    all_banners = list(banners_here)
    for child in frame.child_frames:
        if not child.is_detached() and child.url and child.url.strip() != "" and child.url != "about:blank":
            child_banners = find_all_possible_cookie_banners(child)
            all_banners.extend(child_banners)

    # Sort them by z-index desc, then top (y), then left (x)
    all_banners.sort(key=lambda x: (-x["is_visible"], -x["z_index"], x["top"], x["left"]))

    return all_banners

def find_best_candidate(
    stage: "Stage",
    frame: "Frame",
    num_attempts: int = local_config["num_llm_attempts"],
    min_consensus: float = local_config["min_consensus"],
    strict_consensus: bool = local_config["strict_consensus"]
) -> dict[str, Any]:
    """
    Find best cookie banner candidate using multiple LLM queries.

    Args:
        stage: Current processing stage
        frame: Frame containing potential cookie banners
        num_attempts: Number of LLM queries to make for consensus
        min_consensus: Minimum ratio needed for consensus
        strict_consensus: Flag indicating that we use strict consensus

    Returns:
        A dictionary with the following keys:
            - "candidate": dict | None
            - "raw_response": str | None
            - "parsed_response": dict | None
            - "consensus_ratio": float | None
            - "consensus_reached": bool | None
    """
    # Try to find all possible cookie banners
    candidates = find_all_possible_cookie_banners(frame)

    # If still no candidates found, return everything as None
    if not candidates:
        return {
            "candidate": None,
            "raw_llm_response": None,
            "parsed_llm_response": None,
            "consensus_ratio": None,
            "consensus_reached": None,
        }

    # Iterate over each candidate to see if we can get an LLM consensus
    for candidate in candidates:
        if not candidate["is_visible"] and not local_config["allow_invisible"]:
            continue

        # Prepare the text prompt
        clickable_texts = [
            ce['text'].strip()
            for ce in candidate["clickable_elements"]
            if '\n' not in ce['text'].strip()
        ]
        formatted_text = "\n".join(f"[{text}]" for text in set(clickable_texts))

        # Get multiple responses using our helper
        responses = _get_llm_responses(
            formatted_text=formatted_text,
            num_attempts=num_attempts
        )

        if not responses:
            continue

        # If we got valid responses, attempt to select the best one
        try:
            best_raw_response, best_parsed_response, consensus_ratio, consensus_reached = _get_llm_consensus(
                responses=responses,
                min_consensus=min_consensus,
                strict_consensus=strict_consensus
            )
        except Exception as ex:
            error_msg = f"Exception occurred while selecting best response: {str(ex)}"
            logger.error(error_msg)
            stage.exceptions.append(error_msg)
            continue

        # Check if the best parsed response has an actual action (Accept, Decline, etc.)
        #    If it does, we consider this candidate "valid" and return it.
        if any(best_parsed_response.get(key) for key in ["Accept", "Decline", "Settings", "Save Settings"]):
            return {
                "candidate": candidate,
                "raw_llm_response": best_raw_response,
                "parsed_llm_response": best_parsed_response,
                "consensus_ratio": consensus_ratio,
                "consensus_reached": consensus_reached,
            }

    # If no suitable candidate was found at all, return all None
    return {
        "candidate": None,
        "raw_llm_response": None,
        "parsed_llm_response": None,
        "consensus_ratio": None,
        "consensus_reached": None,
    }


def _get_llm_responses(
        formatted_text: str,
        num_attempts: int,
        use_save_prompt: bool = False) -> list[tuple[str, dict]]:
    """
    Query the LLM multiple times for the given formatted_text.

    Args:
        formatted_text: The text to pass into the prompt
        num_attempts: Number of times to query the LLM for different responses

    Returns:
        A list of (raw_response, parsed_response) tuples.
    """
    responses = []
    query_fn = _query_save_user_prompt if use_save_prompt else _query_normal_user_prompt
    for _ in range(num_attempts):
        raw_response, parsed_response = query_fn(formatted_text)
        if raw_response and parsed_response:
            responses.append((raw_response, parsed_response))
    return responses

def _get_llm_consensus(
    responses: list[tuple[str, dict]],
    min_consensus: float = 0.6,
    strict_consensus: bool = False,
    use_save_prompt: bool = False
) -> tuple[str, dict, float, bool]:
    """
    Select best response based on frequency, always returns a response.
    Excludes explanation from consensus calculation but keeps it in the final response.

    Args:
        responses: List of tuples where the first element is a str and the second element is a dict
        min_consensus: Minimum ratio needed for consensus (default: 0.6)
        use_save_prompt: Whether to use the 'Save Settings' key instead of 'Accept', 'Decline', 'Settings'
        strict_consensus: Indicates if the function should raise an error if consensus was not reached
    Returns:
        Tuple[str, dict]: The entire tuple whose dict portion is the most frequent pattern (consensus key).
    """
    if not responses:
        raise ValueError("Cannot select from empty responses.")

    def get_consensus_key(parsed_resp: dict) -> Any:
        """
        Get the key used for consensus counting (excluding explanation).
        If 'use_save_prompt' is True, we only consider the 'Save Settings' field.
        Otherwise, we consider the triple (Accept, Decline, Settings).
        """
        if use_save_prompt:
            return parsed_resp.get("Save Settings")
        else:
            return parsed_resp.get("Accept"), parsed_resp.get("Decline"), parsed_resp.get("Settings")

    # Log all responses
    full_log_text = "\nAll parsed responses received:\n"
    for i, (raw_text, parsed_response) in enumerate(responses, start=1):
        if use_save_prompt:
            full_log_text += f"Response {i}: Save Settings={parsed_response.get('Save Settings')}"
        else:
            full_log_text += f"Response {i}: Accept={parsed_response.get('Accept')}, Decline={parsed_response.get('Decline')}, Settings={parsed_response.get('Settings')}; "
        full_log_text += f"Explanation: {parsed_response.get('Explanation')}\n"

    logger.info(full_log_text)

    # Count frequency of patterns (excluding explanation)
    response_counts = Counter(get_consensus_key(parsed_response) for _, parsed_response in responses)

    full_log_text = "\nResponse patterns frequency:\n"
    for pattern, cnt in response_counts.items():
        full_log_text += f"Pattern {pattern}: {cnt} occurrences. \n"

    # Identify most common pattern
    (pattern, count) = response_counts.most_common(1)[0]
    consensus_ratio = count / len(responses)
    consensus_reached = consensus_ratio >= min_consensus

    if consensus_reached:
        logger.info(f"Consensus reached with ratio {consensus_ratio:.2f}")
    elif strict_consensus:
        raise ValueError(f"Consensus not reached. Best ratio was {consensus_ratio:.2f}, needed at least {min_consensus}.")
    else:
        logger.warning(f"No consensus reached. Best ratio was {consensus_ratio:.2f}, needed {min_consensus}. Using most frequent response.")

    # Return the first tuple whose dict matches the most common pattern
    for text_part, parsed_response in responses:
        if get_consensus_key(parsed_response) == pattern:
            if use_save_prompt:
                logger.info(f"Selected pattern (Save Settings): {pattern} -- With explanation: {parsed_response.get('Explanation')}")
            else:
                logger.info(f"Selected pattern (Accept, Decline, Settings): {pattern} -- With explanation: {parsed_response.get('Explanation')}")
            return text_part, parsed_response, consensus_ratio, consensus_reached

    # Should not happen if there's at least one response
    raise ValueError("Could not find response matching the most common pattern")


def find_cookie_banners_in_frame(frame: Frame):
    """
    Searches for cookie banner elements within a single frame.

    The function operates as follows:
      - It gathers all cookie-related keywords from the cookie lexicon (for both English and Slovenian).
      - It calls `_gather_cookie_element_handles_in_frame` to run a JS snippet that recursively
        traverses the DOM (and shadow roots) to collect elements whose text contains any of the cookie keywords
        and which have banner-like characteristics (e.g., a high z-index or fixed/sticky positioning).
      - For each element handle returned, if the element is visible (unless allow_invisible is True),
        the function extracts:
            - The element's text content,
            - Its bounding box (position and size),
            - Its computed z-index,
            - The list of clickable sub-elements (using `find_clickable_elements_within_element`).
      - A dictionary is built for each element containing the above information.

    Parameters:
        frame (Frame): The frame in which to search for cookie banners.

    Returns:
        list[dict]: A list of dictionaries, each representing a cookie banner with details:
            - "element": The ElementHandle for the banner.
            - "clickable_elements": List of clickable sub-elements found within the banner.
            - "text": The text content of the element.
            - "z_index": The computed z-index of the element.
            - "top": The y-coordinate (top) of the element.
            - "left": The x-coordinate (left) of the element.
            - "is_visible": Boolean indicating whether the element is visible.
    """
    # Merge all cookie words from the lexicon
    words_en = [w.lower() for w in cookie_lexicon["words"]["en"]["cookie_words"]]
    words_sl = [w.lower() for w in cookie_lexicon["words"]["sl"]["cookie_words"]]
    all_cookie_words = list(set(words_en + words_sl))  # Remove duplicates if any

    # Get all matching element handles in one pass
    element_handles = _gather_cookie_element_handles_in_frame(frame, all_cookie_words)

    found_banners = []

    for handle in element_handles:
        try:
            text = handle.text_content() or ""
            if text == "":
                continue

            box = handle.bounding_box()
            if not box:
                continue

            z_index = handle.evaluate("el => parseInt(getComputedStyle(el).zIndex) || 0")
            position = handle.evaluate("el => getComputedStyle(el).position")

            clickable_elements = find_clickable_elements_within_element(handle)
            if not clickable_elements:
                continue

            found_banners.append({
                "element": handle,
                "clickable_elements": clickable_elements,
                "text": text.strip(),
                "z_index": z_index,
                "position": position,
                "top": box["y"],
                "left": box["x"],
                "is_visible": is_element_actually_visible(handle)
            })
        except Exception as ex:
            logger.error(f"Exception occurred while parsing handle: {ex}")
            pass

    return found_banners


def is_element_actually_visible(handle):
    """Check if an element is truly visible to the user within the viewport."""
    global page

    # Get bounding box
    box = handle.bounding_box()
    if not box:
        return False  # No bounding box, definitely not visible

    x, y, width, height = box["x"], box["y"], box["width"], box["height"]

    if width == 0 or height == 0:
        return False

    viewport_width, viewport_height = page.viewport_size["width"], page.viewport_size["height"]

    # Check if any part of the element is within the visible viewport
    # Only perform a check for width as we allow the vertical partial invisibility (e.g., banner on the bottom of page)
    partially_visible = (
            (x + width) > 0 and  # Right side is within viewport
            #(y + height) > 0 and  # Bottom side is within viewport
            x < viewport_width  # Left side is within viewport
            # y < viewport_height  # Top side is within viewport
    )

    if not partially_visible:
        return False  # Completely out of viewport

    # Check CSS properties
    display = handle.evaluate("el => window.getComputedStyle(el).display")
    visibility = handle.evaluate("el => window.getComputedStyle(el).visibility")
    opacity = handle.evaluate("el => parseFloat(window.getComputedStyle(el).opacity)")

    if display == "none" or visibility == "hidden" or opacity == 0:
        return False  # Element is hidden via CSS

    return True # Element is visible in viewport and not hidden


def find_clickable_elements_within_element(element):
    """
    Recursively finds clickable sub-elements within the given element.

    The function identifies clickable elements by:
      - Running a JavaScript snippet that walks the DOM (and any open shadow roots) starting from the given element.
      - The snippet collects elements that match common clickable selectors such as:
            - Buttons (e.g., <button>, input[type='button'], input[type='submit'])
            - Links (<a>)
            - Divs and spans (provided they have a CSS cursor style of 'pointer')
      - Once candidate elements are collected, the function:
            - Filters them by ensuring they are visible and have a bounding box.
            - Retrieves their text content.
            - For input elements with no text, attempts to get the value attribute.
            - Assigns a priority based on the element type (e.g., button/input get higher priority).
      - Finally, the list is sorted by the assigned priority (with lower numerical priority meaning higher importance)
        and then returned (in reversed order based on the current implementation).

    Parameters:
        element: The ElementHandle from which to search for clickable sub-elements.

    Returns:
        list[dict]: A list of dictionaries, each representing a clickable element with:
            - "element": The clickable ElementHandle.
            - "text": The text content of the element.
            - "top": The top (y) coordinate from the element's bounding box.
            - "left": The left (x) coordinate from the element's bounding box.
            - "priority": A numerical priority assigned based on the element type.
    """

    js_code = """
    (root) => {
      const results = [];

      function walk(node) {
        if (!node) return;
        if (node.nodeType === Node.ELEMENT_NODE || node.nodeType === Node.DOCUMENT_FRAGMENT_NODE) {

          if (node.nodeType === Node.ELEMENT_NODE) {
            const el = node;
            if (el.matches("button, a, div, span, input[type='button'], input[type='submit']")) {
              results.push(el);
            }
          }

          if (node.shadowRoot) {
            walk(node.shadowRoot);
          }

          const children = node.children || [];
          for (let i = 0; i < children.length; i++) {
            walk(children[i]);
          }
        }
      }

      walk(root);
      return results;
    }
    """

    handle_array = element.evaluate_handle(js_code)

    found_handles = []
    properties = handle_array.get_properties()
    for _, js_handle in properties.items():
        el = js_handle.as_element()
        if el:
            found_handles.append(el)

    handle_array.dispose()

    clickable_items = []
    for el in found_handles:
        try:
            if not is_element_actually_visible(el):
                continue

            tag = el.evaluate("node => node.tagName.toLowerCase()")

            text = el.evaluate('''(node) => {
                function getVisibleText(node) {
                    // For element nodes, check if the node is hidden.
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        const style = getComputedStyle(node);
                        if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') {
                            return '';
                        }
                    }
                    // For text nodes, simply return the text as-is.
                    if (node.nodeType === Node.TEXT_NODE) {
                        return node.textContent;
                    }
                    // For other node types, recursively get the text from child nodes.
                    let result = '';
                    node.childNodes.forEach(child => {
                        result += getVisibleText(child);
                    });
                    return result;
                }
                return getVisibleText(node);
            }''') or ""

            # For input elements with no text, retrieve the value.
            if tag == "input" and not text.strip():
                text = el.evaluate("node => node.value") or ""

            if not text or not text.strip():
                continue

            box = el.bounding_box()
            if not box:
                continue

            # Assign a default priority (lower numbers indicate higher priority)
            priority = 4  # Default for span
            if tag == "button" or tag == "input":
                priority = 1
            elif tag == "a":
                priority = 2
            elif tag in ["div", "span"]:
                if tag == "div":
                    priority = 3
                cursor_style = el.evaluate("node => getComputedStyle(node).cursor")
                if cursor_style != "pointer":
                    continue

            clickable_items.append({
                "element": el,
                "type": tag,
                "text": text.strip(),
                "top": box["y"],
                "left": box["x"],
                "priority": priority
            })
        except Exception:
            pass

    # Sort clickable items by priority (lowest number = highest priority)
    clickable_items.sort(key=lambda x: x["priority"])

    return clickable_items

