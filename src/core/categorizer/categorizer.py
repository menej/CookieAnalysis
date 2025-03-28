import logging
import re
import time
import uuid
from datetime import datetime, timezone

import pandas as pd
import requests
from bs4 import BeautifulSoup
from itertools import chain

from src.core.common import loader
from src.entities.enums.CookieCategory import CookieCategory
from src.entities.models.WebsiteCrawl import WebsiteCrawl

logger = logging.getLogger(__name__)

global_config = loader.load_config()

last_request_time = {}
THROTTLE_SECONDS_MID = 10
THORTTLE_SECONDS_HIGH = 30


def process_crawl(crawl: WebsiteCrawl):
    for cookies in chain(
            crawl.normal_stage.stage_cookies.values() if crawl.normal_stage and crawl.normal_stage.stage_cookies else [],
            crawl.accept_stage.stage_cookies.values() if crawl.accept_stage and crawl.accept_stage.stage_cookies else [],
            crawl.decline_stage.stage_cookies.values() if crawl.decline_stage and crawl.decline_stage.stage_cookies else []):
        for cookie in cookies:
            name = cookie['name']

            # Handle scenario when the cookie name is empty
            if not name.strip():
                cookie['categorization'] = {
                    'platform': "Cookie Analysis",
                    'cookie_category': CookieCategory.UNKNOWN.name,
                }
                continue

            platform, cookie_category = _categorize(name)

            cookie['categorization'] = {
                'platform': platform,
                'cookie_category': cookie_category.name,
            }


def wildcard_to_regex(wildcard_pattern: str) -> re.Pattern | None:
    """
    Converts a 'wildcard' pattern (e.g., '_ga_*') into a case-sensitive regex pattern.

    The wildcard (*) can be replaced with:
    - Alphanumeric characters [A-Za-z0-9]
    - Underscore (_)
    - Hyphen (-)
    - Period (.)

    If the prefix doesn't end with punctuation, the first character after the
    wildcard must be a punctuation character (_, -, .).

    Args:
        wildcard_pattern: A string containing exactly one wildcard (*)

    Returns:
        A compiled regex pattern or None if invalid (no wildcard or multiple wildcards)
    """

    pattern = wildcard_pattern.strip()
    if "*" not in pattern or pattern.count('*') > 1:
        return None

    prefix = pattern.split('*', 1)[0]
    escaped_prefix = re.escape(prefix)

    # Check if the prefix ends with punctuation
    if prefix and prefix[-1] in ['_', '.', '-']:
        # If it already ends with punctuation, any valid character can follow
        regex_str = f"^{escaped_prefix}[A-Za-z0-9._-]+$"
    else:
        # If not, require punctuation as the first character after the wildcard
        regex_str = f"^{escaped_prefix}[_.-][A-Za-z0-9._-]*$"

    try:
        return re.compile(regex_str)  # Case sensitive
    except re.error:
        return None


def _categorize_cookie_db_open(cookie_name: str) -> tuple[CookieCategory, bool, str]:
    """
    Categorizes a cookie based on its name by looking it up in the open cookie database.

    First tries to find an exact match, then falls back to wildcard matching using
    the most specific (longest prefix) match available.

    Args:
        cookie_name: The name of the cookie to categorize

    Returns:
        A tuple containing:
        - The cookie category (from CookieCategory enum)
        - A boolean indicating if this was a wildcard match (True) or exact match (False)
        - The pattern that matched (empty string if no match or exact match)
    """
    data = loader.load_cookie_db_open()

    # First try exact matching
    exact_match = data.loc[data['Cookie / Data Key name'] == cookie_name]
    if not exact_match.empty:
        matching_row = exact_match.iloc[0]
        return _determine_category_ocd(matching_row["Category"]), False, ''

    # Read all rows where the wildcard match
    wildcard_rows = data.loc[data['Wildcard match'] == 1]

    # Prepare all different regexs and check for matching
    # Take the most specific one and later we take the maximum length prefix
    matches = []
    for idx, row in wildcard_rows.iterrows():
        # Skip if the pattern is empty or null
        if pd.isna(row["Cookie / Data Key name"]) or str(row["Cookie / Data Key name"]).strip() == "":
            continue

        pattern = str(row["Cookie / Data Key name"]).strip()

        if "*" not in pattern:
            pattern += "*"
        regex = wildcard_to_regex(pattern)
        if regex and regex.match(cookie_name):
            prefix_len = len(pattern.split('*', 1)[0])
            matches.append((prefix_len, row))

    if matches:
        best_match = max(matches, key=lambda x: x[0])[1]
        return _determine_category_ocd(best_match["Category"]), True, best_match["Cookie / Data Key name"]

    return CookieCategory.UNKNOWN, False, ''


def _determine_category_ocd(category: str) -> CookieCategory:
    match category:
        case "Functional" | "Security":
            return CookieCategory.STRICTLY_NECESSARY
        case "Personalization":
            return CookieCategory.FUNCTIONALITY
        case "Analytics":
            return CookieCategory.PERFORMANCE
        case "Marketing":
            return CookieCategory.TARGETING
        case _:
            return CookieCategory.UNKNOWN


def _categorize_cookie_db_local(cookie_name: str) -> tuple[str | None, CookieCategory]:
    try:
        df = loader.load_cookie_db_local()

        # Strip whitespace just in case
        df["Cookie name"] = df["Cookie name"].str.strip()
        cookie_name = cookie_name.strip()

        result = df[df["Cookie name"] == cookie_name]

        if result.empty:
            return None, CookieCategory.UNKNOWN

        category_value = result["Category"].iloc[0]
        platform_value = result["Platform"].iloc[0]

        cookie_category = CookieCategory(category_value)

        return platform_value, cookie_category
    except Exception as e:
        logger.exception(f"LOCAL: Error occurred: {str(e)}")
        return None, CookieCategory.UNKNOWN


def _create_cookie_name_variations(cookie_name: str) -> list[str]:
    pass


def _categorize(cookie_name) -> tuple[str, CookieCategory]:
    # First check if we've already categorized this cookie (including UNKNOWN ones)
    df = loader.load_cookie_db_local()
    existing_cookie = df[df["Cookie name"] == cookie_name]
    if not existing_cookie.empty:
        return existing_cookie["Platform"].iloc[0], CookieCategory(existing_cookie["Category"].iloc[0])

    # If not in local DB, try open cookie database
    cookie_category, is_wildcard, wildcard_name = _categorize_cookie_db_open(cookie_name)
    if cookie_category is not CookieCategory.UNKNOWN:
        _write_cookie_to_local(cookie_name, cookie_category, "Open Cookie Database", is_wildcard, wildcard_name)
        return "Open Cookie Database", cookie_category

    if not global_config["categorizer_configuration"]["use_only_local"]:
        cookie_category = _categorize_cookie_cookiedatabase(cookie_name)
        if cookie_category is not CookieCategory.UNKNOWN:
            _write_cookie_to_local(cookie_name, cookie_category, "Cookie Database")
            return "Cookie Database", cookie_category

        cookie_category = _categorize_cookie_cookiepedia(cookie_name)
        if cookie_category is not CookieCategory.UNKNOWN:
            _write_cookie_to_local(cookie_name, cookie_category, "Cookiepedia")
            return "Cookiepedia", cookie_category

    # If still unknown, write to local DB to prevent future lookups
    _write_cookie_to_local(cookie_name, CookieCategory.UNKNOWN, "Cookie Analysis")
    return "Cookie Analysis", CookieCategory.UNKNOWN


def _write_cookie_to_local(cookie_name: str, category: CookieCategory, platform: str, is_wildcard=False, wildcard_name=''):
    df = loader.load_cookie_db_local()

    # Only write if not already exists
    if df[df["Cookie name"] == cookie_name].empty:
        new_cookie = {
            "ID": str(uuid.uuid4()),
            "Platform": platform,
            "Category": category.name,
            "Cookie name": cookie_name,
            "Is Wildcard": is_wildcard,
            "Wildcard Name": wildcard_name,
            "Timestamp": datetime.now(timezone.utc).isoformat(),  # Timezone-aware UTC timestamp
        }

        df = pd.concat([df, pd.DataFrame([new_cookie])], ignore_index=True)
        loader.save_cookie_db_local(df)


def _categorize_cookie_cookiepedia(cookie_name: str) -> CookieCategory:
    base_url = "https://cookiepedia.co.uk/cookies/"
    url = base_url + cookie_name

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

    cookie_category = CookieCategory.UNKNOWN

    throttle_domain("cookiepedia.co.uk", THORTTLE_SECONDS_HIGH)

    try:
        response = requests.get(url, headers=headers, timeout=(5, 10))

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            content_left = soup.find('div', id='content-left')
            if content_left is not None:

                second_paragraph = content_left.find_all('p')[1]
                cookie_category = second_paragraph.get_text(strip=True).split(":")[1]
                found_cookie_name = soup.find('div', id='content').find('h1').get_text(strip=True).split(":")[1].strip()

                if cookie_name == found_cookie_name:
                    cookie_category = _determine_category_cp(cookie_category)
                else:
                    logger.warning(f"COOKIEPEDIA: Cookie name dont match. Expected ({cookie_name}) got ({found_cookie_name})")
            else:
                logger.info(f"COOKIEPEDIA: Cookie not found by the name of {cookie_name}.")
        else:
            logger.warning(f"COOKIEPEDIA: Failed to retrieve the page. Status code: {response.status_code}")
    except Exception as e:
        logger.exception(f"COOKIEPEDIA: Exception occurred while inquiring cookiepedia: {e}")

    return cookie_category


def _categorize_cookie_cookiedatabase(cookie_name: str) -> CookieCategory:
    base_url = "https://cookiedatabase.org/"
    url = base_url + cookie_name

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

    throttle_domain("cookiedatabase.org", THROTTLE_SECONDS_MID)

    cookie_category = CookieCategory.UNKNOWN
    try:
        response = requests.get(url, headers=headers, timeout=(5, 10))
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            headings = soup.find_all('h3', class_='elementor-heading-title')

            found_cookie_name = soup.find('h1', class_='elementor-icon-box-title').find('span').get_text(strip=True)
            if found_cookie_name == cookie_name:
                cookie_category = _determine_category_cd(headings[1].get_text(strip=True))
            else:
                logger.warning(f"COOKIEDATABASE: Cookie name don't match. Expected ({cookie_name}) got ({found_cookie_name})")
        else:
            logger.warning(f"COOKIEDATABASE: Failed to retrieve the page. Status code: {response.status_code}")
    except Exception as e:
        logger.error(f"COOKIEDATABASE: Exception occurred while inquiring cookie database: {str(e)}")

    return cookie_category


def _determine_category_cp(category: str) -> CookieCategory:
    match category:
        case "Targeting/Advertising":
            return CookieCategory.TARGETING
        case "Performance":
            return CookieCategory.PERFORMANCE
        case "Strictly Necessary":
            return CookieCategory.STRICTLY_NECESSARY
        case "Functionality":
            return CookieCategory.FUNCTIONALITY
        case _:
            logger.info(f"COOKIEPEDIA: Received either UNKONWN category or UNKONWN by Cookie Analysis: {category}")
            return CookieCategory.UNKNOWN


def _determine_category_cd(category: str) -> CookieCategory:
    match category:
        case "Functional":
            return CookieCategory.STRICTLY_NECESSARY
        case "Statistics" | "Analytics":
            return CookieCategory.PERFORMANCE
        case "Marketing":
            return CookieCategory.TARGETING
        case "Preferences":
            return CookieCategory.FUNCTIONALITY
        case _:
            logger.info(f"COOKIEDATABASE: Received either UNKONWN category or UNKONWN by Cookie Analysis: {category}")
            return CookieCategory.UNKNOWN


def throttle_domain(domain: str, throttle_period: float):
    """
    If we have made a request to this domain recently, ensure we wait
    at least `throttle_period` seconds since that last request.
    """
    global last_request_time

    now = time.time()
    if domain in last_request_time:
        elapsed = now - last_request_time[domain]
        if elapsed < throttle_period:
            # Wait only the difference
            to_wait = throttle_period - elapsed
            logger.info(f"Categorizer waiting for: {to_wait}")
            time.sleep(to_wait)
            logger.info("Categorizer end of waiting.")
    # Update the domain’s last request time
    last_request_time[domain] = time.time()
