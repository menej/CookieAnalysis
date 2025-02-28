from pathlib import Path

from src.entities.models.WebsiteCrawl import WebsiteCrawl


def crawl(web_page: str, output_path: Path) -> WebsiteCrawl:
    ...
