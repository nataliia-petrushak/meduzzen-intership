import sys

from loguru import logger


class CustomLogger:
    def __init__(self):
        logger.remove(0)
        logger.add(sys.stderr)
        self.logger = logger


custom_logger = CustomLogger()
