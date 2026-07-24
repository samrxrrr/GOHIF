from __future__ import annotations

import logging
from pathlib import Path

from rich.logging import RichHandler


def setup_logger(
    log_directory: Path = Path("logs"),
    log_level: str = "INFO",
) -> logging.Logger:

    log_directory.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("GAE")

    if logger.handlers:
        return logger

    logger.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        log_directory / "gae.log",
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    console_handler = RichHandler(
        rich_tracebacks=True,
        show_path=False,
    )

    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
