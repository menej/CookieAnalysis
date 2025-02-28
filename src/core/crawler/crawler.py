from pathlib import Path
from importlib import import_module
from typing import Any, Optional

from src.entities.models.WebsiteCrawl import WebsiteCrawl
from src.core.common import loader

class ProcessorLoader:
    def __init__(self, config: Optional[dict] = None):
        """
        Initialize ProcessorLoader with optional config.
        If config is not provided, it will be loaded when needed.
        """
        self._config = config
        self._processor = None

    @property
    def config(self) -> dict:
        """Lazy load configuration if not already loaded."""
        if self._config is None:
            self._config = loader.load_config()
        return self._config

    @staticmethod
    def _get_module_path(crawl_mode: str) -> str:
        """Constructs the module path based on the crawl mode."""
        return f"src.core.crawler.processors.{crawl_mode.lower()}.processor"

    def validate(self) -> bool:
        """
        Validates that the processor can be loaded and has required attributes.
        Returns True if valid, raises appropriate exception if invalid.
        """
        try:
            self.load_processor()
            return True
        except (NotImplementedError, AttributeError) as e:
            raise e

    def load_processor(self) -> Any:
        """
        Loads and validates the processor module based on configuration.
        Caches the processor for subsequent calls.

        Returns:
            The loaded processor module

        Raises:
            NotImplementedError: If the processor module is not found
            AttributeError: If the processor module doesn't have a crawl function
        """
        if self._processor is not None:
            return self._processor

        crawl_mode = self.config["cookie_crawler_configuration"]["crawl_mode"]
        module_path = self._get_module_path(crawl_mode)

        try:
            processor_module = import_module(module_path)
        except ModuleNotFoundError as e:
            raise NotImplementedError(f"Processor module not found for crawl mode: {crawl_mode}") from e

        if not hasattr(processor_module, "crawl"):
            raise AttributeError(f"The processor module '{module_path}' does not have a 'crawl' function.")

        self._processor = processor_module
        return processor_module


def crawl(web_page: str, output_path: Path, processor_loader: Optional[ProcessorLoader] = None) -> WebsiteCrawl:
    """
    Crawls a webpage using the configured processor.

    Args:
        web_page: URL of the webpage to crawl
        output_path: Path to store the crawl results
        processor_loader: Optional ProcessorLoader instance to reuse

    Returns:
        WebsiteCrawl: Results of the crawl operation
    """
    if processor_loader is None:
        processor_loader = ProcessorLoader()
    processor = processor_loader.load_processor()
    return processor.crawl(web_page, output_path)