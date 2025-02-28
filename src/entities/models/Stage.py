import logging

from datetime import datetime
from typing import Any, Optional

logger = logging.getLogger(__name__)

class Stage:
    """
    Represents a stage in the website crawling process, capturing interactions, cookies, and metadata.

    A Stage tracks various aspects of website interaction during a specific phase of crawling,
    such as normal browsing, accepting cookies, or declining cookies. It maintains lists of
    interactions performed, pages visited, cookies encountered, exceptions raised, and screenshots
    taken during the stage.

    Attributes:
        interactions (list[str]): Chronological list of user interactions performed during the stage,
            such as button clicks, form submissions, or navigation actions.

        pages_visited (list[str]): URLs of all pages visited during this stage of the crawl.

        stage_cookies (dict[str, list[dict]]): Mapping of parts of visit stage to lists of cookie details.
            Each cookie is represented as a dictionary containing properties like name, value, domain, etc.

        exceptions (list[str]): List of error messages or exceptions encountered during the stage.

        screenshots (list[str]): File paths or references to screenshots taken during the stage.
            These may be local file paths or URLs depending on the storage configuration.

        metadata (dict[str, Any]): Additional stage-specific data that doesn't fit into other categories.
            Can store any serializable values. Note: Users must ensure all metadata values are JSON
            serializable (e.g., basic types like str, int, float, bool, list, dict) as the Stage
            will be converted to JSON. Non-serializable types (like datetime objects, custom classes)
            must be converted to serializable formats before being added to metadata.

        timestamp_start (Optional[datetime]): When the stage began execution, set by start().

        timestamp_stop (Optional[datetime]): When the stage finished execution, set by stop().
    """

    def __init__(self):
        self.interactions: list[str] = list()
        self.pages_visited: list[str] = list()
        self.stage_cookies: dict[str, list[dict]] = dict()
        self.exceptions: list[str] = list()
        self.screenshots: list[str] = list()
        self.metadata: dict[str, Any] = dict()
        self.timestamp_start: Optional[datetime] = None
        self.timestamp_stop: Optional[datetime] = None

    def start(self):
        """
        Marks the beginning of the stage by recording the current timestamp.
        This should be called before any stage operations begin.
        """
        self.timestamp_start = datetime.now()
        logger.info(f"Stage start time set: {self.timestamp_start}")

    def stop(self):
        """
        Marks the completion of the stage by recording the current timestamp.
        This should be called after all stage operations are complete.
        """
        self.timestamp_stop = datetime.now()
        logger.info(f"Stage stop time set: {self.timestamp_stop}")

    def to_dict(self) -> dict[str, Any]:
        """
        Converts the Stage instance to a serializable dictionary format.

        Returns:
            dict[str, Any]: A dictionary containing all stage data with base datetime
                objects converted to ISO format strings. The resulting dictionary can
                be directly serialized to JSON.
        """
        return {
            "interactions": self.interactions,
            "pages_visited": self.pages_visited,
            "stage_cookies": self.stage_cookies,
            "exceptions": self.exceptions,
            "screenshots": self.screenshots,
            "metadata": self.metadata,
            "timestamp_start": self.timestamp_start.isoformat() if self.timestamp_start else None,
            "timestamp_stop": self.timestamp_stop.isoformat() if self.timestamp_stop else None,
        }