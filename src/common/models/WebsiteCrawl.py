from datetime import datetime
from typing import Optional

from src.common.models.Stage import Stage


class WebsiteCrawl:
    def __init__(
        self,
        web_page: str,
        name_of_analysis: str,
        crawl_mode: str,
        browser_provider: str,
        simulate_mobile: bool = False,
        take_screenshots: bool = False,
    ):
        """
        Initializes a WebsiteCrawl instance with the provided parameters.

        :param web_page: The web page to crawl.
        :param name_of_analysis: The name of the analysis being conducted.
        :param crawl_mode: The mode of crawling (e.g., automated, manual).
        :param browser_provider: The browser used for crawling (e.g., Chrome, Firefox).
        :param simulate_mobile: Whether to simulate a mobile device during the crawl.
        :param take_screenshots: Whether to take screenshots during the crawl.
        """
        self.web_page: str = web_page
        self.name_of_analysis: str = name_of_analysis
        self.crawl_mode: str = crawl_mode
        self.browser_provider: str = browser_provider
        self.simulate_mobile: bool = simulate_mobile
        self.take_screenshots: bool = take_screenshots

        self.timestamp_start: Optional[datetime] = None
        self.timestamp_stop: Optional[datetime] = None

        self.normal_stage: Optional[Stage] = None
        self.accept_stage: Optional[Stage] = None
        self.decline_stage: Optional[Stage] = None

    def start(self):
        """Sets the start timestamp to the current time."""
        self.timestamp_start = datetime.now()
        print(f"Start time set: {self.timestamp_start}")

    def stop(self):
        """Sets the stop timestamp to the current time."""
        self.timestamp_stop = datetime.now()
        print(f"Stop time set: {self.timestamp_stop}")
