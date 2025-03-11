import json
import logging
import sys
import traceback
from datetime import datetime
from pathlib import Path
from queue import Queue
from threading import Thread

from src.core.categorizer import categorizer
from src.core.common import loader
from src.core.crawler.crawler import ProcessorLoader
from src.entities.models.WebsiteCrawl import WebsiteCrawl
from src.logging_config import setup_logging

logger = logging.getLogger(__name__)


def serialize_website_crawl_to_json(website_crawl: WebsiteCrawl) -> str:
    """Convert WebsiteCrawl instance to JSON string."""
    return json.dumps(website_crawl.to_dict(), indent=4)


def save_website_crawl_to_file(crawl: WebsiteCrawl, website_output_dir: Path):
    """Save WebsiteCrawl data to a file."""
    website_output_dir.mkdir(parents=True, exist_ok=True)
    file_path = website_output_dir / "analysis.json"

    with file_path.open("w", encoding="utf-8") as f:
        f.write(serialize_website_crawl_to_json(crawl))

    logger.info(f"Saved WebsiteCrawl data to {file_path}")


def crawler_worker(website_queue, analysis_output_dir, result_queue):
    """Worker function for crawlers, takes websites from queue."""
    processor_loader = ProcessorLoader()
    processor = processor_loader.load_processor()

    while not website_queue.empty():
        website = website_queue.get()
        if website is None:
            break

        try:
            logger.info(f"[Crawler] Initiating crawl on: {website}")
            sanitized_name = website.replace("://", "_").replace("/", "_")
            website_output_dir = analysis_output_dir / sanitized_name

            if website_output_dir.exists():
                logger.info(f"[Crawler] Directory '{website_output_dir}' already exists. Skipping.")
                continue

            website_output_dir.mkdir(parents=True, exist_ok=True)

            crawl = processor.crawl(website, website_output_dir)
            if crawl is None or not isinstance(crawl, WebsiteCrawl):
                logger.error(f"[Crawler] Invalid state for {website}: The result of the crawl must not be None.")
                continue

            result_queue.put((crawl, website_output_dir))

        except Exception as e:
            _handle_exception(e, website, analysis_output_dir)
        finally:
            website_queue.task_done()


def categorizer_worker(result_queue):
    """Single-threaded categorizer that processes crawl results."""
    while True:
        item = result_queue.get()
        if item is None:
            result_queue.task_done()
            break

        crawl, website_output_dir = item

        try:
            logger.info(f"[Categorizer] Processing {website_output_dir}")
            categorizer.process_crawl(crawl)
            save_website_crawl_to_file(crawl, website_output_dir)
        except Exception as e:
            website = crawl.web_page if crawl else "Unknown"
            _handle_exception(e, website, website_output_dir)
        finally:
            result_queue.task_done()


def _handle_exception(exception, website, website_output_dir):
    """Handles exceptions and logs them to a file."""
    exception_message = (
            f"Error processing website: {website}\n"
            f"Exception: {str(exception)}\n"
            + traceback.format_exc()
    )

    time_part = datetime.now().isoformat(timespec="seconds").replace(":", "-")
    sanitized_name = website.replace("://", "_").replace("/", "_")
    error_filename = f"{sanitized_name}_{time_part}_error.txt"

    error_output_path = website_output_dir / error_filename

    try:
        with error_output_path.open('w', encoding='utf-8') as error_file:
            error_file.write(exception_message)
        logger.error(f"[Error] Logged exception to {error_output_path}")
    except Exception as ex:
        logger.error(f"[Error] Failed to write error file: {str(ex)}. Original exception: {exception_message}")


def main():
    global logger

    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        config = loader.load_config()
    except FileNotFoundError:
        logger.error("Configuration file not found.")
        sys.exit(1)

    try:
        proc_loader = ProcessorLoader()
        proc_loader.validate()
    except Exception as e:
        logger.error(f"Error while loading the processor: {str(e)}")
        sys.exit(2)

    try:
        analysis_config = config["cookie_crawler_configuration"]

        analysis_output_dir = (
                Path(config['paths']['outputs']['analysis_report_dir']) /
                analysis_config['name_of_analysis']
        )
        analysis_output_dir.mkdir(parents=True, exist_ok=True)

        active_website_list = analysis_config['active_website_list']
        active_website_list_path = config['paths']['website_lists'][active_website_list]

        with open(active_website_list_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        websites = data.get('websites', [])
        if not websites:
            logger.error("No websites found in the active website list.")
            sys.exit(3)

        # Create shared queues
        website_queue = Queue()
        result_queue = Queue()

        # Fill the queue with websites
        for website in websites:
            website_queue.put(website)

        # Number of crawler threads
        num_crawler_threads = 1

        # Start crawler workers
        crawler_threads = []
        for _ in range(num_crawler_threads):
            t = Thread(target=crawler_worker, args=(website_queue, analysis_output_dir, result_queue), daemon=True)
            t.start()
            crawler_threads.append(t)

        # Start single categorizer worker
        categorizer_thread = Thread(target=categorizer_worker, args=(result_queue,), daemon=True)
        categorizer_thread.start()

        # Wait for all crawlers to finish
        for t in crawler_threads:
            t.join()

        # Signal categorizer to stop
        result_queue.put(None)
        categorizer_thread.join()

        logger.info("All crawling and categorization tasks are complete.")

    except KeyError as e:
        logger.error(f"Configuration is missing required key: {e}")
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON file: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    main()
