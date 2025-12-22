import logging
import traceback

from error import Error


class Logger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.addHandler(logging.FileHandler(f"{name}.log"))

    def info(self, message: str):
        self.logger.info(message)

    def unexpected_error(self, exception: Exception):
        self.logger.error(f"""
Unexpected error:
    Class: {exception.__class__.__name__}
    Traceback: {traceback.format_exc()}
""")

    def error(self, error: Error):
        self.logger.error(f"""
Error:
    Class: {error.__class__.__name__}
    Message: {str(error)}
""")
