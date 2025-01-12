from collections import defaultdict
from typing import Any, Optional


class Stage:
    def __init__(self):
        # List of interactions (strings)
        self.interactions: Optional[list[str]] = None

        # List of pages visited (strings)
        self.pages_visited: Optional[list[str]] = None

        # Dictionary where values are defaultdicts
        self.stage_cookies: Optional[dict[str, defaultdict[str, Any]]] = None

        # List of exceptions (strings)
        self.exceptions: Optional[list[str]] = None

        # List of screenshots (strings, file paths or URLs)
        self.screenshots: Optional[list[str]] = None

        # Metadata dictionary with values as any type
        self.metadata: Optional[dict[str, Any]] = None
