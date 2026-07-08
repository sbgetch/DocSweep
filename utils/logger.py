import logging
from pathlib import Path
from datetime import datetime

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Logs directory
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Daily log file
LOG_FILE = LOG_DIR / f"docsweep_{datetime.now():%Y-%m-%d}.log"

# Configure the root DocSweep logger
root_logger = logging.getLogger("DocSweep")

if not root_logger.handlers:
    root_logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(name)-50s | %(levelname)-8s | %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)


def get_logger(name: str):
    """Return a logger for a DocSweep module."""
    return logging.getLogger(f"DocSweep.{name}")