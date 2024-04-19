
import sys
from loguru import logger

from config import settings


class CustomLogger:
    def __init__(self):
        logger.remove(0)
        logger.add(sys.stderr, level=settings.LOG_LEVEL)
        self._logger = logger

    def info(self, message):
        self._logger.info(message)

    def debug(self, message):
        self._logger.debug(message)

    def warning(self, message):
        self._logger.warning(message)

    def error(self, message):
        self._logger.error(message)

    def critical(self, message):
        self._logger.critical(message)


custom_logger = CustomLogger()
