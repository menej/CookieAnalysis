import logging

from datetime import datetime
from typing import Optional, Any

from src.entities.models.Stage import Stage

logger = logging.getLogger(__name__)

class WebsiteCrawl:
    """
    Represents a complete website crawl session, managing multiple stages of interaction.

    WebsiteCrawl orchestrates the entire crawling process for a single website, including
    different stages of interaction like normal browsing, accepting cookies, and declining
    cookies. It maintains configuration settings and timing information for the overall crawl.

    Attributes:
        web_page (str): The URL of the website being crawled.

        name_of_analysis (str): Identifier for this analysis run, used for grouping related crawls.

        crawl_mode (str): The type of processor being used/crawling being performed.
            Affects how the crawler interacts with the website.

        browser_provider (str): The browser being used for crawling (e.g., 'chrome', 'firefox').
            Determines which browser automation tools are used.

        take_screenshots (bool): Whether to capture screenshots during the crawl.
            Defaults to False to save storage space.

        timestamp_start (Optional[datetime]): When the overall crawl began, set by start().

        timestamp_stop (Optional[datetime]): When the overall crawl completed, set by stop().

        normal_stage (Optional[Stage]): Stage representing normal browsing without
            cookie preference selection.

        accept_stage (Optional[Stage]): Stage representing browsing after accepting
            cookie preferences.

        decline_stage (Optional[Stage]): Stage representing browsing after declining
            cookie preferences.
    """

    def __init__(
        self,
        web_page: str,
        name_of_analysis: str,
        crawl_mode: str,
        browser_provider: str,
        take_screenshots: bool = False,
    ):
        self.web_page = web_page
        self.name_of_analysis = name_of_analysis
        self.crawl_mode = crawl_mode
        self.browser_provider = browser_provider
        self.take_screenshots = take_screenshots

        self.timestamp_start: Optional[datetime] = None
        self.timestamp_stop: Optional[datetime] = None

        self.normal_stage: Optional[Stage] = None
        self.accept_stage: Optional[Stage] = None
        self.decline_stage: Optional[Stage] = None

    def start(self):
        """
        Marks the beginning of the website crawl by recording the current timestamp.
        This should be called before any crawling operations begin.
        """
        self.timestamp_start = datetime.now()
        logger.info(f"Crawl started at {self.timestamp_start} for {self.web_page}")

    def stop(self):
        """
        Marks the completion of the website crawl by recording the current timestamp.
        This should be called after all crawling operations are complete.
        """
        self.timestamp_stop = datetime.now()
        logger.info(f"Crawl stopped at {self.timestamp_stop} for {self.web_page}")

    def to_dict(self) -> dict[str, Any]:
        """
        Converts the WebsiteCrawl instance to a serializable dictionary format.

        Returns:
            dict[str, Any]: A dictionary containing all crawl data with base datetime
                objects converted to ISO format strings and Stage objects converted to
                their dictionary representations. The resulting dictionary can be directly
                serialized to JSON.
        """
        return {
            "web_page": self.web_page,
            "name_of_analysis": self.name_of_analysis,
            "crawl_mode": self.crawl_mode,
            "browser_provider": self.browser_provider,
            "take_screenshots": self.take_screenshots,
            "timestamp_start": self.timestamp_start.isoformat() if self.timestamp_start else None,
            "timestamp_stop": self.timestamp_stop.isoformat() if self.timestamp_stop else None,
            "normal_stage": self.normal_stage.to_dict() if self.normal_stage else None,
            "accept_stage": self.accept_stage.to_dict() if self.accept_stage else None,
            "decline_stage": self.decline_stage.to_dict() if self.decline_stage else None,
        }