import logging
import sys


def setup_logging(log_level=logging.INFO, log_file="app.log"):
    """Sets up application-wide logging."""

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    file_handler = logging.FileHandler(log_file, encoding="utf-8")

    stream_handler = logging.StreamHandler(sys.stdout)
    try:
        stream_handler.stream.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    # Set formatting for both handlers
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Get the root logger and configure it
    logger = logging.getLogger()
    logger.setLevel(log_level)
    logger.handlers = [file_handler, stream_handler]  # Replace handlers to avoid duplicates

    logging.captureWarnings(True)