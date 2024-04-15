import sys

from loguru import logger

from app.config import settings


class CustomLogger:
    def __init__(self):
        logger.remove(0)
        logger.add(sys.stderr, level=settings.LOG_LEVEL)
        self.logger = logger

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


custom_logger = CustomLogger()
