import logging
import os
import re
import sys
from logging.handlers import RotatingFileHandler

from johnny_indexer.config import ConfigHelper
from johnny_indexer.paths import LOGS_PATH

"""
log.py

Sets up logging for a run. Modules log through `logging.getLogger(__name__)`, and
messages go to:
- The console (stderr), only when it's a terminal. Scheduled runs have no terminal, so
  they only write to the log file.
- logs/<notes directory name>.log, for commands that run on a notes directory. Rotated
  at 1 MB, keeping 3 old files.

The log_level config option sets which messages are shown. Warnings are always counted,
so a run that logged any exits with EXIT_WARNINGS.
"""

EXIT_WARNINGS = 2

_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR")
_MAX_LOG_BYTES = 1_000_000
_LOG_BACKUP_COUNT = 3
_FILE_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"

logger = logging.getLogger(__name__)


class _ConsoleFormatter(logging.Formatter):
    """Shows only the message, with its level in front for warnings and errors."""

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        if record.levelno >= logging.WARNING:
            return f"{record.levelname}: {message}"
        return message


class _WarningCounter(logging.Handler):
    def __init__(self) -> None:
        super().__init__(logging.WARNING)
        self.count = 0

    def emit(self, record: logging.LogRecord) -> None:
        self.count += 1


_warning_counter = _WarningCounter()


def log_path(notes_path: str) -> str:
    log_name = re.sub(r"[^A-Za-z0-9_.-]", "_", os.path.basename(notes_path))
    return os.path.join(LOGS_PATH, f"{log_name}.log")


def setup_logging(notes_path: str | None) -> None:
    """Sets up the handlers, logging to the notes directory's log file when given."""
    handlers: list[logging.Handler] = []
    if sys.stderr.isatty():
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(_ConsoleFormatter())
        handlers.append(console_handler)
    if notes_path is not None:
        os.makedirs(LOGS_PATH, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_path(notes_path),
            maxBytes=_MAX_LOG_BYTES,
            backupCount=_LOG_BACKUP_COUNT,
            encoding="utf-8",
        )
        file_handler.setFormatter(logging.Formatter(_FILE_FORMAT))
        handlers.append(file_handler)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    for handler in [*handlers, _warning_counter]:
        root_logger.addHandler(handler)

    # Handlers are set up first, so warnings from loading the config are logged
    level = _configured_level()
    for handler in handlers:
        handler.setLevel(level)
    root_logger.setLevel(min(level, logging.WARNING))


def _configured_level() -> int:
    level = ConfigHelper.load_from_config("log_level")
    if level not in _LEVELS:
        logger.warning(
            "log_level must be one of %s, got '%s'. Using INFO.",
            ", ".join(_LEVELS),
            level,
        )
        return logging.INFO
    return logging.getLevelNamesMapping()[level]


def warning_count() -> int:
    return _warning_counter.count
