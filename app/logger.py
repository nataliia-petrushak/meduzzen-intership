from loguru import logger


class CustomLogger:
    def __init__(self, log_file: str = "logs/app.log"):
        self.log_file = log_file
        logger.add(self.log_file, rotation="500 MB", level="DEBUG")

    def info(self, message):
        logger.info(message)

    def debug(self, message):
        logger.debug(message)

    def warning(self, message):
        logger.warning(message)

    def error(self, message):
        logger.error(message)

    def critical(self, message):
        logger.critical(message)


custom_logger = CustomLogger()
