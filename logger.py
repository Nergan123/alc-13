import logging


class LoggingHandler:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
