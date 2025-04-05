import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, "app.log")
MAX_LOG_SIZE = 10 * 1024 * 1024
LOG_BACKUP_COUNT = 3


def configure_logging():
    """Конфигурация логирования."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=LOG_BACKUP_COUNT)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(console_handler)

    logger.info("Logging is configured.")


if __name__ == "__main__":
    configure_logging()
    logging.info("This is an info message.")
    logging.error("This is an error message.")
